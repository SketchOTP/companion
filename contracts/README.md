# Phase 01 contracts

These Draft 2020-12 schemas and JSON fixtures define transport and persistence
shapes only. They do not describe a living organism, a sensor implementation,
or an emergency/care policy. Unknown fields are rejected at the service
boundary until a schema major is deliberately revised.

`fixtures/event-v1.json` is the canonical event vector used by the Rust tests
and bootstrap verification. Authoritative numeric fields are bounded integers
or fixed-point milli-units; floating point is rejected.
