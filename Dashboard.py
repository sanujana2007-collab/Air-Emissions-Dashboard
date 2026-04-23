import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
from scipy import stats

# Page configuration
st.set_page_config(
    page_title="European Air Emissions Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 
st.markdown("""
<style>
/* ===============================
   GLOBAL STYLES
================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #f5f7fa;
}

/* remove streamlit padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* ===============================
   HEADINGS - ALL WHITE
================================= */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 700 !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* ===============================
   DASHBOARD HEADER (TOP TITLE BOX)
================================= */
.dashboard-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    padding: 2.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

.dashboard-title {
    color: #ffffff !important;
    font-size: 2.4rem;
    font-weight: 800;
}

.dashboard-subtitle {
    color: rgba(255,255,255,0.9) !important;
}

/* ===============================
   SECTION HEADINGS WITH GRADIENT BACKGROUND
================================= */
.dashboard-header {
    background: transparent !important;   /* removes blue box */
    box-shadow: none !important;          /* removes glow/shadow */
    padding: 1rem 0;
    border-radius: 0;
}
.section-title {
    color: #ffffff !important;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* ===============================
   KPI / KEY PERFORMANCE INDICATORS BOXES
   NEAT WHITE CARDS WITH BORDER
================================= */

/* ================================
   KPI CARDS (WHITE + PERFECT CENTER)
================================= */

/* CARD BOX */
div[data-testid="stMetric"] {
    background: #ffffff !important;
    border-radius: 14px;
    padding: 18px 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;

    /* CENTER FIX */
    display: flex !important;
    flex-direction: column;
    align-items: center !important;
    justify-content: center !important;
}

/* FORCE INNER CONTENT CENTER */
div[data-testid="stMetric"] > div {
    display: flex !important;
    flex-direction: column;
    align-items: center !important;
    justify-content: center !important;
}

/* LABEL */
div[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    color: #6b7280 !important;
    font-weight: 600 !important;
    text-align: center !important;
    margin-bottom: 6px;
}

/* VALUE */
div[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #111827 !important;

    text-align: center !important;

    /* prevent overflow */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* DELTA */
div[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    text-align: center !important;
}

/* REMOVE DEFAULT LEFT ALIGNMENTS */
[data-testid="stMetric"] label,
[data-testid="stMetric"] p {
    text-align: center !important;
}
/* ===============================
   INSIGHT CARDS - 4 NEAT BOXES
================================= */
.insight-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.75rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-top: 5px solid;
    transition: all 0.3s ease;
    height: 100%;
    min-height: 180px;
}

.insight-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

.insight-card-success { border-top-color: #10b981; }
.insight-card-warning { border-top-color: #f59e0b; }
.insight-card-danger { border-top-color: #ef4444; }
.insight-card-info { border-top-color: #3b82f6; }

.insight-icon {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
    color: #ffffff;
}

.icon-success { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.icon-warning { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.icon-danger { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }
.icon-info { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }

.insight-title {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
}

.insight-value {
    font-size: 2.25rem;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 0.5rem;
    line-height: 1;
}

.insight-description {
    font-size: 0.875rem;
    color: #64748b;
    line-height: 1.6;
    font-weight: 500;
}

/* ===============================
   SIDEBAR (DARK)
================================= */
section[data-testid="stSidebar"] {
    background: #0f172a !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    text-shadow: none;
}

/* ===============================
   TABS
================================= */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.stTabs [data-baseweb="tab"] {
    color: #1e293b !important;
    font-weight: 600;
    padding: 10px 20px;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #f1f5f9;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: #ffffff !important;
}

/* ===============================
   TABLE HEADERS
================================= */
.dataframe th {
    background: #f1f5f9 !important;
    color: #1e293b !important;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}

/* ===============================
   INFO / WARNING BOXES
================================= */
.info-box-light {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    color: #1e40af;
    font-weight: 500;
}

.warning-box-light {
    background: #fef3c7;
    border-left: 4px solid #f59e0b;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    color: #92400e;
    font-weight: 500;
}

/* ===============================
   BUTTONS
================================= */
.stDownloadButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3);
}

/* ================================
   FIX KPI HEADING VISIBILITY
================================= */

/* KPI label (top heading inside box) */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] * {
    color: #000000 !important;   /* force black */
}

/* KPI value */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #111827 !important;
}

/* KPI delta */
div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] * {
    color: #000000 !important;
}
            
/* ================================
   FORCE KPI TEXT RESET (FINAL FIX)
================================= */

/* Reset EVERYTHING inside KPI cards */
div[data-testid="stMetric"],
div[data-testid="stMetric"] * {
    color: #000000 !important;   /* force black */
}

/* Make value slightly darker for emphasis */
div[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 700 !important;
}

/* Keep label slightly lighter (professional look) */
div[data-testid="stMetricLabel"] {
    color: #374151 !important;
    font-weight: 600 !important;
}
            
/* Tab hover + click animation */
.stTabs [data-baseweb="tab"] {
    transition: all 0.25s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# Pollutant risk classification
# Manually curated from WHO, EPA, IARC and EU treaty standards.
POLLUTANT_RISK = {
    'High Risk': [
        'Arsenic and compounds (as As)', 'Cadmium and compounds (as Cd)', 
        'Chromium and compounds (as Cr)', 'Lead and compounds (as Pb)', 
        'Mercury and compounds (as Hg)', 'Nickel and compounds (as Ni)',
        'Polychlorinated biphenyls (PCBs)', 'PCDD + PCDF (dioxins + furans) (as Teq)',
        'Hexachlorobenzene (HCB)', 'Lindane', 'Aldrin', 'Endrin', 'Chlordecone',
        'Brominated diphenylethers (PBDE)', 'Pentachlorobenzene', 'Pentachlorophenol (PCP)',
        'Benzene', 'Asbestos', 'Vinyl chloride', 'Ethylene oxide',
        'Polycyclic aromatic hydrocarbons (PAHs)', 'Anthracene', 
        'Fluoranthene', 'Naphthalene', 'Benzo(g,h,i)perylene',
        'Hydrogen cyanide (HCN)', '1,2,3,4,5,6-hexachlorocyclohexane (HCH)'
    ],
    'Medium Risk': [
        'Particulate matter (PM10)', 'Fine particulate matter (PM2.5)',
        'Nitrogen oxides (NOX)', 'Sulphur oxides (SOX)', 'Carbon monoxide (CO)',
        'Non-methane volatile organic compounds (NMVOC)', 'Ammonia (NH3)',
        'Trichloroethylene (TRI)', 'Tetrachloroethylene', 
        'Dichloromethane (DCM)', 'Trichloromethane', 'Tetrachloromethane (TCM)',
        '1,2-dichloroethane (DCE-1,2)', '1,1,1-trichloroethane (TCE-1,1,1)',
        '1,1,2,2-tetrachloroethane (TETRACHLOROETHANE-1,1,2,2)',
        'Trichlorobenzenes (TCB)', 'Toluene', 'Xylenes', 'Ethyl benzene',
        'Phenols (as total C)', 'Chlorine and inorganic compounds (as HCl)',
        'Fluorine and inorganic compounds (as HF)', 'Copper and compounds (as Cu)',
        'Zinc and compounds (as Zn)', 'Di-(2-ethyl hexyl) phthalate (DEHP)',
        'Nonylphenol and Nonylphenol ethoxylates',
        'Halogenated organic compounds (as AOX)'
    ],
    'Climate Impact': [
        'Carbon dioxide (CO2)', 'Carbon dioxide (CO2) excluding biomass',
        'Methane (CH4)', 'Nitrous oxide (N2O)',
        'Hydro-fluorocarbons (HFCS)', 'Perfluorocarbons (PFCs)', 
        'Sulphur hexafluoride (SF6)', 
        'Chlorofluorocarbons (CFCs)', 'Hydrochlorofluorocarbons (HCFCs)', 'Halons'
    ],
    'Other': [
        'Total nitrogen', 'Total organic carbon(as total C or COD/3) (TOC)',
        'Chlorides (as total Cl)', 'Fluorides (as total F)'
    ]
}

# Metadata for the risk methodology tab — criteria, health effects, regulatory basis per category
RISK_JUSTIFICATIONS = {
    'High Risk': {
        'criteria': [
            'IARC Group 1 or 2A carcinogens (Benzene, Asbestos, Vinyl chloride)',
            'Heavy metals with proven neurotoxicity and organ damage (As, Cd, Cr, Pb, Hg, Ni)',
            'Stockholm Convention Persistent Organic Pollutants (PCBs, Dioxins, HCB)',
            'WHO Air Quality Guidelines priority pollutants with no safe exposure threshold'
        ],
        'health_effects': 'Cancer, neurological damage, reproductive harm, developmental disorders',
        'regulatory_basis': 'WHO Air Quality Guidelines (2021), IARC Monographs, Stockholm Convention, EU REACH Regulation'
    },
    'Medium Risk': {
        'criteria': [
            'EPA Criteria Air Pollutants (PM10, PM2.5, NOx, SOx, CO, NMVOC)',
            'WHO-listed respiratory irritants and systemic toxins',
            'Volatile Organic Compounds with confirmed health impacts',
            'Chlorinated solvents with liver and kidney toxicity'
        ],
        'health_effects': 'Respiratory disease, cardiovascular impacts, liver/kidney damage, environmental acidification',
        'regulatory_basis': 'EU Air Quality Directive 2008/50/EC, WHO Global Air Quality Guidelines, EPA NAAQS'
    },
    'Climate Impact': {
        'criteria': [
            'Kyoto Protocol Annex A greenhouse gases (CO₂, CH₄, N₂O, HFCs, PFCs, SF₆)',
            'Montreal Protocol ozone-depleting substances (CFCs, HCFCs, Halons)',
            'Global Warming Potential (GWP) > 1 on 100-year timescale'
        ],
        'health_effects': 'Indirect health impacts through climate change: heat stress, disease vector expansion, food insecurity',
        'regulatory_basis': 'Kyoto Protocol, Paris Agreement, Montreal Protocol, EU Emissions Trading System'
    },
    'Other': {
        'criteria': [
            'Eutrophication contributors (nitrogen, phosphorus)',
            'General water quality indicators (TOC, chlorides)',
            'Localized environmental impacts without systemic toxicity'
        ],
        'health_effects': 'Eutrophication, water quality degradation, ecosystem imbalances',
        'regulatory_basis': 'EU Water Framework Directive 2000/60/EC, Nitrates Directive 91/676/EEC'
    }
}

@st.cache_data
def load_data():
   # Reads CSV, coerces numeric columns, drops bad rows, then tags each pollutant with its risk category
    try:
        df = pd.read_csv('F1_1_Air_Releases_National.csv', encoding='utf-8-sig')
        df['reportingYear'] = df['reportingYear'].astype(int)
        df['Releases'] = pd.to_numeric(df['Releases'], errors='coerce')
        df = df.dropna(subset=['Releases'])
        
        def classify_risk(pollutant):
            for category, pollutants in POLLUTANT_RISK.items():
                if pollutant in pollutants:
                    return category
            return 'Other'
        
        df['Risk_Category'] = df['Pollutant'].apply(classify_risk)
        return df
    except FileNotFoundError:
        st.error("Dataset file not found")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

def create_professional_header():
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title">European Air Emissions Dashboard</h1>
            <p class="dashboard-subtitle">
                Comprehensive Analysis of Industrial Pollutant Releases | 2007-2024 | 
                32 Countries | 68 Pollutant Types
            </p>
        </div>
    """, unsafe_allow_html=True)

def create_enhanced_metrics(df, filtered_df):
    """Create professional metric cards in neat boxes"""
    col1, col2, col3, col4, col5 = st.columns(5)
    # Year-over-year delta shown on the total emissions card
    years = sorted(filtered_df['reportingYear'].unique())
    if len(years) >= 2:
        current = filtered_df[filtered_df['reportingYear'] == years[-1]]['Releases'].sum()
        previous = filtered_df[filtered_df['reportingYear'] == years[-2]]['Releases'].sum()
        yoy = ((current - previous) / previous * 100) if previous > 0 else 0
    else:
        yoy = 0
    
    with col1:
        st.metric(
            label="Total Emissions",
            value=f"{filtered_df['Releases'].sum() / 1e9:.1f}B kg",
            delta=f"{yoy:+.1f}% YoY" if yoy != 0 else None,
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="Countries Analyzed",
            value=f"{len(filtered_df['countryName'].unique())}",
            delta=f"of {len(df['countryName'].unique())} total"
        )
    
    with col3:
        coverage = len(filtered_df['Pollutant'].unique())/len(df['Pollutant'].unique())*100
        st.metric(
            label="Pollutant Types",
            value=f"{len(filtered_df['Pollutant'].unique())}",
            delta=f"{coverage:.0f}% coverage"
        )
    
    with col4:
        year_span = filtered_df['reportingYear'].max() - filtered_df['reportingYear'].min() + 1
        st.metric(
            label="Time Period",
            value=f"{year_span} years",
            delta=f"{filtered_df['reportingYear'].min()}-{filtered_df['reportingYear'].max()}"
        )
    
    with col5:
        if filtered_df['Releases'].sum() > 0:
            hr_pct = (filtered_df[filtered_df['Risk_Category'] == 'High Risk']['Releases'].sum() / 
                     filtered_df['Releases'].sum() * 100)
        else:
            hr_pct = 0
        st.metric(
            label="High Risk Pollutants",
            value=f"{hr_pct:.1f}%",
            delta="of total volume",
            delta_color="off"
        )

def create_professional_insights(df):
    """Create 4 neat insight boxes"""
      # Overall trend
    yearly = df.groupby('reportingYear')['Releases'].sum()
    first = yearly.iloc[0]
    last = yearly.iloc[-1]
    trend_pct = ((last - first) / first * 100)
    
     # Top emitter by cumulative volume across the selected period
    top_country = df.groupby('countryName')['Releases'].sum().idxmax()
    top_value = df.groupby('countryName')['Releases'].sum().max() / 1e9
    
     # Best performer = country with largest percentage reduction
    country_trends = {}
    for country in df['countryName'].unique():
        country_data = df[df['countryName'] == country].groupby('reportingYear')['Releases'].sum()
        if len(country_data) >= 2:
            change = ((country_data.iloc[-1] - country_data.iloc[0]) / country_data.iloc[0] * 100)
            country_trends[country] = change
    
    if country_trends:
        best_country = min(country_trends, key=country_trends.get)
        best_improvement = country_trends[best_country]
    else:
        best_country = "N/A"
        best_improvement = 0
    
    # High-risk share of total volume
    if df['Releases'].sum() > 0:
        hr_pct = (df[df['Risk_Category'] == 'High Risk']['Releases'].sum() / df['Releases'].sum() * 100)
    else:
        hr_pct = 0
    
    st.markdown('<div class="section-header"><h2 class="section-title">Key Performance Indicators</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        card_type = "success" if trend_pct < -10 else ("danger" if trend_pct > 10 else "info")
        direction = "↓" if trend_pct < 0 else ("↑" if trend_pct > 0 else "→")
        
        st.markdown(f"""
            <div class="insight-card insight-card-{card_type}">
                <div class="insight-icon icon-{card_type}">{direction}</div>
                <div class="insight-title">Overall Trend</div>
                <div class="insight-value">{abs(trend_pct):.1f}%</div>
                <div class="insight-description">
                    {'Decrease' if trend_pct < 0 else 'Increase'} from {yearly.index[0]} to {yearly.index[-1]}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="insight-card insight-card-warning">
                <div class="insight-icon icon-warning">#1</div>
                <div class="insight-title">Top Emitter</div>
                <div class="insight-value">{top_value:.1f}B kg</div>
                <div class="insight-description">
                    {top_country} leads in total emissions
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if best_improvement < 0:
            st.markdown(f"""
                <div class="insight-card insight-card-success">
                    <div class="insight-icon icon-success">★</div>
                    <div class="insight-title">Best Performer</div>
                    <div class="insight-value">{abs(best_improvement):.1f}%</div>
                    <div class="insight-description">
                        {best_country} achieved largest reduction
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="insight-card insight-card-info">
                    <div class="insight-icon icon-info">i</div>
                    <div class="insight-title">Performance</div>
                    <div class="insight-value">—</div>
                    <div class="insight-description">
                        Analyzing reduction trends
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col4:
        card_type = "danger" if hr_pct > 1 else "success"
        symbol = "!" if hr_pct > 1 else "✓"
        st.markdown(f"""
            <div class="insight-card insight-card-{card_type}">
                <div class="insight-icon icon-{card_type}">{symbol}</div>
                <div class="insight-title">High Risk Exposure</div>
                <div class="insight-value">{hr_pct:.2f}%</div>
                <div class="insight-description">
                    Toxic substances share
                </div>
            </div>
        """, unsafe_allow_html=True)

def plot_emissions_trend_advanced(df):
    """Create time series with trend"""
    yearly_data = df.groupby('reportingYear')['Releases'].sum().reset_index()
    yearly_data['Releases_MT'] = yearly_data['Releases'] / 1_000_000
    
    x = yearly_data['reportingYear'].values
    y = yearly_data['Releases_MT'].values
    z = np.polyfit(x, y, 2)
    p = np.poly1d(z)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=yearly_data['reportingYear'],
        y=yearly_data['Releases_MT'],
        mode='lines+markers',
        name='Actual Emissions',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_data['reportingYear'],
        y=p(x),
        mode='lines',
        name='Trend Line',
        line=dict(color='#ef4444', width=2, dash='dash')
    ))
    
    max_year = yearly_data.loc[yearly_data['Releases_MT'].idxmax()]
    min_year = yearly_data.loc[yearly_data['Releases_MT'].idxmin()]
    
    fig.add_annotation(
        x=max_year['reportingYear'], y=max_year['Releases_MT'],
        text=f"Peak: {max_year['Releases_MT']:.0f}M kg",
        showarrow=True, arrowhead=2,
        bgcolor='rgba(239, 68, 68, 0.9)', bordercolor='#ef4444',
        font=dict(color='white', size=11, family='Inter')
    )
    
    fig.add_annotation(
        x=min_year['reportingYear'], y=min_year['Releases_MT'],
        text=f"Low: {min_year['Releases_MT']:.0f}M kg",
        showarrow=True, arrowhead=2,
        bgcolor='rgba(16, 185, 129, 0.9)', bordercolor='#10b981',
        font=dict(color='white', size=11, family='Inter')
    )
    
    fig.update_layout(
        title={
            'text': 'Historical Emissions Trend Analysis (2007-2024)',
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter'}
        },
        xaxis_title='Year',
        yaxis_title='Emissions (Million kg)',
        height=450,
        template='plotly_white',
        hovermode='x unified',
        font=dict(family='Inter'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_interactive_map_with_labels(df, year):
    """Create choropleth map"""
    year_data = df[df['reportingYear'] == year].groupby('countryName')['Releases'].sum().reset_index()
    year_data['Releases_Billion'] = year_data['Releases'] / 1e9
    
    # Plotly's choropleth is mapped by ISO-3 country codes
    country_iso = {
        'Germany': 'DEU', 'France': 'FRA', 'Italy': 'ITA', 'Spain': 'ESP', 'Poland': 'POL',
        'United Kingdom': 'GBR', 'Netherlands': 'NLD', 'Belgium': 'BEL', 'Austria': 'AUT',
        'Sweden': 'SWE', 'Denmark': 'DNK', 'Finland': 'FIN', 'Norway': 'NOR', 'Ireland': 'IRL',
        'Portugal': 'PRT', 'Greece': 'GRC', 'Czechia': 'CZE', 'Romania': 'ROU', 'Hungary': 'HUN',
        'Slovakia': 'SVK', 'Bulgaria': 'BGR', 'Croatia': 'HRV', 'Slovenia': 'SVN',
        'Lithuania': 'LTU', 'Latvia': 'LVA', 'Estonia': 'EST', 'Luxembourg': 'LUX',
        'Cyprus': 'CYP', 'Malta': 'MLT', 'Iceland': 'ISL', 'Switzerland': 'CHE', 'Serbia': 'SRB'
    }
    
    year_data['ISO'] = year_data['countryName'].map(country_iso)
    
    fig = px.choropleth(
        year_data,
        locations='ISO',
        color='Releases_Billion',
        hover_name='countryName',
        hover_data={'Releases_Billion': ':.2f', 'ISO': False},
        color_continuous_scale='Reds',
        scope='europe',
        title=f'Geographic Distribution of Emissions - {year}',
        labels={'Releases_Billion': 'Emissions (Billion kg)'}
    )
    
    fig.update_traces(marker_line_width=0.5, marker_line_color='white')
    
    fig.update_layout(
        height=600,
        font=dict(family='Inter'),
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_risk_distribution_comprehensive(df):
    """Risk distribution charts with legend"""
    risk_totals = df.groupby('Risk_Category')['Releases'].sum().reset_index()
    risk_totals['Percentage'] = (risk_totals['Releases'] / risk_totals['Releases'].sum() * 100)
    risk_totals['Releases_Billion'] = risk_totals['Releases'] / 1e9
    
#aggregation for pollutant count
    pollutant_counts = df.groupby('Risk_Category')['Pollutant'].nunique().reset_index()
    pollutant_counts.columns = ['Risk_Category', 'Count']
    
    risk_totals = risk_totals.merge(pollutant_counts, on='Risk_Category')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Emission Volume Distribution', 'Pollutant Count by Category'),
        specs=[[{'type': 'pie'}, {'type': 'bar'}]]
    )
    
    color_map = {
        'High Risk': '#ef4444',
        'Medium Risk': '#f59e0b',
        'Climate Impact': '#10b981',
        'Other': '#94a3b8'
    }
    
    colors = [color_map.get(cat, '#cccccc') for cat in risk_totals['Risk_Category']]
    
    fig.add_trace(
        go.Pie(
            labels=risk_totals['Risk_Category'],
            values=risk_totals['Releases_Billion'],
            hole=0.5,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo='percent',
            textfont=dict(size=14, family='Inter', color='white'),
            textposition='inside',
            showlegend=True
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=risk_totals['Risk_Category'],
            y=risk_totals['Count'],
            marker=dict(color=colors, line=dict(color='white', width=1)),
            text=risk_totals['Count'],
            textposition='outside',
            textfont=dict(size=16, color='#1e293b', family='Inter', weight='bold'),
            showlegend=False
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=450,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.15,
            font=dict(size=12, family='Inter')
        ),
        template='plotly_white',
        font=dict(family='Inter'),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(title_text='Risk Category', row=1, col=2)
    fig.update_yaxes(title_text='Number of Pollutants', row=1, col=2)
    
    return fig

def create_risk_classification_details():
    """Risk classification details"""
    st.markdown('<div class="section-header"><h2 class="section-title">Scientific Risk Classification Methodology</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-box-light">
            <strong>Classification Framework:</strong> All 68 pollutants are categorized using internationally 
            recognized environmental health standards from WHO, EPA, IARC, and international environmental treaties.
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "High Risk (27 pollutants)",
        "Medium Risk (27 pollutants)",
        "Climate Impact (10 pollutants)",
        "Other (4 pollutants)"
    ])
    
    with tab1:
        info = RISK_JUSTIFICATIONS['High Risk']
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"• {criterion}")
        st.markdown(f"""
            <div class="warning-box-light">
                <strong>Health Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("View all 27 High Risk pollutants"):
            cols = st.columns(2)
            pollutants = POLLUTANT_RISK['High Risk']
            mid = len(pollutants) // 2
            with cols[0]:
                for p in pollutants[:mid]:
                    st.markdown(f"• {p}")
            with cols[1]:
                for p in pollutants[mid:]:
                    st.markdown(f"• {p}")
    
    with tab2:
        info = RISK_JUSTIFICATIONS['Medium Risk']
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"• {criterion}")
        st.markdown(f"""
            <div class="info-box-light">
                <strong>Health Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("View all 27 Medium Risk pollutants"):
            cols = st.columns(2)
            pollutants = POLLUTANT_RISK['Medium Risk']
            mid = len(pollutants) // 2
            with cols[0]:
                for p in pollutants[:mid]:
                    st.markdown(f"• {p}")
            with cols[1]:
                for p in pollutants[mid:]:
                    st.markdown(f"• {p}")
    
    with tab3:
        info = RISK_JUSTIFICATIONS['Climate Impact']
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"• {criterion}")
        st.markdown(f"""
            <div class="info-box-light">
                <strong>Environmental Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("View all 10 Climate Impact pollutants"):
            for p in POLLUTANT_RISK['Climate Impact']:
                st.markdown(f"• {p}")
    
    with tab4:
        info = RISK_JUSTIFICATIONS['Other']
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"• {criterion}")
        st.markdown(f"""
            <div class="info-box-light">
                <strong>Environmental Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("View all 4 Other pollutants"):
            for p in POLLUTANT_RISK['Other']:
                st.markdown(f"• {p}")

def plot_risk_area_chart(df):
    """Stacked area chart"""
    risk_data = df.groupby(['reportingYear', 'Risk_Category'])['Releases'].sum().reset_index()
    risk_data['Releases_MT'] = risk_data['Releases'] / 1_000_000
    
    fig = px.area(
        risk_data,
        x='reportingYear',
        y='Releases_MT',
        color='Risk_Category',
        title='Emissions by Risk Category Over Time',
        labels={'reportingYear': 'Year', 'Releases_MT': 'Emissions (Million kg)'},
        color_discrete_map={
            'High Risk': '#ef4444',
            'Medium Risk': '#f59e0b',
            'Climate Impact': '#10b981',
            'Other': '#94a3b8'
        }
    )
    
    fig.update_layout(
        height=450,
        template='plotly_white',
        font=dict(family='Inter'),
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_top_polluters_race(df, pollutant, top_n=10):
    """Animated bar chart"""
    pollutant_data = df[df['Pollutant'] == pollutant]
    
    if len(pollutant_data) == 0:
        return None
    
    top_countries = (pollutant_data.groupby('countryName')['Releases']
                    .sum().nlargest(top_n).index.tolist())
    
    race_data = pollutant_data[pollutant_data['countryName'].isin(top_countries)]
    yearly = race_data.groupby(['reportingYear', 'countryName'])['Releases'].sum().reset_index()
    yearly['Releases_MT'] = yearly['Releases'] / 1_000_000
    yearly = yearly.sort_values(['reportingYear', 'Releases_MT'], ascending=[True, False])
    
    fig = px.bar(
        yearly,
        x='Releases_MT',
        y='countryName',
        animation_frame='reportingYear',
        orientation='h',
        title=f'Top {top_n} Countries - {pollutant} (Animated)',
        labels={'Releases_MT': 'Emissions (Million kg)', 'countryName': 'Country'},
        color='Releases_MT',
        color_continuous_scale=[[0, '#3b82f6'], [1, '#ef4444']],
        range_x=[0, yearly['Releases_MT'].max() * 1.1]
    )
    
    fig.update_layout(
        height=500,
        template='plotly_white',
        font=dict(family='Inter'),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_correlation_matrix(df, selected_countries):
    """Correlation matrix"""
    if len(selected_countries) < 2:
        return None
    
    pivot_data = df[df['countryName'].isin(selected_countries)].pivot_table(
        index='reportingYear',
        columns='countryName',
        values='Releases',
        aggfunc='sum'
    )
    
    corr_matrix = pivot_data.corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        title='Emission Pattern Correlation Between Countries'
    )
    
    fig.update_layout(
        height=500,
        template='plotly_white',
        font=dict(family='Inter'),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Main Application
def main():
    create_professional_header()
    
    with st.spinner('Loading emissions data...'):
        df = load_data()
        
    # Sidebar with visible dropdowns
    with st.sidebar:
        st.markdown("## Analysis Controls")
        st.markdown("---")
        
        st.markdown("### Time Period")
        year_preset = st.radio(
            "Quick selection:",
            ["Custom Range", "Last 5 Years", "Last 10 Years", "All Years"],
            label_visibility="collapsed"
        )
        
        min_year = int(df['reportingYear'].min())
        max_year = int(df['reportingYear'].max())
        
        if year_preset == "Last 5 Years":
            year_range = (max_year - 4, max_year)
        elif year_preset == "Last 10 Years":
            year_range = (max_year - 9, max_year)
        elif year_preset == "All Years":
            year_range = (min_year, max_year)
        else:
            year_range = st.slider("Year range:", min_year, max_year, (min_year, max_year))
        
        st.markdown("---")
        
        st.markdown("### Geographic Scope")
        all_countries = sorted(df['countryName'].unique())
        
        country_option = st.radio(
            "Country selection:",
            ["All Countries", "Select Specific Countries"],
            label_visibility="collapsed"
        )
        
        if country_option == "All Countries":
            selected_countries = all_countries
            st.info(f"All {len(all_countries)} countries selected")
        else:
            selected_countries = st.multiselect(
                "Choose countries:",
                options=all_countries,
                default=all_countries[:5]
            )
        
        st.markdown("---")
        
        st.markdown("### Risk Categories")
        risk_option = st.radio(
            "Risk category selection:",
            ["All Risk Categories", "Select Specific Categories"],
            label_visibility="collapsed"
        )
        
        if risk_option == "All Risk Categories":
            risk_categories = ['High Risk', 'Medium Risk', 'Climate Impact', 'Other']
            st.info("All 4 risk categories selected")
        else:
            risk_categories = st.multiselect(
                "Choose risk categories:",
                options=['High Risk', 'Medium Risk', 'Climate Impact', 'Other'],
                default=['High Risk', 'Medium Risk']
            )
        
        available_pollutants = df[df['Risk_Category'].isin(risk_categories)]['Pollutant'].unique()
        
        st.markdown("---")
 # Pollutant list updates based on the risk categories chosen above
        st.markdown(f"### Pollutant Selection")
        st.caption(f"{len(available_pollutants)} pollutants available")
        
        pollutant_option = st.radio(
            "Pollutant selection:",
            ["All Pollutants", "Select Specific Pollutants"],
            label_visibility="collapsed"
        )
        
        if pollutant_option == "All Pollutants":
            selected_pollutants = list(available_pollutants)
            st.info(f"All {len(available_pollutants)} pollutants selected")
        else:
            selected_pollutants = st.multiselect(
                "Choose pollutants:",
                options=sorted(available_pollutants),
                default=sorted(available_pollutants)[:5]
            )
    
    # Apply filters
    filtered_df = df[
        (df['reportingYear'] >= year_range[0]) &
        (df['reportingYear'] <= year_range[1]) &
        (df['countryName'].isin(selected_countries)) &
        (df['Risk_Category'].isin(risk_categories)) &
        (df['Pollutant'].isin(selected_pollutants))
    ]
    
    if len(filtered_df) == 0:
        st.error("No data matches your current filter selection. Please adjust the filters.")
        return
    
    # Executive Summary with metric boxes
    st.markdown('<div class="section-header"><h2 class="section-title">Executive Summary</h2></div>', unsafe_allow_html=True)
    create_enhanced_metrics(df, filtered_df)
    
    # Key Performance Indicators - 4 neat boxes
    st.markdown("<br>", unsafe_allow_html=True)
    create_professional_insights(filtered_df)
    
    # Tabs
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Temporal Trends",
        "Geographic Analysis",
        "Risk Assessment",
        "Country Rankings",
        "Pollutant Analysis",
        "Advanced Analytics"
    ])
    
    with tab1:
        st.markdown('<div class="section-header"><h3 class="section-title">Total Emissions Trend (2007-2024)</h3></div>', unsafe_allow_html=True)
        
        fig = plot_emissions_trend_advanced(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Year-over-Year Performance</h3></div>', unsafe_allow_html=True)
        
        yearly = filtered_df.groupby('reportingYear')['Releases'].sum().reset_index()
        yearly['YoY_%'] = yearly['Releases'].pct_change() * 100
        
        fig_yoy = go.Figure()
        colors = ['#10b981' if x < 0 else '#ef4444' for x in yearly['YoY_%']]
        
        fig_yoy.add_trace(go.Bar(
            x=yearly['reportingYear'],
            y=yearly['YoY_%'],
            marker_color=colors,
            marker_line=dict(color='white', width=1),
            text=yearly['YoY_%'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=11, family='Inter')
        ))
        
        fig_yoy.update_layout(
            title='Annual Percentage Change in Emissions',
            xaxis_title='Year',
            yaxis_title='Change (%)',
            height=400,
            template='plotly_white',
            font=dict(family='Inter'),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_yoy, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-header"><h3 class="section-title">Geographic Distribution</h3></div>', unsafe_allow_html=True)
        
        map_year = st.slider(
            "Select year for geographic visualization:",
            min_value=int(filtered_df['reportingYear'].min()),
            max_value=int(filtered_df['reportingYear'].max()),
            value=int(filtered_df['reportingYear'].max())
        )
        
        fig_map = plot_interactive_map_with_labels(filtered_df, map_year)
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Country Comparison Rankings</h3></div>', unsafe_allow_html=True)
        
        country_totals = filtered_df.groupby('countryName')['Releases'].sum().reset_index()
        country_totals['Billion'] = country_totals['Releases'] / 1e9
        country_totals = country_totals.sort_values('Billion', ascending=True)
        
        fig_countries = px.bar(
            country_totals,
            x='Billion',
            y='countryName',
            orientation='h',
            title='Total Emissions by Country (Ranked)',
            labels={'Billion': 'Total Emissions (Billion kg)', 'countryName': ''},
            color='Billion',
            color_continuous_scale=[[0, '#3b82f6'], [1, '#ef4444']]
        )
        
        fig_countries.update_layout(
            height=max(400, len(country_totals) * 25),
            template='plotly_white',
            font=dict(family='Inter'),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_countries, use_container_width=True)
    
    with tab3:
        create_risk_classification_details()
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Risk Distribution Analysis</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="warning-box-light">
                <strong>Chart Explanation:</strong> The donut chart (left) shows what percentage of total emissions 
                comes from each risk category. The bar chart (right) shows how many different pollutant types fall 
                into each category.
            </div>
        """, unsafe_allow_html=True)
        
        fig_risk = plot_risk_distribution_comprehensive(filtered_df)
        st.plotly_chart(fig_risk, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Temporal Risk Evolution</h3></div>', unsafe_allow_html=True)
        
        fig_area = plot_risk_area_chart(filtered_df)
        st.plotly_chart(fig_area, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Detailed Risk Statistics</h3></div>', unsafe_allow_html=True)
        
        risk_stats = filtered_df.groupby('Risk_Category').agg({
            'Releases': 'sum',
            'Pollutant': 'nunique',
            'countryName': 'nunique'
        }).reset_index()
        
        risk_stats.columns = ['Risk Category', 'Total (kg)', 'Pollutant Types', 'Reporting Countries']
        risk_stats['Total (Billion kg)'] = (risk_stats['Total (kg)'] / 1e9).round(2)
        risk_stats['% of Total'] = ((risk_stats['Total (kg)'] / risk_stats['Total (kg)'].sum()) * 100).round(2)
        risk_stats = risk_stats[['Risk Category', 'Total (Billion kg)', '% of Total', 'Pollutant Types', 'Reporting Countries']]
        risk_stats = risk_stats.sort_values('Total (Billion kg)', ascending=False)
        
        st.dataframe(risk_stats, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown('<div class="section-header"><h3 class="section-title">Country Performance Scorecard</h3></div>', unsafe_allow_html=True)
        
        scorecard = []
        for country in selected_countries:
            cdf = filtered_df[filtered_df['countryName'] == country]
            total = cdf['Releases'].sum() / 1e9
            pollutants = cdf['Pollutant'].nunique()
            
            years = sorted(cdf['reportingYear'].unique())
            if len(years) >= 2:
                latest = cdf[cdf['reportingYear'] == years[-1]]['Releases'].sum()
                prev = cdf[cdf['reportingYear'] == years[-2]]['Releases'].sum()
                yoy = ((latest - prev) / prev * 100) if prev > 0 else 0
            else:
                yoy = 0
            
            scorecard.append({
                'Country': country,
                'Total Emissions (B kg)': round(total, 2),
                'YoY Change (%)': round(yoy, 1),
                'Pollutant Types': pollutants,
                'Data Points': len(cdf)
            })
        
        scorecard_df = pd.DataFrame(scorecard).sort_values('Total Emissions (B kg)', ascending=False)
        st.dataframe(scorecard_df, use_container_width=True, hide_index=True)
        
        csv = scorecard_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Scorecard (CSV)",
            data=csv,
            file_name="country_scorecard.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Dynamic Country Rankings</h3></div>', unsafe_allow_html=True)
        
        
        anim_pollutant = st.selectbox(
            "Select pollutant for animated ranking:",
            options=sorted(filtered_df['Pollutant'].unique()),
            key="animation"
        )
        
        if anim_pollutant:
            fig_race = plot_top_polluters_race(filtered_df, anim_pollutant)
            if fig_race:
                st.plotly_chart(fig_race, use_container_width=True)
    
    with tab5:
        st.markdown('<div class="section-header"><h3 class="section-title">Detailed Pollutant Analysis</h3></div>', unsafe_allow_html=True)
        
        detail_pollutant = st.selectbox(
            "Select pollutant for in-depth analysis:",
            options=sorted(filtered_df['Pollutant'].unique()),
            key="detail"
        )
        
        if detail_pollutant:
            pdata = filtered_df[filtered_df['Pollutant'] == detail_pollutant]
            risk = pdata['Risk_Category'].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Risk Classification", risk)
            with col2:
                st.metric("Total Emissions", f"{pdata['Releases'].sum() / 1e9:.2f}B kg")
            with col3:
                st.metric("Reporting Countries", pdata['countryName'].nunique())
            with col4:
                st.metric("Years of Data", pdata['reportingYear'].nunique())
            
            st.markdown("---")
            
            yearly_p = pdata.groupby('reportingYear')['Releases'].sum().reset_index()
            yearly_p['MT'] = yearly_p['Releases'] / 1_000_000
            
            fig_p = px.line(
                yearly_p,
                x='reportingYear',
                y='MT',
                title=f'{detail_pollutant} - Temporal Trend',
                labels={'reportingYear': 'Year', 'MT': 'Emissions (Million kg)'},
                markers=True
            )
            
            fig_p.update_traces(line=dict(color='#3b82f6', width=3), marker=dict(size=8))
            fig_p.update_layout(height=400, template='plotly_white', font=dict(family='Inter'), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_p, use_container_width=True)
            
            st.markdown("---")
            st.markdown(f'<div class="section-header"><h3 class="section-title">Top 10 Contributing Countries - {detail_pollutant}</h3></div>', unsafe_allow_html=True)
            
            country_p = pdata.groupby('countryName')['Releases'].sum().reset_index()
            country_p['MT'] = country_p['Releases'] / 1_000_000
            country_p = country_p.sort_values('MT', ascending=False).head(10)
            
            fig_cp = px.bar(
                country_p,
                x='MT',
                y='countryName',
                orientation='h',
                labels={'MT': 'Emissions (Million kg)', 'countryName': ''},
                color='MT',
                color_continuous_scale=[[0, '#3b82f6'], [1, '#ef4444']]
            )
            
            fig_cp.update_layout(
                height=400,
                template='plotly_white',
                font=dict(family='Inter'),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_cp, use_container_width=True)
    
    with tab6:
        st.markdown('<div class="section-header"><h3 class="section-title">Cross-Country Correlation Analysis</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box-light">
                <strong></strong> This correlation matrix shows how similarly countries' 
                emissions change over time. Values close to +1 (red) mean similar patterns. Values close to 
                -1 (blue) mean opposite patterns. Values near 0 (white) mean no relationship.
            </div>
        """, unsafe_allow_html=True)
        
        if len(selected_countries) >= 2:
            fig_corr = plot_correlation_matrix(filtered_df, selected_countries)
            if fig_corr:
                st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.warning("Please select at least 2 countries to view correlation analysis")
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Data Export Center</h3></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_full = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Full Dataset",
                data=csv_full,
                file_name="filtered_emissions.csv",
                mime="text/csv"
            )
        
        with col2:
            summary = filtered_df.groupby(['countryName', 'reportingYear', 'Risk_Category']).agg({
                'Releases': 'sum',
                'Pollutant': 'count'
            }).reset_index()
            csv_summary = summary.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Summary Report",
                data=csv_summary,
                file_name="summary_report.csv",
                mime="text/csv"
            )
        
        with col3:
            pivot = filtered_df.pivot_table(
                index='countryName',
                columns='reportingYear',
                values='Releases',
                aggfunc='sum',
                fill_value=0
            )
            csv_pivot = pivot.to_csv().encode('utf-8')
            st.download_button(
                label="Pivot Table",
                data=csv_pivot,
                file_name="emissions_pivot.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Raw Data Explorer</h3></div>', unsafe_allow_html=True)
        
        if st.checkbox("Display detailed data table"):
            search = st.text_input("Search by country or pollutant name:")
            
            display = filtered_df.copy()
            if search:
                display = display[
                    display['countryName'].str.contains(search, case=False, na=False) |
                    display['Pollutant'].str.contains(search, case=False, na=False)
                ]
            
            st.caption(f"Showing {len(display):,} of {len(filtered_df):,} filtered records")
            st.dataframe(
                display[['countryName', 'reportingYear', 'Pollutant', 'Risk_Category', 'Releases']],
                use_container_width=True,
                height=400
            )

if __name__ == "__main__":
    main()
