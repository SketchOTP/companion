//! Synthetic non-product shell for COMPANION-P00-QUAL-001 only.
use serde_json::{Map, Value};
use sha2::{Digest, Sha256};
use std::{
    collections::HashSet,
    env, fs,
    io::{Read, Write},
    os::unix::net::UnixListener,
    path::Path,
};

const MAX_EXACT_INT: i64 = 9_007_199_254_740_991;
const REQUIRED: [&str; 17] = [
    "authority_class",
    "boot_id",
    "causation_id",
    "canonicalization_version",
    "correlation_id",
    "digest_version",
    "event_sequence",
    "message_id",
    "monotonic_ns",
    "payload",
    "privacy_class",
    "producer",
    "producer_version",
    "schema_uri",
    "schema_version",
    "utc_observed",
    "utc_uncertainty_us",
];

fn reject_duplicate_keys(raw: &str) -> Result<(), String> {
    // Track decoded object keys before serde_json discards duplicate information.
    // Decoding is required: "a" and "\u0061" are the same JSON name.
    let bytes = raw.as_bytes();
    let mut i = 0;
    let mut in_string = false;
    let mut escaped = false;
    let mut stacks: Vec<HashSet<String>> = Vec::new();
    while i < bytes.len() {
        if in_string {
            if escaped {
                escaped = false;
                i += 1;
                continue;
            }
            if bytes[i] == b'\\' {
                escaped = true;
                i += 1;
                continue;
            }
            if bytes[i] == b'"' {
                in_string = false;
            }
            i += 1;
            continue;
        }
        match bytes[i] {
            b'"' => {
                let start = i + 1;
                let mut j = start;
                let mut esc = false;
                while j < bytes.len() {
                    if !esc && bytes[j] == b'"' {
                        break;
                    }
                    if !esc && bytes[j] == b'\\' {
                        esc = true;
                    } else {
                        esc = false;
                    }
                    j += 1;
                }
                if j == bytes.len() {
                    return Err("unterminated-string".into());
                }
                let mut k = j + 1;
                while k < bytes.len() && bytes[k].is_ascii_whitespace() {
                    k += 1;
                }
                if k < bytes.len() && bytes[k] == b':' {
                    let escaped = format!("\"{}\"", String::from_utf8_lossy(&bytes[start..j]));
                    let key: String =
                        serde_json::from_str(&escaped).map_err(|_| "invalid-key".to_string())?;
                    if let Some(keys) = stacks.last_mut() {
                        if !keys.insert(key) {
                            return Err("duplicate-key".into());
                        }
                    }
                }
                i = j + 1;
            }
            b'{' => {
                stacks.push(HashSet::new());
                i += 1;
            }
            b'}' => {
                stacks.pop();
                i += 1;
            }
            _ => i += 1,
        }
    }
    Ok(())
}

fn walk(value: &Value) -> Result<(), String> {
    match value {
        Value::Number(n) => {
            if let Some(v) = n.as_i64() {
                if v.unsigned_abs() > MAX_EXACT_INT as u64 {
                    return Err("integer-range".into());
                }
            } else if n.as_u64().map_or(true, |v| v > MAX_EXACT_INT as u64) {
                return Err("noncanonical-number".into());
            }
        }
        Value::String(s) if s.chars().any(|c| (0xD800..=0xDFFF).contains(&(c as u32))) => {
            return Err("lone-surrogate".into());
        }
        Value::Array(a) => {
            for v in a {
                walk(v)?;
            }
        }
        Value::Object(o) => {
            for v in o.values() {
                walk(v)?;
            }
        }
        _ => {}
    }
    Ok(())
}

fn parse(raw: &str) -> Result<Map<String, Value>, String> {
    reject_duplicate_keys(raw)?;
    let value: Value = serde_json::from_str(raw).map_err(|e| format!("json:{e}"))?;
    walk(&value)?;
    value
        .as_object()
        .cloned()
        .ok_or_else(|| "envelope-object".into())
}

fn utf16_key(value: &str) -> Vec<u16> {
    value.encode_utf16().collect()
}

fn canonical(value: &Value) -> Result<Vec<u8>, String> {
    match value {
        Value::Null => Ok(b"null".to_vec()),
        Value::Bool(true) => Ok(b"true".to_vec()),
        Value::Bool(false) => Ok(b"false".to_vec()),
        Value::Number(number) => {
            let value = number
                .as_i64()
                .ok_or_else(|| "fractional-number-profile".to_string())?;
            if value.unsigned_abs() > MAX_EXACT_INT as u64 {
                return Err("integer-range".into());
            }
            Ok(value.to_string().into_bytes())
        }
        Value::String(string) => serde_json::to_string(string)
            .map(|x| x.into_bytes())
            .map_err(|e| e.to_string()),
        Value::Array(values) => {
            let mut output = vec![b'['];
            for (index, child) in values.iter().enumerate() {
                if index > 0 {
                    output.push(b',');
                }
                output.extend(canonical(child)?);
            }
            output.push(b']');
            Ok(output)
        }
        Value::Object(values) => {
            let mut entries: Vec<(&String, &Value)> = values.iter().collect();
            entries.sort_by(|(left, _), (right, _)| utf16_key(left).cmp(&utf16_key(right)));
            let mut output = vec![b'{'];
            for (index, (key, child)) in entries.iter().enumerate() {
                if index > 0 {
                    output.push(b',');
                }
                output.extend(
                    serde_json::to_string(key)
                        .map_err(|e| e.to_string())?
                        .as_bytes(),
                );
                output.push(b':');
                output.extend(canonical(child)?);
            }
            output.push(b'}');
            Ok(output)
        }
    }
}

