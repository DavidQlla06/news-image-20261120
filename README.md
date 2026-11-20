# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/DavidQlla06/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/DavidQlla06/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image for the world news of Friday 20 November 2026: Trump pushes
the Iran war decision into 2027, Cyclone Akvan makes landfall on the
Odisha coast with 300,000 people evacuated, Anthropic jumps 17% on
its first day of trading, Europe signals it is ready for Ukraine
peace talks, and NASA confirms Voyager 1 now sits one light-day from
Earth — plus GTA VI passing $1.8B in sales and engine trouble ending
Hayabusa2's asteroid landing plan.

The front page is painted by `generate.py` (Pillow, a local build
step) from the seven stories in `stories.json`, and shipped as
`entry.png` (1024x1024).

## Build the image

```sh
python3 generate.py   # reads stories.json, writes entry.png
```

## Run the entry

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
byte for byte, so the graded run is identical every time.

---

<sub>Entered on [make.fun](https://make.fun/?ref=56285tn4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
