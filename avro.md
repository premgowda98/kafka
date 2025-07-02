# Avro Data Types: Detailed Guide with JSON Comparison and Compatibility Notes

Apache Avro defines a rich set of data types for schema-based serialization. Below is a comprehensive guide to all Avro data types, with explanations, JSON comparisons, and notes on backward/forward compatibility for each.

---

## 1. Primitive Types

| Avro Type | JSON Example | Description | Backward Compatibility | Forward Compatibility |
|-----------|-------------|-------------|-----------------------|----------------------|
| `null`    | `null`      | No value    | Adding/removing null fields is usually compatible if default is provided | Same |
| `boolean` | `true`      | True/false  | Adding/removing boolean fields is compatible with default | Same |
| `int`     | `42`        | 32-bit signed int | Changing to long is backward compatible; removing is not | Same |
| `long`    | `42`        | 64-bit signed int | Changing from int to long is backward compatible | Same |
| `float`   | `3.14`      | 32-bit float | Changing to double is backward compatible | Same |
| `double`  | `3.14`      | 64-bit float | Changing from float to double is backward compatible | Same |
| `bytes`   | `"U3dhZ2dlciByb2Nrcw=="` | Sequence of 8-bit bytes (base64 in JSON) | Changing to string is NOT compatible | Same |
| `string`  | `"hello"`  | Unicode string | Changing to bytes is NOT compatible | Same |

---

## 2. Complex Types

### a. Records
- **Avro:**
  ```json
  { "type": "record", "name": "User", "fields": [ {"name": "name", "type": "string"} ] }
  ```
- **JSON:**
  ```json
  { "name": "Alice" }
  ```
- **Compatibility:**
  - Adding a field with a default: backward compatible
  - Removing a field: forward compatible if field had a default
  - Changing field type: may break compatibility

### b. Enums
- **Avro:**
  ```json
  { "type": "enum", "name": "Suit", "symbols": ["SPADES", "HEARTS"] }
  ```
- **JSON:**
  ```json
  "SPADES"
  ```
- **Compatibility:**
  - Adding symbols: backward compatible
  - Removing symbols: not backward compatible

### c. Arrays
- **Avro:**
  ```json
  { "type": "array", "items": "string" }
  ```
- **JSON:**
  ```json
  ["a", "b", "c"]
  ```
- **Compatibility:**
  - Changing item type: not compatible
  - Adding/removing array fields: compatible with default

### d. Maps
- **Avro:**
  ```json
  { "type": "map", "values": "int" }
  ```
- **JSON:**
  ```json
  { "a": 1, "b": 2 }
  ```
- **Compatibility:**
  - Changing value type: not compatible
  - Adding/removing map fields: compatible with default

### e. Unions
- **Avro:**
  ```json
  ["null", "string"]
  ```
- **JSON:**
  ```json
  null
  "hello"
  ```
- **Compatibility:**
  - Adding a type to union: backward compatible
  - Removing a type: not backward compatible

### f. Fixed
- **Avro:**
  ```json
  { "type": "fixed", "name": "md5", "size": 16 }
  ```
- **JSON:**
  ```json
  "YWJjZGVmZ2hpamtsbW5vcA=="  // base64
  ```
- **Compatibility:**
  - Changing size: not compatible
  - Changing name: not compatible

---

## 3. Summary Table: Avro Types vs JSON

| Avro Type | JSON Example | Notes |
|-----------|-------------|-------|
| null      | null        | No value |
| boolean   | true        | true/false |
| int       | 42          | 32-bit signed |
| long      | 42          | 64-bit signed |
| float     | 3.14        | 32-bit float |
| double    | 3.14        | 64-bit float |
| bytes     | "..."       | base64 string |
| string    | "hello"     | Unicode |
| record    | { ... }     | JSON object |
| enum      | "SYMBOL"    | String value |
| array     | [ ... ]     | JSON array |
| map       | { ... }     | JSON object (string keys) |
| union     | null or value | Multiple types |
| fixed     | "..."       | base64 string |

---

## 4. Compatibility Details by Type

- **Primitive types:**
  - Widening (e.g., int → long, float → double) is backward compatible.
  - Changing between unrelated types (e.g., string ↔ bytes) is not compatible.
- **Records:**
  - Adding fields with defaults: backward compatible.
  - Removing fields: forward compatible if default exists.
- **Enums:**
  - Adding symbols: backward compatible.
  - Removing symbols: not backward compatible.
