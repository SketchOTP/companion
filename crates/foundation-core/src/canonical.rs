use serde_json::Value;
use sha2::{Digest, Sha256};
use std::collections::HashSet;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum CanonicalError {
    #[error("json parse error: {0}")]
    Parse(#[from] serde_json::Error),
    #[error("duplicate decoded object key: {0}")]
    DuplicateKey(String),
    #[error("non-finite or unsupported numeric value")]
    Number,
    #[error("unsupported schema major: {0}")]
    SchemaMajor(String),
    #[error("invalid unicode")]
    Unicode,
}

/// The bounded Phase 01 profile is RFC 8785-shaped but intentionally limits
/// authoritative numbers to integers. Object members are sorted by decoded
/// UTF-16 code units and strings use JSON's interoperable escaping.
pub fn canonical_event(input: &[u8]) -> Result<Vec<u8>, CanonicalError> {
    reject_duplicate_keys(input)?;
    let value: Value = serde_json::from_slice(input)?;
    validate_value(&value)?;
    let mut bytes = Vec::with_capacity(input.len());
    write_canonical(&value, &mut bytes)?;
    Ok(bytes)
}

pub fn digest_event(input: &[u8]) -> Result<String, CanonicalError> {
    let bytes = canonical_event(input)?;
    Ok(format!("{:x}", Sha256::digest(bytes)))
}

fn validate_value(value: &Value) -> Result<(), CanonicalError> {
    match value {
        Value::Object(map) => {
            for child in map.values() {
                validate_value(child)?;
            }
            if let Some(schema) = map.get("schema_major")
                && schema != &Value::from(1_u64)
            {
                return Err(CanonicalError::SchemaMajor(schema.to_string()));
            }
        }
        Value::Array(items) => {
            for child in items {
                validate_value(child)?;
            }
        }
        Value::Number(number) => {
            if number.as_i64().is_none() && number.as_u64().is_none() {
                return Err(CanonicalError::Number);
            }
        }
        Value::String(text) => {
            if text.chars().any(|c| (c as u32) > 0x10ffff) {
                return Err(CanonicalError::Unicode);
            }
        }
        Value::Null | Value::Bool(_) => {}
    }
    Ok(())
}

fn write_canonical(value: &Value, out: &mut Vec<u8>) -> Result<(), CanonicalError> {
    match value {
        Value::Null => out.extend_from_slice(b"null"),
        Value::Bool(v) => out.extend_from_slice(if *v { b"true" } else { b"false" }),
        Value::Number(n) => out.extend_from_slice(n.to_string().as_bytes()),
        Value::String(s) => out.extend_from_slice(serde_json::to_string(s)?.as_bytes()),
        Value::Array(items) => {
            out.push(b'[');
            for (index, item) in items.iter().enumerate() {
                if index > 0 {
                    out.push(b',');
                }
                write_canonical(item, out)?;
            }
            out.push(b']');
        }
        Value::Object(map) => {
            let mut entries: Vec<_> = map.iter().collect();
            entries.sort_by(|(a, _), (b, _)| a.encode_utf16().cmp(b.encode_utf16()));
            out.push(b'{');
            for (index, (key, item)) in entries.into_iter().enumerate() {
                if index > 0 {
                    out.push(b',');
                }
                out.extend_from_slice(serde_json::to_string(key)?.as_bytes());
                out.push(b':');
                write_canonical(item, out)?;
            }
            out.push(b'}');
        }
    }
    Ok(())
}

/// Reject duplicate decoded keys, including escaped/unescaped equivalents.
pub fn reject_duplicate_keys(input: &[u8]) -> Result<(), CanonicalError> {
    let mut pos = 0;
    let mut duplicate = None;
    scan_value(input, &mut pos, &mut Vec::new(), &mut duplicate);
    let _: Value = serde_json::from_slice(input)?;
    if let Some(key) = duplicate {
        return Err(CanonicalError::DuplicateKey(key));
    }
    Ok(())
}

fn skip_ws(input: &[u8], pos: &mut usize) {
    while input.get(*pos).is_some_and(|b| b" \t\r\n".contains(b)) {
        *pos += 1;
    }
}

fn string_end(input: &[u8], pos: &mut usize) -> Option<(usize, usize)> {
    skip_ws(input, pos);
    if input.get(*pos)? != &b'"' {
        return None;
    }
    let start = *pos;
    *pos += 1;
    while *pos < input.len() {
        match input[*pos] {
            b'\\' => *pos += 2,
            b'"' => {
                *pos += 1;
                return Some((start, *pos));
            }
            _ => *pos += 1,
        }
    }
    None
}

fn scan_value(
    input: &[u8],
    pos: &mut usize,
    stack: &mut Vec<HashSet<String>>,
    duplicate: &mut Option<String>,
) {
    skip_ws(input, pos);
    match input.get(*pos) {
        Some(b'{') => scan_object(input, pos, stack, duplicate),
        Some(b'[') => {
            *pos += 1;
            loop {
                skip_ws(input, pos);
                if input.get(*pos) == Some(&b']') {
                    *pos += 1;
                    break;
                }
                if *pos >= input.len() {
                    break;
                }
                scan_value(input, pos, stack, duplicate);
                skip_ws(input, pos);
                if input.get(*pos) == Some(&b',') {
                    *pos += 1;
                    continue;
                }
                if input.get(*pos) == Some(&b']') {
                    *pos += 1;
                }
                break;
            }
        }
        Some(b'"') => {
            let _ = string_end(input, pos);
        }
        Some(_) => {
            while input.get(*pos).is_some_and(|b| !b" \t\r\n,]}".contains(b)) {
                *pos += 1;
            }
        }
        None => {}
    }
}

fn scan_object(
    input: &[u8],
    pos: &mut usize,
    stack: &mut Vec<HashSet<String>>,
    duplicate: &mut Option<String>,
) {
    *pos += 1;
    stack.push(HashSet::new());
    loop {
        skip_ws(input, pos);
        if input.get(*pos) == Some(&b'}') {
            *pos += 1;
            stack.pop();
            return;
        }
        let Some((start, end)) = string_end(input, pos) else {
            stack.pop();
            return;
        };
        if let Ok(key) = serde_json::from_slice::<String>(&input[start..end]) {
            let frame = stack.last_mut().expect("object frame");
            if !frame.insert(key.clone()) && duplicate.is_none() {
                *duplicate = Some(key);
            }
        }
        skip_ws(input, pos);
        if input.get(*pos) == Some(&b':') {
            *pos += 1;
            scan_value(input, pos, stack, duplicate);
        }
        skip_ws(input, pos);
        if input.get(*pos) == Some(&b',') {
            *pos += 1;
            continue;
        }
        if input.get(*pos) == Some(&b'}') {
            *pos += 1;
            stack.pop();
            return;
        }
        stack.pop();
        return;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn digest_is_stable() {
        assert_eq!(
            digest_event(br#"{"schema_major":1,"n":2}"#).unwrap(),
            digest_event(br#"{"schema_major":1,"n":2}"#).unwrap()
        );
    }

    #[test]
    fn floats_are_rejected() {
        assert!(matches!(
            canonical_event(br#"{"schema_major":1,"n":1.5}"#),
            Err(CanonicalError::Number)
        ));
    }

    #[test]
    fn schema_major_and_trailing_invalid_input_are_rejected() {
        assert!(matches!(
            canonical_event(br#"{"schema_major":2}"#),
            Err(CanonicalError::SchemaMajor(_))
        ));
        assert!(canonical_event(br#"{"schema_major":1} trailing"#).is_err());
    }

    #[test]
    fn escaped_duplicate_is_rejected() {
        assert!(canonical_event(br#"{"schema_major":1,"a":1,"\u0061":2}"#).is_err());
    }

    #[test]
    fn nested_objects_and_non_bmp_keys_are_deterministic() {
        let input = br#"{"schema_major":1,"payload":{"z":1,"\uD834\uDF06":2,"a":3}}"#;
        let result = canonical_event(input).unwrap();
        assert!(result.windows(2).any(|pair| pair == *b"a\""));
        assert_eq!(result, canonical_event(&result).unwrap());
    }

    #[test]
    fn phase_fixture_has_expected_canonical_bytes() {
        let source = include_bytes!("../../../contracts/fixtures/event-v1.json");
        let expected = include_bytes!("../../../contracts/fixtures/event-v1.canonical.json");
        assert_eq!(
            canonical_event(source).unwrap(),
            expected.strip_suffix(b"\n").unwrap_or(expected)
        );
    }
}
