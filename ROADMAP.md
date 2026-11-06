# UnitLedger roadmap

All work is proposed and unimplemented. Total estimate: **30 engineering hours**.

## Temperature quantities — 6 hours
Add separately modeled absolute temperatures and temperature intervals.
Acceptance: affine conversions never mix with intervals, absolute-zero validation is
documented, and exact/rounded boundary fixtures cover Celsius, kelvin, and Fahrenheit.

## Compound units and dimensional algebra — 9 hours
Parse bounded compound expressions and reduce compatible dimensions.
Acceptance: grammar is explicit, ambiguity is rejected, exponents are bounded, and
compatibility follows dimension vectors rather than string guesses.

## Project-specific registries — 6 hours
Load optional validated registries without overriding built-ins silently.
Acceptance: exact rational scales, namespace/collision rules, schema versioning, and
cycle-free base relationships are fully validated before use.

## Streaming CSV and JSONL conversion — 6 hours
Convert explicit mapped columns record by record.
Acceptance: mappings and error policies are declared, ordering/Unicode survive,
partial output is cleaned, and global numeric contexts remain untouched.

## Packaging and compatibility matrix — 3 hours
Verify Python 3.11+ across Windows, macOS, and Linux.
Acceptance: wheel/source installs and command workflows run outside the checkout,
with exact-registry regression fixtures.
