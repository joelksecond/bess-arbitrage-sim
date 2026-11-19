# Work Log

## Day 1 — Setup (18 Nov, ~2h)

**Did:** Created project folder, virtual environment, installed libraries, pushed to GitHub.
**Learnt:** A virtual environment keeps this project's libraries separate from my main Python.
**Mistakes:** Files were empty because I hadn't saved them (0 bytes in `dir`); installed into main Python because .venv wasn't active; push failed because Windows had a different GitHub account saved.
**Next:** Day 2 — download VIC price data.

## Day 2/3 - Prices and Download, Daily price
**Did:** Downloaded price data and plotted on graph. Prices hovering around 0 with daily spikes but mostly stable. Power is cheapest around 11am–1pm (avg ~$3/MWh, driven by solar) and most expensive 5–8pm (avg ~$93/MWh). The typical midday-to-evening gap is about $[X]/MWh (median of daily gaps). Prices were negative in 2,410 intervals (~28% of the month) but only 8 intervals exceeded $300, so this month’s money comes from the daily solar pattern, not from spikes. → A battery should charge around midday and discharge in the evening peak.