- **Arrays/Maps:**
  - Changing item/value type: not compatible.
- **Unions:**
  - Adding a type: backward compatible.
  - Removing a type: not backward compatible.
- **Fixed:**
  - Changing size or name: not compatible.

---

## 5. Example: Schema Evolution and Compatibility Modes

### 5.1 Record Type Evolution

#### v1
```json
{ "type": "record", "name": "User", "fields": [ {"name": "name", "type": "string"} ] }
```
#### v2 (Add optional field)
```json
{ "type": "record", "name": "User", "fields": [ {"name": "name", "type": "string"}, {"name": "age", "type": ["null", "int"], "default": null} ] }
```
#### v3 (Remove field)
```json
{ "type": "record", "name": "User", "fields": [ {"name": "age", "type": ["null", "int"], "default": null} ] }
```

| Compatibility Mode      | v1→v2 | v2→v1 | v2→v3 | v3→v2 | v1→v3 | v3→v1 |
|------------------------|-------|-------|-------|-------|-------|-------|
| Backward               |  ✅   |  ❌   |  ✅   |  ❌   |  ✅   |  ❌   |
| Forward                |  ❌   |  ✅   |  ❌   |  ✅   |  ❌   |  ✅   |
| Full                   |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |
| Backward Transitive    |  ✅   |  ❌   |  ✅   |  ❌   |  ✅   |  ❌   |
| Forward Transitive     |  ❌   |  ✅   |  ❌   |  ✅   |  ❌   |  ✅   |
| Full Transitive        |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |

---

### 5.2 Enum Type Evolution

#### v1
```json
{ "type": "enum", "name": "Color", "symbols": ["RED", "GREEN"] }
```
#### v2 (Add symbol)
```json
{ "type": "enum", "name": "Color", "symbols": ["RED", "GREEN", "BLUE"] }
```
#### v3 (Remove symbol)
```json
{ "type": "enum", "name": "Color", "symbols": ["RED"] }
```

| Compatibility Mode      | v1→v2 | v2→v1 | v2→v3 | v3→v2 | v1→v3 | v3→v1 |
|------------------------|-------|-------|-------|-------|-------|-------|
| Backward               |  ✅   |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |
| Forward                |  ❌   |  ✅   |  ✅   |  ❌   |  ✅   |  ❌   |
| Full                   |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |
| Backward Transitive    |  ✅   |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |
| Forward Transitive     |  ❌   |  ✅   |  ✅   |  ❌   |  ✅   |  ❌   |
| Full Transitive        |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |

---

### 5.3 Array Type Evolution

#### v1
```json
{ "type": "array", "items": "string" }
```
#### v2 (Change item type to union)
```json
{ "type": "array", "items": ["string", "null"] }
```
#### v3 (Change item type to int)
```json
{ "type": "array", "items": "int" }
```

| Compatibility Mode      | v1→v2 | v2→v1 | v2→v3 | v3→v2 | v1→v3 | v3→v1 |
|------------------------|-------|-------|-------|-------|-------|-------|
| Backward               |  ✅   |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |
| Forward                |  ❌   |  ✅   |  ✅   |  ❌   |  ✅   |  ❌   |
| Full                   |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |
| Backward Transitive    |  ✅   |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |
| Forward Transitive     |  ❌   |  ✅   |  ✅   |  ❌   |  ✅   |  ❌   |
| Full Transitive        |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |

---

### 5.4 Map Type Evolution

#### v1
```json
{ "type": "map", "values": "string" }
```
#### v2 (Change value type to union)
```json
{ "type": "map", "values": ["string", "null"] }
```
#### v3 (Change value type to int)
```json
{ "type": "map", "values": "int" }
```

| Compatibility Mode      | v1→v2 | v2→v1 | v2→v3 | v3→v2 | v1→v3 | v3→v1 |
|------------------------|-------|-------|-------|-------|-------|-------|
| Backward               |  ✅   |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |
| Forward                |  ❌   |  ✅   |  ✅   |  ❌   |  ✅   |  ❌   |
| Full                   |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |
| Backward Transitive    |  ✅   |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |
| Forward Transitive     |  ❌   |  ✅   |  ✅   |  ❌   |  ✅   |  ❌   |
| Full Transitive        |  ✅   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |

---

**References:**
- [Avro Specification: Data Types](https://avro.apache.org/docs/current/spec.html#schema_primitive)
- [Avro Schema Evolution](https://avro.apache.org/docs/current/spec.html#Schema+Resolution)
