//! Synthetic non-product shell for COMPANION-P00-QUAL-001 only.
use serde_json::{Map, Value};
use sha2::{Digest, Sha256};
use std::{collections::HashSet, env, fs, io::{Read, Write}, os::unix::net::UnixListener, path::Path};

const MAX_EXACT_INT: i64 = 9_007_199_254_740_991;
const REQUIRED: [&str; 17] = ["authority_class","boot_id","causation_id","canonicalization_version","correlation_id","digest_version","event_sequence","message_id","monotonic_ns","payload","privacy_class","producer","producer_version","schema_uri","schema_version","utc_observed","utc_uncertainty_us"];

fn reject_duplicate_keys(raw: &str) -> Result<(), String> {
    // Deliberately small JSON lexical gate: tracks every object key before serde_json
    // discards duplicate information. Fixtures exercise ASCII protocol keys only.
    let bytes = raw.as_bytes(); let mut i = 0; let mut in_string = false; let mut escaped = false;
    let mut stacks: Vec<HashSet<String>> = Vec::new();
    while i < bytes.len() {
        if in_string {
            if escaped { escaped = false; i += 1; continue; }
            if bytes[i] == b'\\' { escaped = true; i += 1; continue; }
            if bytes[i] == b'"' { in_string = false; }
            i += 1; continue;
        }
        match bytes[i] {
            b'"' => {
                let start = i + 1; let mut j = start; let mut esc = false;
                while j < bytes.len() { if !esc && bytes[j] == b'"' { break; } if !esc && bytes[j] == b'\\' { esc=true; } else { esc=false; } j += 1; }
                if j == bytes.len() { return Err("unterminated-string".into()); }
                let mut k = j + 1; while k < bytes.len() && bytes[k].is_ascii_whitespace() { k += 1; }
                if k < bytes.len() && bytes[k] == b':' {
                    let key = String::from_utf8_lossy(&bytes[start..j]).to_string();
                    if let Some(keys) = stacks.last_mut() { if !keys.insert(key) { return Err("duplicate-key".into()); } }
                }
                i = j + 1;
            },
            b'{' => { stacks.push(HashSet::new()); i += 1; },
            b'}' => { stacks.pop(); i += 1; },
            _ => i += 1,
        }
    }
    Ok(())
}

fn walk(value: &Value) -> Result<(), String> {
    match value {
        Value::Number(n) => {
            if let Some(v)=n.as_i64() { if v.abs() > MAX_EXACT_INT { return Err("integer-range".into()); } }
            else if n.as_u64().map_or(true, |v| v > MAX_EXACT_INT as u64) { return Err("noncanonical-number".into()); }
        },
        Value::String(s) if s.chars().any(|c| (0xD800..=0xDFFF).contains(&(c as u32))) => return Err("lone-surrogate".into()),
        Value::Array(a) => for v in a { walk(v)?; },
        Value::Object(o) => for v in o.values() { walk(v)?; },
        _ => {},
    } Ok(())
}

fn parse(raw: &str) -> Result<Map<String, Value>, String> {
    reject_duplicate_keys(raw)?;
    let value: Value = serde_json::from_str(raw).map_err(|e| format!("json:{e}"))?;
    walk(&value)?;
    value.as_object().cloned().ok_or_else(|| "envelope-object".into())
}

fn canonical(value: &Value) -> Result<Vec<u8>, String> { serde_json::to_vec(value).map_err(|e| e.to_string()) }

fn validate(event: &Map<String, Value>) -> Result<(), String> {
    if event.len()!=REQUIRED.len() || REQUIRED.iter().any(|k| !event.contains_key(*k)) { return Err("envelope-fields".into()); }
    if event.get("canonicalization_version") != Some(&Value::String("JCS-RFC8785-v1".into())) || event.get("digest_version") != Some(&Value::String("sha-256-jcs-event-v1".into())) { return Err("canonical-profile".into()); }
    if !event.get("schema_version").and_then(Value::as_str).map_or(false, |s| s.split('.').next()==Some("1")) { return Err("schema-major".into()); }
    if !event.get("payload").and_then(Value::as_object).and_then(|p|p.get("fixed_point_delta")).map_or(false, Value::is_i64) { return Err("payload".into()); }
    for key in ["boot_id","monotonic_ns","event_sequence","causation_id","message_id"] { if event.get(key).and_then(Value::as_str).map_or(true, str::is_empty) { return Err(format!("field:{key}")); } }
    Ok(())
}

fn process(raw: &str, seen: &mut HashSet<String>) -> Result<Value, String> {
    let event=parse(raw)?; validate(&event)?; let message=event["message_id"].as_str().unwrap().to_string();
    let duplicate=!seen.insert(message); let bytes=canonical(&Value::Object(event.clone()))?;
    let digest=format!("{:x}", Sha256::digest(bytes)); let delta=event["payload"]["fixed_point_delta"].as_i64().unwrap();
    Ok(serde_json::json!({"accepted":true,"duplicate":duplicate,"digest":digest,"fixed_point_state":if duplicate {0} else {delta}}))
}

fn recv_frame(stream: &mut std::os::unix::net::UnixStream) -> Result<String,String> { let mut h=[0;4]; stream.read_exact(&mut h).map_err(|_|"short-header")?; let n=u32::from_be_bytes(h) as usize; if n>65536{return Err("frame-limit".into())}; let mut b=vec![0;n]; stream.read_exact(&mut b).map_err(|_|"short-frame")?; String::from_utf8(b).map_err(|_|"utf8".into()) }
fn send_frame(stream: &mut std::os::unix::net::UnixStream, value:&Value)->Result<(),String>{let b=canonical(value)?;stream.write_all(&(b.len() as u32).to_be_bytes()).and_then(|_|stream.write_all(&b)).map_err(|e|e.to_string())}
fn serve(path:&Path)->Result<(),String>{let _=fs::remove_file(path);let listener=UnixListener::bind(path).map_err(|e|e.to_string())?;let(mut stream,_)=listener.accept().map_err(|e|e.to_string())?;let mut seen=HashSet::new();let raw=recv_frame(&mut stream)?;let result=process(&raw,&mut seen).unwrap_or_else(|e|serde_json::json!({"accepted":false,"reason":e}));send_frame(&mut stream,&result)?;drop(listener);let _=fs::remove_file(path);Ok(())}

fn self_test(fixture:&Path)->Result<(),String>{let raw=fs::read_to_string(fixture).map_err(|e|e.to_string())?;let first=process(&raw,&mut HashSet::new())?;let mut seen=HashSet::from(["message-0001".to_string()]);let again=process(&raw,&mut seen)?;if first["fixed_point_state"]!=25 || again["fixed_point_state"]!=0{return Err("idempotency".into())};for bad in [r#"{"message_id":"a","message_id":"b"}"#,r#"{"x":NaN}"#,r#""\ud800""#]{if parse(bad).is_ok(){return Err("invalid-accepted".into())}};let mut event=parse(&raw)?;event.insert("schema_version".into(),Value::String("2.0".into()));if validate(&event).is_ok(){return Err("major-accepted".into())};println!("{}",serde_json::json!({"self_test":"passed","digest":first["digest"],"rust":env!("CARGO_PKG_VERSION")}));Ok(())}
fn main(){let a:Vec<String>=env::args().collect();let result=if a.len()==3&&a[1]=="--self-test"{self_test(Path::new(&a[2]))}else if a.len()==3&&a[1]=="--serve"{serve(Path::new(&a[2]))}else{Err("usage: --self-test FIXTURE | --serve SOCKET".into())};if let Err(e)=result{eprintln!("{e}");std::process::exit(2)}}
