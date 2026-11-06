# UnitLedger

UnitLedger is an offline command-line tool for exact fixed-registry measurement
conversion, compatibility checking, ordered conversion tables, and expectation-file
verification. It is a new, original, AI-assisted Python implementation with no
third-party runtime dependencies and an MIT license.

## Install and commands

Requires Python 3.11+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install .
```

```bash
unitledger convert --value 1.5 --from m --to cm
unitledger convert --value 1 --from MiB --to B --format json
unitledger convert --value 1 --from m --to ft --precision 12
unitledger units --category length
unitledger units --format json
unitledger table --value 1 --value 2.5 --value 10 --from m --to cm --to mm --to ft
unitledger check examples/conversions.json
```

`python -m unitledger` is equivalent. Convert, units, table, and check support text
and JSON output.

## Registry

- Length: `mm cm m km in ft` (base `m`)
- Mass: `mg g kg` (base `kg`)
- Duration: `us ms s min h d` (base `s`; day is exactly 86,400 seconds)
- Data size: `bit B kB MB GB KiB MiB GiB` (base `B`)

Symbols are case-sensitive. Bits/bytes and decimal/binary prefixes remain distinct;
undocumented or ambiguous spellings are rejected. Exact definitions and references
are in [docs/unit-definitions.md](docs/unit-definitions.md).

## Exact arithmetic and display

Decimal strings, including scientific notation and signed values, are parsed
directly into exact `Fraction` values without binary floating point. NaN, infinity,
commas, malformed numbers, unknown symbols, and cross-category conversions fail.
Conversion is exactly `value × source scale ÷ target scale`.

Only display formatting rounds. `--precision` means 1–100 significant decimal
digits (default 28), using `ROUND_HALF_EVEN` in a local Decimal context. The global
context remains untouched and displayed negative zero becomes `0`. JSON numeric
results are strings. Exact rational values may require a rounded decimal display.

## Tables and checks

Tables preserve input-value and destination order, validate all destinations first,
and convert each original directly rather than chaining rounded displays.

Check files have integer `schema_version: 1` and a `cases` array. Each case has
unique string `id`, decimal-string `value`, `from`, `to`, and `expected`; optional
decimal-string `tolerance` defaults to zero and is absolute in the destination unit.
The whole file is validated before execution. Exact values are compared before
display rounding, so matching rounded text cannot make a wrong expectation pass.
`examples/conversions.json` passes; `failing-conversions.json` intentionally exits 1.

## Exit codes, tests, and limitations

- `0`: successful command or all checks pass.
- `1`: one or more valid expectation cases fail.
- `2`: arguments, file, number, unit, category, or check-format error.

```bash
python -m unittest discover -s tests -v
```

Version 0.1.0 has a deliberately small fixed linear registry. It excludes absolute
temperatures, compound dimensions, project-specific units, calendars, and streaming
file conversion. See [ROADMAP.md](ROADMAP.md) for proposed work.
