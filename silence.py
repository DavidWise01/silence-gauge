#!/usr/bin/env python3
"""silence — the evidential weight of a NEGATIVE, quantified.

surfacing says it in words: "a positive is hard to explain away; a negative
means almost nothing." This is that sentence turned into arithmetic, so you can
*see* how near-zero a negative is — and break the assumption that makes it so.

The model (Bayes on canary extraction):
  e   = emission rate   P(surface | ingested)      -- how often a model that WAS
        trained on your canary actually re-emits it. LOW for frontier models,
        because they are trained to suppress verbatim regurgitation.
  fp  = false-positive  P(surface | NOT ingested)  -- chance completion of a
        128-bit withheld half ~ 2^-64. Astronomically small.
  pi  = prior           P(ingested)                -- your belief before probing.

Bayes factors (how much one observation multiplies your odds):
  positive:  BF+ = e / fp            -- huge, because fp is ~0. A surface is decisive.
  negative:  BF- = (1 - e) / (1 - fp) -- ~ (1 - e). With e small this is ~1: a
             negative multiplies your odds by ~1, i.e. it moves you almost nowhere.

The asymmetry is not rhetoric — it is log-scale. A positive can carry 60+ bits of
evidence; a negative, when e is small, carries a small fraction of one bit.

The control you can break: the ONLY reason a negative is worthless is that e is
small (suppression). Crank e toward 1 (a model that always emits what it trained
on) and a negative finally becomes strong evidence of NON-ingestion. That is why
this instrument refuses to read a negative as "clean": it depends entirely on a
suppression rate you cannot measure.
"""
from __future__ import annotations
import math


def base_rate_fp(withheld_bits: int = 64) -> float:
    """False-positive rate = chance a random completion matches the withheld half."""
    return 2.0 ** (-withheld_bits)


def bf_positive(e: float, fp: float) -> float:
    """Bayes factor of observing a SURFACE."""
    if fp <= 0:
        return math.inf if e > 0 else 1.0
    return e / fp


def bf_negative(e: float, fp: float) -> float:
    """Bayes factor of observing SILENCE (no surface)."""
    denom = 1.0 - fp
    if denom <= 0:
        return 0.0
    return (1.0 - e) / denom


def posterior(prior: float, bf: float) -> float:
    """Update a prior probability by a Bayes factor (odds form)."""
    if prior <= 0:
        return 0.0
    if prior >= 1:
        return 1.0
    if bf == math.inf:
        return 1.0
    odds = prior / (1.0 - prior)
    post_odds = odds * bf
    return post_odds / (1.0 + post_odds)


def bits(bf: float) -> float:
    """Signed bits of evidence. + supports ingested, - supports not-ingested."""
    if bf <= 0:
        return -math.inf
    if bf == math.inf:
        return math.inf
    return math.log2(bf)


def gauge(e: float, withheld_bits: int = 64, prior: float = 0.5) -> dict:
    """Full readout: what a positive is worth, what silence is worth."""
    fp = base_rate_fp(withheld_bits)
    bfp, bfn = bf_positive(e, fp), bf_negative(e, fp)
    return {
        "e": e, "fp": fp, "prior": prior, "withheld_bits": withheld_bits,
        "bf_positive": bfp, "bf_negative": bfn,
        "bits_positive": bits(bfp), "bits_negative": bits(bfn),
        "posterior_if_positive": posterior(prior, bfp),
        "posterior_if_negative": posterior(prior, bfn),
        # how far a negative moved you off your prior (0 = told you nothing):
        "negative_moved_prior_by": abs(posterior(prior, bfn) - prior),
    }
