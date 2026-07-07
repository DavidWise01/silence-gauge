# silence-gauge — the evidential weight of a negative, quantified

surfacing says it in words: *a positive is hard to explain away; a negative
means almost nothing.* This is that sentence turned into arithmetic — so you can
see how near-zero a negative is, and **break the assumption that makes it so.**

It is a companion to the boundary-crossing detectors ([forward-observers](https://github.com/DavidWise01/forward-observers),
[surfacing](https://github.com/DavidWise01/surfacing), [hearsay](https://github.com/DavidWise01/hearsay)):
they tell you whether your marker crossed a membrane; the gauge tells you **how
much to believe a silence** when it doesn't.

## The model (Bayes on canary extraction)

| symbol | meaning | typical |
|--------|---------|---------|
| `e`  | emission rate `P(surface \| ingested)` — how often a model that *was* trained on your canary re-emits it | **small** for frontier models (verbatim suppression) |
| `fp` | false-positive `P(surface \| not ingested)` — chance completion of a 128-bit withheld half | `~2^-64` ≈ 0 |
| `pi` | prior `P(ingested)` | your call |

Bayes factors (how much one observation multiplies your odds):

```
positive:  BF+ = e / fp             huge, because fp ~ 0  → a surface is decisive
negative:  BF- = (1 - e) / (1 - fp) ~ (1 - e) → with e small this is ~1: silence moves you almost nowhere
```

The asymmetry is **log-scale**, not rhetoric. In the frontier regime (`e=0.05`,
64-bit withheld half, even prior) a positive carries **~60 bits** of evidence and
drives the posterior to ~1; silence carries **less than a tenth of one bit** and
leaves the posterior sitting on your prior.

## The control you can break

The *only* reason a negative is worthless is that `e` is small — suppression.
Crank `e` toward 1 (a model that always emits what it trained on) and a negative
becomes strong evidence of **non-ingestion**. That is the honesty of the gauge:
it refuses to read silence as "clean," because the reading depends entirely on a
suppression rate **you cannot measure**. Drag the emission slider on the page and
watch silence gain meaning — the assumption is right there, breakable.

## Verify first

```bash
python selftest.py
```

Proves with no network: a positive drives the posterior to ~1 (~60 bits); under
suppression silence leaves the posterior within 0.02 of the prior (<0.1 bit); the
asymmetry is hundreds of times in bits; and silence becomes informative only as
`e` rises (monotonic), reaching a decisive non-ingestion verdict at `e=0.99`.

## Files

| File | Role |
|------|------|
| `silence.py` | the Bayes math: `bf_positive`, `bf_negative`, `posterior`, `bits`, `gauge` |
| `selftest.py` | the four claims, proven with no network |
| `index.html` | the live gauge — sliders for `e`, entropy, prior; the asymmetry drawn |

## What it is and is not

Is: an honest accounting of how much a canary-extraction result should move your
belief, given assumptions **you set and can see**.

Is not: a way to make a negative mean something it doesn't. Its whole point is
that a negative, under real suppression, means almost nothing — and it shows you
exactly what would have to be true for that to change.

---
David Lee Wise / ROOT0 / TriPod LLC · CC-BY-ND-4.0
