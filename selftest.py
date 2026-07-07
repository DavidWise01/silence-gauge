#!/usr/bin/env python3
"""Verify-first self-test. Proves, with no network, the four things the gauge
claims: (1) a positive is decisive; (2) under frontier suppression a negative
moves you almost nowhere; (3) the asymmetry is many orders of magnitude in bits;
(4) the negative only becomes informative as the emission rate e rises — the
assumption you can break.
"""
from __future__ import annotations
import math
from silence import gauge, bf_negative, base_rate_fp, posterior

fails = 0
def check(cond, msg):
    global fails
    print(("ok  · " if cond else "FAIL· ") + msg)
    fails += 0 if cond else 1

# frontier-ish regime: strong suppression (e=0.05), 64-bit withheld half, even prior.
g = gauge(e=0.05, withheld_bits=64, prior=0.5)

# 1. A positive is decisive: posterior -> ~1 regardless of the small emission rate.
check(g["posterior_if_positive"] > 0.9999999, f"a surface drives posterior ~1 (got {g['posterior_if_positive']:.10f})")
check(g["bits_positive"] > 55, f"a positive carries many bits of evidence (got {g['bits_positive']:.1f})")

# 2. A negative moves you almost nowhere: posterior|negative ~ prior.
check(abs(g["posterior_if_negative"] - 0.5) < 0.02, f"silence leaves posterior ~ prior (got {g['posterior_if_negative']:.4f})")
check(g["negative_moved_prior_by"] < 0.02, f"silence moved the prior by < 0.02 (got {g['negative_moved_prior_by']:.4f})")
check(abs(g["bits_negative"]) < 0.1, f"a negative carries < 0.1 bit under suppression (got {g['bits_negative']:.4f})")

# 3. The asymmetry is not rhetoric: positive evidence dwarfs negative by orders of magnitude.
check(g["bits_positive"] > 500 * abs(g["bits_negative"]), "positive evidence dwarfs negative evidence (asymmetry is log-scale)")

# 4. Break the control: as e -> 1 (a model that does NOT suppress), a negative
#    becomes strong evidence of NON-ingestion (posterior|negative -> 0).
fp = base_rate_fp(64)
weights = [abs(math.log2(bf_negative(e, fp))) for e in (0.01, 0.1, 0.5, 0.9, 0.99)]
check(all(weights[i] < weights[i+1] for i in range(len(weights)-1)),
      "a negative gains weight monotonically as emission rate e rises")
g_noSuppress = gauge(e=0.99, withheld_bits=64, prior=0.5)
check(g_noSuppress["posterior_if_negative"] < 0.02,
      f"with no suppression (e=0.99) silence IS informative: posterior -> {g_noSuppress['posterior_if_negative']:.3f}")

# 5. Sanity: posteriors are probabilities; with fp==e (no discrimination) a positive says nothing.
check(0.0 <= g["posterior_if_negative"] <= 1.0 and 0.0 <= g["posterior_if_positive"] <= 1.0, "posteriors are valid probabilities")
check(abs(posterior(0.5, 1.0) - 0.5) < 1e-12, "a Bayes factor of 1 updates nothing")

print("\n" + ("SOME CHECKS FAILED" if fails else "all silence-gauge checks passed"))
raise SystemExit(1 if fails else 0)
