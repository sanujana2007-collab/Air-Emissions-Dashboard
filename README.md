# European Air Emissions Dashboard

An interactive Streamlit dashboard for exploring industrial air pollutant releases across 32 European countries (2007–2024), built using data from the European Environment Agency.
This dashboard enables users to explore emission trends, identify high-risk pollutants, compare countries, and gain actionable environmental insights through dynamic visualizations.
---

## Links

| | |
|---|---|
| **Streamlit App** | https://air-emissions-dashboard-adwkvy4kwmo4yj79lvrmjz.streamlit.app/ |


---

## What it does

The dashboard lets you filter by year range, country, risk category and individual pollutant, then explore the data across six analysis tabs:

- **Temporal Trends** — historical emissions line chart with a polynomial trend line, plus a year-on-year percentage change bar chart
- **Geographic Analysis** — choropleth map of Europe with a year slider, and a ranked bar chart of countries by total emissions
- **Risk Assessment** — scientific classification methodology panel, donut/bar charts showing emission volume by risk category, and a stacked area chart of how risk shares evolve over time
- **Country Rankings** — sortable performance scorecard with YoY change per country, plus an animated bar chart race by pollutant
- **Pollutant Analysis** — drill into any pollutant to see its trend line, KPI metrics, and top contributing countries
- **Advanced Analytics** — Pearson correlation heatmap between countries, and three CSV export options (full data, summary, pivot table)

---

## Dataset

**Source:** [European Environment Agency — E-PRTR Air Releases (National)](https://www.eea.europa.eu/en/datahub)

**File:** `F1_1_Air_Releases_National.csv`

- 13,570 records
- 32 European countries
- 68 pollutant types
- Reporting years: 2007–2024

The 68 pollutants are manually classified into four risk categories based on WHO Air Quality Guidelines (2021), IARC Monographs, the Stockholm Convention, and EU REACH/Air Quality Directives.

---

## Running locally

**Requirements:** Python 3.9+

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run Dashboard.py
```

Make sure `F1_1_Air_Releases_National.csv` is in the same directory as `Dashboard.py`.

---

## Dependencies

```
streamlit
pandas
plotly
numpy
scipy
```

Installation and setup:
```
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/Air-Emissions-Dashboard.git
cd Air-Emissions-Dashboard
2. Install dependencies
pip install -r requirements.txt
3. Run the application
streamlit run dashboard.py
```
---

## Project structure

```
├── Dashboard.py                    # Main application
├── F1_1_Air_Releases_National.csv  # Dataset (EEA)
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Use cases
Environmental analysis
Policy evaluation
Academic research
Data visualization projects

## Author
Sanujana Perera
