# Unit definitions and references

UnitLedger stores every scale as an exact rational relative to `m`, `kg`, `s`, or
`B`. Length uses `1 in = 0.0254 m` and `1 ft = 12 in`. Mass uses SI decimal
prefixes. Duration uses SI seconds with `min = 60 s`, `h = 3600 s`, and a fixed
`d = 86400 s`. Data size uses `1 B = 8 bit`, decimal powers of 1000, and IEC binary
powers of 1024.

Authoritative references:

- BIPM, *The International System of Units (SI Brochure), 9th edition*:
  https://www.bipm.org/en/publications/si-brochure
- NIST SP 811, *Guide for the Use of the International System of Units*:
  https://www.nist.gov/pml/special-publication-811
- NIST Handbook 44, Appendix C (exact international inch/foot relationships):
  https://www.nist.gov/pml/owm/nist-handbook-44-current-edition
- IEC, binary prefixes for quantities of digital information:
  https://www.iec.ch/prefixes-binary-multiples

Calendar months and years are deliberately absent because they are not fixed linear
durations.
