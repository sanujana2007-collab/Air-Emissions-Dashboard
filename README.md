# European Air Emissions Analytics Dashboard

## Project Overview
Interactive dashboard analyzing air pollutant emissions across 32 European countries (2007-2024) using EEA Industrial Emissions Directive & E-PRTR data.

**Course:** 5DATA004C Data Science Project Lifecycle  
**Institution:** University of Westminster  
**Dataset:** F1_1_Air_Releases_National.csv (13,568 records, 68 pollutants)

---

## Key Features

### 1. **Interactive Filtering System**
- Multi-select country filter with "Select All" option
- Year range slider with quick presets (Last 5/10 years, All years)
- Risk-based pollutant filtering (High Risk, Medium Risk, Climate Impact)
- Dynamic pollutant selection based on risk categories

### 2. **Advanced Visualizations** (35 marks component)

#### Trends & Forecasting Tab
- Polynomial trend line with peak/low annotations
- Year-over-year growth analysis
- Risk category stacked area chart
- Statistical metrics (CAGR, CV, Std Dev)

#### Geographic Analysis Tab
- **Interactive choropleth map** - pan, zoom, hover for country details
- Year selector slider for temporal map updates
- **Correlation matrix** - reveals emission pattern similarities between countries
- Color-coded heatmap with diverging scale

#### Risk Assessment Tab
- Risk-level pie chart with donut visualization
- High-risk pollutant rankings
- Comprehensive risk breakdown table with country counts

#### Country Rankings Tab
- **Animated bar chart race** - shows top polluters over time (highly interactive!)
- Performance scorecard with YoY changes
- Downloadable country rankings CSV
- Dynamic ranking system

#### Pollutant Deep Dive Tab
- Multi-country comparison for specific pollutants
- Top 5 emitter identification
- Peak year detection
- Latest year-over-year metrics

#### Advanced Analytics Tab
- **Two-panel decomposition** - emissions + YoY change bars
- Country-specific statistical summaries
- Top pollutant breakdowns per country
- Data explorer with search functionality
- Three export options (full data, summary, pivot table)

### 3. **Executive Dashboard Features**
- **5 KPI cards** with year-over-year deltas
- Auto-generated insights using statistical analysis
- Color-coded insight boxes (success/warning/info)
- Real-time metric calculations

### 4. **Interactivity Elements** (10 marks component)
- 6 tabbed navigation system
- 15+ interactive charts (all with zoom, pan, hover)
- Animated visualizations (bar chart race)
- Slider controls (year range, map year selector)
- Multi-select dropdowns with cascading filters
- Radio buttons for quick presets
- Checkboxes for data display toggles
- Search functionality in data explorer
- Download buttons for CSV exports (3 types)

### 5. **Design & Usability** (10 marks component)
- Custom CSS with gradient headers
- Color-coded insight boxes (green/yellow/blue)
- Consistent Plotly template (plotly_white)
- Responsive layout with columns (2, 3, 4, 5 column grids)
- Professional color schemes per chart type
- Clear labeling and units
- Descriptive tooltips and legends
- Mobile-friendly layout (wide mode)

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Download Files
Ensure you have these files in the same directory:
```
project/
├── enhanced_app.py (or app.py)
├── requirements_enhanced.txt
└── F1_1_Air_Releases_National.csv
```

### Step 2: Install Dependencies
```bash
pip install -r requirements_enhanced.txt
```

### Step 3: Run the Dashboard
```bash
streamlit run enhanced_app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

---

## GitHub & Streamlit Cloud Deployment

### 1. Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit - Air Emissions Dashboard"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file path: `enhanced_app.py`
6. Click "Deploy"

**Important:** Rename `requirements_enhanced.txt` to `requirements.txt` for Streamlit Cloud deployment.

Your public URL will be: `https://YOUR-USERNAME-air-emissions.streamlit.app`

---

## Dataset Information

**Source:** European Environment Agency (EEA)  
**Dataset:** Industrial Emissions Directive & E-PRTR  
**Time Period:** 2007-2024  
**Coverage:** 32 European countries  
**Pollutants:** 68 types  
**Records:** 13,568 entries  

### Key Columns:
- `countryName` - European country name
- `reportingYear` - Year of emission report (2007-2024)
- `Pollutant` - Type of air pollutant
- `Releases` - Emission quantity in kilograms
- `Risk_Category` - Auto-classified (High/Medium/Climate/Other)

---

## Testing Guide

### Functional Tests
1. **Filter Interaction**
   - Select/deselect countries → charts update
   - Adjust year slider → all visualizations refresh
   - Change risk categories → pollutant list updates

2. **Navigation**
   - Click each tab → content loads correctly
   - Switch between tabs → no errors