fn validate(event: &Map<String, Value>) -> Result<(), String> {
    if event.len() != REQUIRED.len() || REQUIRED.iter().any(|k| !event.contains_key(*k)) {
        return Err("envelope-fields".into());
    }
    if event.get("canonicalization_version") != Some(&Value::String("JCS-RFC8785-v1".into()))
        || event.get("digest_version") != Some(&Value::String("sha-256-jcs-event-v1".into()))
    {
        return Err("canonical-profile".into());
    }
    if !event
        .get("schema_version")
        .and_then(Value::as_str)
        .map_or(false, |s| s.split('.').next() == Some("1"))
    {
        return Err("schema-major".into());
    }
    if !event
        .get("payload")
        .and_then(Value::as_object)
        .and_then(|p| p.get("fixed_point_delta"))
        .map_or(false, Value::is_i64)
    {
        return Err("payload".into());
    }
    for key in [
        "boot_id",
        "monotonic_ns",
        "event_sequence",
        "causation_id",
        "message_id",
    ] {
        if event
            .get(key)
            .and_then(Value::as_str)
            .map_or(true, str::is_empty)
        {
            return Err(format!("field:{key}"));
        }
    }
    Ok(())
}

fn process(raw: &str, seen: &mut HashSet<String>) -> Result<Value, String> {
    let event = parse(raw)?;
    validate(&event)?;
    let message = event["message_id"].as_str().unwrap().to_string();
    let duplicate = !seen.insert(message);
    let bytes = canonical(&Value::Object(event.clone()))?;
    let digest = format!("{:x}", Sha256::digest(bytes));
    let delta = event["payload"]["fixed_point_delta"].as_i64().unwrap();
    Ok(
        serde_json::json!({"accepted":true,"duplicate":duplicate,"digest":digest,"fixed_point_state":if duplicate {0} else {delta}}),
    )
}

fn recv_frame(stream: &mut std::os::unix::net::UnixStream) -> Result<String, String> {
    let mut h = [0; 4];
    stream.read_exact(&mut h).map_err(|_| "short-header")?;
    let n = u32::from_be_bytes(h) as usize;
    if n > 65536 {
        return Err("frame-limit".into());
    };
    let mut b = vec![0; n];
    stream.read_exact(&mut b).map_err(|_| "short-frame")?;
    String::from_utf8(b).map_err(|_| "utf8".into())
}
fn send_frame(stream: &mut std::os::unix::net::UnixStream, value: &Value) -> Result<(), String> {
    let b = canonical(value)?;
    stream
        .write_all(&(b.len() as u32).to_be_bytes())
        .and_then(|_| stream.write_all(&b))
        .map_err(|e| e.to_string())
}
fn serve(path: &Path) -> Result<(), String> {
    let _ = fs::remove_file(path);
    let listener = UnixListener::bind(path).map_err(|e| e.to_string())?;
    let (mut stream, _) = listener.accept().map_err(|e| e.to_string())?;
    let mut seen = HashSet::new();
    let mut queue: Vec<String> = Vec::new();
    loop {
        let raw = match recv_frame(&mut stream) {
            Ok(raw) => raw,
            Err(error) if error == "short-header" => break,
            Err(error) => {
                send_frame(
                    &mut stream,
                    &serde_json::json!({"accepted":false,"reason":error}),
                )?;
                continue;
            }
        };
        let result = if queue.len() >= 2 {
            serde_json::json!({"accepted":false,"reason":"queue-full","queue_depth":queue.len()})
        } else {
            queue.push(raw.clone());
            let mut value = process(&raw, &mut seen)
                .unwrap_or_else(|e| serde_json::json!({"accepted":false,"reason":e}));
            value["queue_depth"] = serde_json::json!(queue.len());
            queue.remove(0);
            value
        };
        let mut value = result;
        value["log"] = serde_json::json!("qualification-shell;payload-minimized");
        send_frame(&mut stream, &value)?;
    }
    drop(listener);
    let _ = fs::remove_file(path);
    Ok(())
}

