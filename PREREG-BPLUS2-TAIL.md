# Preregistration amendment: exact tail scan from certificate-cap boundaries

The full shard 11/14 generic scans were projected too slowly under contention
from unrelated concurrent n=12 jobs.  They are stopped without output and are
`ABORTED-NO-VERDICT`.  This amendment replaces them with exact tail scans; the
B-PLUS-2 predicate is unchanged.

The fixed 4d7a checker appends `A1-BAD-SELECTION` certificates in deterministic
enumeration order and retains the first 50 per shard.  Its 50th records occur at
these graph6 strings and zero-based positions in `geng -bc -q 12`:

- shard 11: `K??FFBw}Fw^_`, index 187,883;
- shard 14: `K??Ffbo}Fw^_`, index 193,230.

All omitted records occur at or after those boundary records.  The new frozen
checker uses the same public-main enumeration engine, skips all earlier graph
indices without mathematical analysis, verifies the boundary graph6 string,
then grades every multi-cycle selection from the entire boundary graph through
the end of that shard.  Including the entire boundary graph deliberately makes
the replay/tail overlap conservative.

The 170-certificate replay covers every retained `(2,1)` case.  The two tails
must cover at least the known 14 and 12 omitted multi-cycle cases respectively;
together their union therefore covers the complete 196-case gap.  A boundary
mismatch, fewer than the expected omitted counts, any cap, any invalid
candidate, or an incomplete tail gives `ABORTED-NO-VERDICT`.  Otherwise the
decision rules of `PREREG-BPLUS2-GENERIC.md` apply.