3. **Data Export**
   - Click download buttons → CSV files generate
   - Open downloaded files → data is complete

### Visual Tests
1. Hover over charts → tooltips display correct values
2. Zoom/pan on maps → responsive and smooth
3. Animated bar race → plays through all years

### Error Handling
1. Select zero countries → "No data" message displays
2. Select zero pollutants → appropriate warning shown
3. Invalid year range → system prevents selection

---

## Technical Architecture

### Libraries Used
- **Streamlit** - Web framework for dashboard
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations
- **SciPy** - Statistical analysis

### Data Processing Pipeline
1. Load CSV with UTF-8 encoding
2. Clean column names (strip whitespace)
3. Convert data types (numeric conversion)
4. Remove null values
5. Add derived columns (Risk_Category, Releases_MT)
6. Apply user-selected filters
7. Generate aggregated views per visualization

### Caching Strategy
- `@st.cache_data` on load_data() function
- Prevents reloading CSV on every interaction
- Improves performance significantly

---

## Key Insights Demonstrated

The dashboard automatically generates insights such as:
- Overall emission trends (increasing/decreasing %)
- Top emitter identification
- Best improvement leader (largest reduction %)
- High-risk pollutant percentage
- Year-over-year changes per country
- Correlation patterns between countries

---

## Report Writing Tips

### Aims & Objectives (2 marks)
Example:
> "To develop an interactive dashboard that enables environmental analysts and policymakers to:
> 1. Identify emission trends across European countries (2007-2024)
> 2. Compare pollutant types by health risk categories
> 3. Analyze geographic distribution of air pollutants
> 4. Track year-over-year changes in emission levels"

### Development Methodology (4 marks)
Recommend **Agile/Iterative**:
> "This project followed an iterative Agile approach with three sprints:
> - Sprint 1: Data loading, cleaning, basic visualizations
> - Sprint 2: Interactive filters, advanced charts, risk classification
> - Sprint 3: Polish, testing, deployment
> 
> Each sprint included development → testing → refinement cycles."

### Requirements (15 marks)

**Functional Requirements (FR):**
- FR1: Users can filter data by country, year range, and pollutant type
- FR2: Dashboard displays temporal trends via line charts
- FR3: System calculates year-over-year percentage changes
- FR4: Users can export filtered data as CSV
- FR5: Dashboard shows geographic distribution via choropleth map
- FR6: System auto-generates insights from statistical analysis
- FR7: Users can view animated bar chart race for pollutants

**Non-Functional Requirements (NFR):**
- NFR1: Dashboard loads initial view within 3 seconds
- NFR2: Visualizations respond to user interactions within 1 second
- NFR3: Interface works on Chrome, Firefox, Safari browsers
- NFR4: Dashboard is accessible via public HTTPS URL
- NFR5: Data exports complete within 5 seconds for full dataset

### Test Cases (Test Log)

| Test ID | Description | Expected Result | Status |
|---------|-------------|-----------------|--------|
| TC01 | Load dashboard with default filters | All charts display data | Pass |
| TC02 | Select single country | Charts filter to that country | Pass |
| TC03 | Adjust year range slider | All visualizations update | Pass |
| TC04 | Click "Select All Countries" | All 32 countries selected | Pass |
| TC05 | Export filtered data as CSV | File downloads successfully | Pass |
| TC06 | Play animated bar race | Animation cycles through years | Pass |
| TC07 | Hover over map region | Tooltip shows country & value | Pass |
| TC08 | Switch between tabs | Content loads without errors | Pass |
| TC09 | Select zero countries | Info message displays | Pass |
| TC10 | Search in data explorer | Results filter correctly | Pass |

---

## Marks Breakdown Mapping

### Quality of Visualisation (10 marks)
- **Appropriate:** Line charts for trends, maps for geography, bars for comparison
- **Creative:** Animated bar race, correlation matrix, risk donut chart
- **Clear:** Labeled axes, units specified, consistent color schemes

### Interactivity (10 marks)
- **Appropriate elements:** Filters, sliders, tabs, multi-select dropdowns
- **Good control:** Year presets, select all/none, search functionality
- **Clear responsiveness:** Instant chart updates, loading spinners, hover tooltips

### Design & Usability (10 marks)
- **Clear layout:** 6-tab structure, grid columns, visual hierarchy
- **Intuitive navigation:** Sidebar filters, tab labels, expandable sections
- **Consistent design:** Plotly white theme, color-coded insights, professional footer

### Functionality (5 marks)
- **Explore insights:** 6 analysis tabs, 15+ charts, statistical summaries
- **No errors:** Try-except blocks, null handling, input validation

---


## Contact & Credits

**Dataset Source:** European Environment Agency (EEA)  
