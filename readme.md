# Postit

A project focused on delivering enhanced market analytics and data-driven insights to support informed trading decisions within the World of Warcraft Classic economy.

- Extract and transform auction house item data from World of Warcraft Classic for quantitative analysis
- Visualize historical price trends and market activity to inform trading strategies
- Apply financial analytics techniques to identify market opportunities and optimize in-game investments

## Features

Currently has two scripts

- [Analyze](./src/analyze.py) uses [pola.rs](https://pola.rs/) and [plotly](https://plotly.com/) to:
  - load market data from csv files
  - show heatmap of weekly & hourly ETL coverage
  - vizualize price trends
- [ETL](./src/etl.py) uses pyautogui to:
    1. start wow classic
    1. open auction house
    1. extract market data
    1. transform and store

## Setup

```bash
mkdir history                   # here you will store csv files
mkdir assets                    # add your icons for pyautogui here
python3 -m venv .venv           # create a virtual environment
pip install -r requirements.txt # install dependencies
```
### Limitations

- World of Warcraft Classic addon `auctionator` is a must
- Recommended to run `etl.py` at least a few times a day for a week in order to find trends.
- Only tested with Orgrimmar Auction House, to change this you need to adjust the auctioneer variables in [etl.py](./src/etl.py#L31-L33)

## Roadmap

- Move away from .csv files to database solution
- More graphs for better insights

## Why postit

Postit will help you know when to post it on Auction House