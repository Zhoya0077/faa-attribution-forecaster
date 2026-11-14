"""make.fun polymarket-faa-attribution-02 entry: a tight random-walk forecaster.

For every case file in the input directory, forecast each market's Yes price
for every minute of the 240 minutes after the checkpoint, as the five
quantiles 0.05, 0.25, 0.5, 0.75, 0.95.

Model: a martingale median (the checkpoint price) with a Student-t (df = 12)
spread of fixed per-minute sigma 0.0016, growing with the square root of the
horizon, clamped to [0, 1].

Why fixed and tight, when the program is handed 72 hours of each market's
minute prices? Backtests on the kit's six practice cases (the NVIDIA CEO
event, scored against the real next-240-minutes from Polymarket's price
history, ~154k scored items) showed:

- per-market volatility calibration loses to a fixed sigma by up to 2x: a
  market's wildest past hours almost never repeat in the next four, and a
  wide forecast pays pinball loss at every quiet minute in between;
- the house baseline's fixed sigma (0.0025, Gaussian) is itself too wide:
  sigma 0.0015-0.0018 scored 7-9% better on both the tuning cases and a
  held-out set, and mild Student-t tails (df 12, unit-variance scaled)
  beat Gaussian tails at the same sigma, hedging the occasional jump.

So the whole history is used for exactly one thing: its last price.

Standard library only, no randomness: two runs on the same case write the
same bytes, and a case takes milliseconds.
"""

import glob
import json
import math
import os

LEVELS = (0.05, 0.25, 0.5, 0.75, 0.95)
SIGMA = 0.0016  # per-minute sigma, tuned on the practice cases (see docstring)

# Student-t quantiles at df = 12, scaled to unit variance: sqrt((df-2)/df).
_T12_SCALE = math.sqrt(10.0 / 12.0)
_T12 = (-1.782, -0.695, 0.0, 0.695, 1.782)
TQ = tuple(t * _T12_SCALE for t in _T12)


def forecast_market(prices, horizon):
    p0 = float(prices[-1])
    rows = []
    for h in range(1, horizon + 1):
        sigma_h = SIGMA * math.sqrt(h)
        row = []
        for t in TQ:
            v = p0 + t * sigma_h
            if v < 0.0:
                v = 0.0
            elif v > 1.0:
                v = 1.0
            row.append(round(v, 6))
        for i in range(1, len(row)):
            if row[i] < row[i - 1]:
                row[i] = row[i - 1]
        rows.append(row)
    return rows


def run(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(input_dir, "*.in"))):
        with open(path, "r", encoding="utf-8") as fh:
            case = json.load(fh)
        horizon = int(case.get("horizon_minutes", 240))
        forecasts = []
        for market in case["markets"]:
            rows = forecast_market(market["prices"], horizon)
            forecasts.append({"id": market["id"], "q": rows})
        out_name = os.path.basename(path)
        if out_name.endswith(".in"):
            out_name = out_name[:-3] + ".out"
        payload = json.dumps({"forecasts": forecasts},
                             separators=(",", ":"), sort_keys=True)
        with open(os.path.join(output_dir, out_name), "w",
                  encoding="utf-8") as fh:
            fh.write(payload)


def main():
    input_dir = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    run(input_dir, output_dir)


if __name__ == "__main__":
    main()
