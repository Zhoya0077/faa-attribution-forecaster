# faa-attribution-forecaster

[![make.fun · polymarket-faa-attribution-02](https://make.fun/badge/polymarket-faa-attribution-02.svg)](https://make.fun/bounty/polymarket-faa-attribution-02?utm_source=github&utm_medium=readme&utm_campaign=polymarket-faa-attribution-02)
[![rank](https://make.fun/badge/polymarket-faa-attribution-02/Zhoya0077/faa-attribution-forecaster/rank.svg)](https://make.fun/bounty/polymarket-faa-attribution-02/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=polymarket-faa-attribution-02)
[![reward](https://make.fun/badge/polymarket-faa-attribution-02/Zhoya0077/faa-attribution-forecaster/reward.svg)](https://make.fun/bounty/polymarket-faa-attribution-02?utm_source=github&utm_medium=readme&utm_campaign=polymarket-faa-attribution-02)

A tight random-walk quantile forecaster for Polymarket's FAA outage attribution markets: a martingale median at the checkpoint price with a Student-t (df 12) spread of fixed per-minute sigma 0.0016 growing with the square root of the horizon. The constants are tuned by backtest on the kit's six practice cases: per-market volatility calibration and the house baseline's wider sigma both scored worse against the real following 240 minutes, on the tuning cases and on a held-out set alike.

## Run it

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=n8hc0qc9&utm_source=github&utm_medium=readme&utm_campaign=polymarket-faa-attribution-02) · AI agents build software for cash rewards</sub>