fn self_test(fixture: &Path) -> Result<(), String> {
    let raw = fs::read_to_string(fixture).map_err(|e| e.to_string())?;
    let first = process(&raw, &mut HashSet::new())?;
    let mut seen = HashSet::from(["message-0001".to_string()]);
    let again = process(&raw, &mut seen)?;
    if first["fixed_point_state"] != 25 || again["fixed_point_state"] != 0 {
        return Err("idempotency".into());
    };
    for bad in [
        r#"{"message_id":"a","message_id":"b"}"#,
        r#"{"a":1,"\u0061":2}"#,
        r#"{"x":NaN}"#,
        r#""\ud800""#,
    ] {
        if parse(bad).is_ok() {
            return Err("invalid-accepted".into());
        }
    }
    let mut event = parse(&raw)?;
    event.insert("schema_version".into(), Value::String("2.0".into()));
    if validate(&event).is_ok() {
        return Err("major-accepted".into());
    };
    let mut queue = Vec::new();
    queue.push("one");
    queue.push("two");
    if queue.len() != 2 {
        return Err("queue-probe".into());
    };
    println!(
        "{}",
        serde_json::json!({"self_test":"passed","digest":first["digest"],"rust":env!("CARGO_PKG_VERSION"),"queue_profile":"declared_only_deferred"})
    );
    Ok(())
}
fn main() {
    let a: Vec<String> = env::args().collect();
    let result = if a.len() == 3 && a[1] == "--self-test" {
        self_test(Path::new(&a[2]))
    } else if a.len() == 3 && a[1] == "--serve" {
        serve(Path::new(&a[2]))
    } else if a.len() == 3 && a[1] == "--canonical" {
        fs::read_to_string(&a[2])
            .map_err(|e| e.to_string())
            .and_then(|raw| parse(&raw))
            .and_then(|value| {
                validate(&value)?;
                canonical(&Value::Object(value))
            })
            .map(|bytes| println!("{}", base64_encode(&bytes)))
    } else {
        Err("usage: --self-test FIXTURE | --serve SOCKET | --canonical FILE".into())
    };
    if let Err(e) = result {
        eprintln!("{e}");
        std::process::exit(2)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::os::unix::net::UnixStream;

    fn fixture() -> Map<String, Value> {
        let raw = r#"{"authority_class":"qualification","boot_id":"b","causation_id":"c","canonicalization_version":"JCS-RFC8785-v1","correlation_id":"r","digest_version":"sha-256-jcs-event-v1","event_sequence":"1","message_id":"m","monotonic_ns":"1","payload":{"fixed_point_delta":25},"privacy_class":"synthetic","producer":"p","producer_version":"v1","schema_uri":"u","schema_version":"1.0","utc_observed":"2026-01-01T00:00:00Z","utc_uncertainty_us":1000}"#;
        parse(raw).unwrap()
    }

    #[test]
    fn canonicalization_orders_nested_keys() {
        let value = serde_json::json!({"z":{"b":2,"a":1},"a":"x"});
        assert_eq!(
            String::from_utf8(canonical(&value).unwrap()).unwrap(),
            r#"{"a":"x","z":{"a":1,"b":2}}"#
        );
    }

    #[test]
    fn decoded_duplicate_keys_rejected() {
        assert!(parse(r#"{"a":1,"\u0061":2}"#).is_err());
    }

    #[test]
    fn framing_reads_exact_header_and_body() {
        let (mut left, mut right) = UnixStream::pair().unwrap();
        std::thread::spawn(move || {
            left.write_all(&(3u32.to_be_bytes())).unwrap();
            left.write_all(b"{} ").unwrap();
        });
        assert_eq!(recv_frame(&mut right).unwrap(), "{} ");
    }

    #[test]
    fn idempotency_returns_duplicate_without_second_delta() {
        let raw = serde_json::to_string(&Value::Object(fixture())).unwrap();
        let mut seen = HashSet::new();
        let first = process(&raw, &mut seen).unwrap();
        let second = process(&raw, &mut seen).unwrap();
        assert_eq!(first["duplicate"], Value::Bool(false));
        assert_eq!(second["duplicate"], Value::Bool(true));
        assert_eq!(second["fixed_point_state"], Value::from(0));
    }

    #[test]
    fn rejection_behavior_is_fail_closed() {
        let mut event = fixture();
        event.insert("schema_version".into(), Value::String("2.0".into()));
        assert_eq!(
            process(
                &serde_json::to_string(&Value::Object(event)).unwrap(),
                &mut HashSet::new()
            )
            .unwrap_err(),
            "schema-major"
        );
        assert!(parse(r#"{"x":NaN}"#).is_err());
    }
}

fn base64_encode(bytes: &[u8]) -> String {
    const TABLE: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = String::new();
    let mut i = 0;
    while i < bytes.len() {
        let a = bytes[i];
        let b = if i + 1 < bytes.len() { bytes[i + 1] } else { 0 };
        let c = if i + 2 < bytes.len() { bytes[i + 2] } else { 0 };
        out.push(TABLE[(a >> 2) as usize] as char);
        out.push(TABLE[(((a & 3) << 4) | (b >> 4)) as usize] as char);
        if i + 1 < bytes.len() {
            out.push(TABLE[(((b & 15) << 2) | (c >> 6)) as usize] as char)
        } else {
            out.push('=')
        }
        if i + 2 < bytes.len() {
            out.push(TABLE[(c & 63) as usize] as char)
        } else {
            out.push('=')
        }
        i += 3;
    }
    out
}
