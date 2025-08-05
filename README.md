# Project 6: Bar Chart Race Visualization

## Introduction

This project "Bar Chart Race Visualization" showcases dynamic horizontal bar charts to visualize two datasets:

1. Taiwan's presidential election vote counts
2. COVID-19 confirmed cases across countries

We utilize `pandas` for data processing from Excel and SQLite sources, and employ `raceplotly` to create interactive, time-evolving visualizations.

Data Sources:

* `113_Election_Polling_Completion_Time.xlsx`: Taiwan polling station completion times
* `taiwan_presidential_election_2024.db`: Voting records database
* `covid_19.db`: Global COVID-19 confirmed case counts

---

## ⚙️How to Reproduce

* Install [Miniconda](https://docs.anaconda.com/miniconda)
* Create the environment from `environment.yml`:

```bash
conda env create -f environment.yml
```

* Place the following files into the `data/` folder:

  * `113_Election_Polling_Completion_Time.xlsx`
  * `taiwan_presidential_election_2024.db`
  * `covid_19.db`

* Ensure the following Python scripts are present in the project root:

  * `create_bar_chart_race_data.py`
  * `create_bar_chart_race_plot.py`

* Activate the environment and execute the script:

```bash
python create_bar_chart_race_plot.py
```

This will generate two HTML outputs:

```
bar_chart_race_votes.html
bar_chart_race_confirmed.html
```

You can view the results directly via GitHub Pages:

* [bar\_chart\_race\_votes.html](https://austinkang666.github.io/bar_chart_race/bar_chart_race_votes.html)
* [bar\_chart\_race\_confirmed.html](https://austinkang666.github.io/bar_chart_race/bar_chart_race_confirmed.html)

---

## 📁 Project Structure

```
BAR_CHART_RACE/
├── data/
│   ├── 113_Election_Polling_Completion_Time.xlsx
│   ├── taiwan_presidential_election_2024.db
│   └── covid_19.db
├── create_bar_chart_race_data.py
├── create_bar_chart_race_plot.py
├── bar_chart_race_votes.html
├── bar_chart_race_confirmed.html
├── proof_of_concept_plot.py
├── environment.yml
└── README.md
```

---

## 🧪 Environment Setup (environment.yml)

```yaml
name: bar_chart_race
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pandas=2.3.1
  - numpy=2.0.1
  - openpyxl=3.1.5
  - matplotlib==3.10.5
  - plotly=6.0.1
  - pip:
      - raceplotly==0.1.7
```

---

## 🖥️ Output Result

The final results are presented as interactive bar chart race animations:

### COVID-19 Confirmed Cases Animation

* Displays the cumulative confirmed cases across countries.
* The chart visualizes the **top 10 countries** with the highest confirmed case counts at each time step.
* Time range is filtered to dates before **2020-12-31** to showcase dynamic changes.
* To adjust the COVID-19 time range, modify the SQL query in `create_bar_chart_race_data.py`.

### Taiwan Presidential Election Votes Animation

* Visualizes the cumulative votes collected by each polling stations.
* Time is filtered to votes collected before **2024-01-13 17:30:30** to showcase dynamic changes.
* To change the vote collection cutoff time, adjust the `early_collected` filtering condition in `create_bar_chart_race_plot.py`.

Both animations are interactive, allowing you to play/pause through the timeline to observe ranking shifts.
