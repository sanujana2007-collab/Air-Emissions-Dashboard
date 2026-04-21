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
    page_title="Air Emissions Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
#styling
st.markdown("""
<style>

/* Fix metric text contrast */
div[data-testid="stMetricValue"] {
    color: #2d3748 !important;
}

div[data-testid="stMetricLabel"] {
    color: #4a5568 !important;
}

div[data-testid="stMetricDelta"] {
    font-weight: 600;
}

/* Insight cards – force proper contrast */
.insight-card {
    background: white !important;
    color: #2d3748 !important;
}

/* Title (small grey text) */
.insight-title {
    color: #4a5568 !important;
}

/* Big value (main number) */
.insight-value {
    color: #1a202c !important;
}

/* Description text */
.insight-description {
    color: #4a5568 !important;
}

/* Make sure ALL nested text is visible */
.insight-card * {
    color: inherit !important;
}

.warning-box-light {
    background: #fffaf0;
    color: #744210 !important;
}

/* Fix text inside white cards */
.metric-card, .insight-card {
    color: #2d3748 !important;
}

/* Ensure markdown inside cards is readable */
.metric-card p, 
.insight-card p, 
.info-box-light p,
.warning-box-light p {
    color: inherit !important;
}

/* FIX SIDEBAR VISIBILITY */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #2d3748 !important;
}

/* Radio + checkbox labels */
section[data-testid="stSidebar"] label {
    color: #2d3748 !important;
}

/* Section headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #1a202c !important;
}

/* Slider text */
section[data-testid="stSidebar"] span {
    color: #2d3748 !important;
}

</style>
""", unsafe_allow_html=True)
# Pollutant risk classification
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

RISK_JUSTIFICATIONS = {
    'High Risk': {
        'description': 'Substances with severe health impacts including carcinogenicity, bioaccumulation, and acute toxicity',
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
        'description': 'Substances causing respiratory illness, environmental damage, and chronic health conditions',
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
        'description': 'Greenhouse gases and ozone-depleting substances driving climate change',
        'criteria': [
            'Kyoto Protocol Annex A greenhouse gases (CO₂, CH₄, N₂O, HFCs, PFCs, SF₆)',
            'Montreal Protocol ozone-depleting substances (CFCs, HCFCs, Halons)',
            'Global Warming Potential (GWP) > 1 on 100-year timescale'
        ],
        'health_effects': 'Indirect health impacts through climate change: heat stress, disease vector expansion, food insecurity',
        'regulatory_basis': 'Kyoto Protocol, Paris Agreement, Montreal Protocol, EU Emissions Trading System'
    },
    'Other': {
        'description': 'Nutrients and general environmental indicators with localized impacts',
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
    """Load and preprocess emissions data"""
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
        st.error(" Dataset file not found!")
        st.stop()
    except Exception as e:
        st.error(f" Error: {str(e)}")
        st.stop()

def create_professional_header():
    """Create professional dashboard header"""
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title">🌍 European Air Emissions Analytics</h1>
            <p class="dashboard-subtitle">
                Comprehensive Analysis of Industrial Pollutant Releases | 2007-2024 | 
                32 Countries | 68 Pollutant Types
            </p>
        </div>
    """, unsafe_allow_html=True)

def create_enhanced_metrics(df, filtered_df):
    """Create professional metric cards"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Calculate YoY
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
            delta=f"{len(df['countryName'].unique())} total"
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
            label="Year Range",
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
    """Create professional insight cards"""
    # Calculate insights
    yearly = df.groupby('reportingYear')['Releases'].sum()
    first = yearly.iloc[0]
    last = yearly.iloc[-1]
    trend_pct = ((last - first) / first * 100)
    
    # Top emitter
    top_country = df.groupby('countryName')['Releases'].sum().idxmax()
    top_value = df.groupby('countryName')['Releases'].sum().max() / 1e9
    
    # Best improver
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
    
    # High risk percentage
    if df['Releases'].sum() > 0:
        hr_pct = (df[df['Risk_Category'] == 'High Risk']['Releases'].sum() / df['Releases'].sum() * 100)
    else:
        hr_pct = 0
    
    # Create insight cards
    st.markdown('<div class="section-header"><h2 class="section-title">📊 Key Performance Indicators</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        card_type = "success" if trend_pct < -10 else ("danger" if trend_pct > 10 else "info")
        icon = "📉" if trend_pct < 0 else ("📈" if trend_pct > 0 else "➡️")
        
        st.markdown(f"""
            <div class="insight-card insight-card-{card_type}">
                <div class="insight-icon icon-{card_type}">{icon}</div>
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
                <div class="insight-icon icon-warning">🏭</div>
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
                    <div class="insight-icon icon-success">🌟</div>
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
                    <div class="insight-icon icon-info">📊</div>
                    <div class="insight-title">Performance Leader</div>
                    <div class="insight-value">—</div>
                    <div class="insight-description">
                        Analyzing reduction trends
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col4:
        card_type = "danger" if hr_pct > 1 else "success"
        st.markdown(f"""
            <div class="insight-card insight-card-{card_type}">
                <div class="insight-icon icon-{card_type}">{'⚠️' if hr_pct > 1 else '✅'}</div>
                <div class="insight-title">High Risk Exposure</div>
                <div class="insight-value">{hr_pct:.2f}%</div>
                <div class="insight-description">
                    Carcinogens & toxic substances share
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
        line=dict(color='#667eea', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_data['reportingYear'],
        y=p(x),
        mode='lines',
        name='Trend Line',
        line=dict(color='#f56565', width=2, dash='dash')
    ))
    
    max_year = yearly_data.loc[yearly_data['Releases_MT'].idxmax()]
    min_year = yearly_data.loc[yearly_data['Releases_MT'].idxmin()]
    
    fig.add_annotation(
        x=max_year['reportingYear'], y=max_year['Releases_MT'],
        text=f"Peak: {max_year['Releases_MT']:.0f}M kg",
        showarrow=True, arrowhead=2,
        bgcolor='rgba(245, 101, 101, 0.8)', bordercolor='#f56565',
        font=dict(color='white', size=11)
    )
    
    fig.add_annotation(
        x=min_year['reportingYear'], y=min_year['Releases_MT'],
        text=f"Low: {min_year['Releases_MT']:.0f}M kg",
        showarrow=True, arrowhead=2,
        bgcolor='rgba(72, 187, 120, 0.8)', bordercolor='#48bb78',
        font=dict(color='white', size=11)
    )
    
    fig.update_layout(
        title={
            'text': 'Total Emissions Over Time with Trend Analysis',
            'font': {'size': 20, 'color': '#2d3748', 'family': 'Arial, sans-serif'}
        },
        xaxis_title='Year',
        yaxis_title='Emissions (Million kg)',
        height=450,
        template='plotly_white',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def plot_interactive_map_with_labels(df, year):
    """Create choropleth map"""
    year_data = df[df['reportingYear'] == year].groupby('countryName')['Releases'].sum().reset_index()
    year_data['Releases_Billion'] = year_data['Releases'] / 1e9
    
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
    """Risk distribution charts"""
    risk_totals = df.groupby('Risk_Category')['Releases'].sum().reset_index()
    risk_totals['Percentage'] = (risk_totals['Releases'] / risk_totals['Releases'].sum() * 100)
    risk_totals['Releases_Billion'] = risk_totals['Releases'] / 1e9
    
    pollutant_counts = df.groupby('Risk_Category')['Pollutant'].nunique().reset_index()
    pollutant_counts.columns = ['Risk_Category', 'Count']
    
    risk_totals = risk_totals.merge(pollutant_counts, on='Risk_Category')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Emission Volume Distribution', 'Pollutant Count by Category'),
        specs=[[{'type': 'pie'}, {'type': 'bar'}]]
    )
    
    color_map = {
        'High Risk': '#f56565',
        'Medium Risk': '#ed8936',
        'Climate Impact': '#48bb78',
        'Other': '#a0aec0'
    }
    
    colors = [color_map.get(cat, '#cccccc') for cat in risk_totals['Risk_Category']]
    
    fig.add_trace(
        go.Pie(
            labels=risk_totals['Risk_Category'],
            values=risk_totals['Releases_Billion'],
            hole=0.5,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo='label+percent',
            textfont=dict(size=12)
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
            textfont=dict(size=14, color='#2d3748')
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        template='plotly_white',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(title_text='Risk Category', row=1, col=2)
    fig.update_yaxes(title_text='Number of Pollutants', row=1, col=2)
    
    return fig

def create_risk_classification_details():
    """Risk classification details"""
    st.markdown('<div class="section-header"><h2 class="section-title">📋 Scientific Risk Classification Methodology</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-box-light">
            <strong>Classification Framework:</strong> All 68 pollutants are categorized using internationally 
            recognized environmental health standards from WHO, EPA, IARC, and international environmental treaties.
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔴 High Risk (27 pollutants)",
        "🟠 Medium Risk (27 pollutants)",
        "🟢 Climate Impact (10 pollutants)",
        "⚪ Other (4 pollutants)"
    ])
    
    with tab1:
        info = RISK_JUSTIFICATIONS['High Risk']
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.markdown(f"""
            <div class="warning-box-light">
                <strong>Health Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("📋 View all 27 High Risk pollutants"):
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
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.markdown(f"""
            <div class="info-box-light">
                <strong>Health Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("📋 View all 27 Medium Risk pollutants"):
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
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.markdown(f"""
            <div class="info-box-light">
                <strong>Environmental Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("📋 View all 10 Climate Impact pollutants"):
            for p in POLLUTANT_RISK['Climate Impact']:
                st.markdown(f"• {p}")
    
    with tab4:
        info = RISK_JUSTIFICATIONS['Other']
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Classification Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.markdown(f"""
            <div class="info-box-light">
                <strong>Environmental Effects:</strong> {info['health_effects']}
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        
        with st.expander("📋 View all 4 Other pollutants"):
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
            'High Risk': '#f56565',
            'Medium Risk': '#ed8936',
            'Climate Impact': '#48bb78',
            'Other': '#a0aec0'
        }
    )
    
    fig.update_layout(
        height=450,
        template='plotly_white',
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
        color_continuous_scale=[[0, '#667eea'], [1, '#f56565']],
        range_x=[0, yearly['Releases_MT'].max() * 1.1]
    )
    
    fig.update_layout(
        height=500,
        template='plotly_white',
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
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Main Application
def main():
    # Professional header
    create_professional_header()
    
    # Load data
    with st.spinner('Loading emissions data...'):
        df = load_data()
    
   
    
    # Sidebar with professional styling
    with st.sidebar:
        st.markdown("##  Analysis Controls")
        st.markdown("---")
        
        # Year filter
        st.markdown("###  Time Period")
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
        
        # Country filter
        st.markdown("### 🌍 Geographic Scope")
        all_countries = sorted(df['countryName'].unique())
        
        if st.checkbox("Select all countries", value=True):
            selected_countries = all_countries
        else:
            selected_countries = st.multiselect(
                "Choose countries:",
                options=all_countries,
                default=all_countries[:8]
            )
        
        st.markdown("---")
        
        # Risk filter
        st.markdown("### ⚠️ Risk Categories")
        risk_categories = st.multiselect(
            "Filter by risk level:",
            options=['High Risk', 'Medium Risk', 'Climate Impact', 'Other'],
            default=['High Risk', 'Medium Risk', 'Climate Impact', 'Other']
        )
        
        # Pollutant filter
        available_pollutants = df[df['Risk_Category'].isin(risk_categories)]['Pollutant'].unique()
        
        st.markdown(f"### 🧪 Pollutant Selection")
        st.caption(f"{len(available_pollutants)} pollutants available")
        
        if st.checkbox("Select all pollutants", value=True):
            selected_pollutants = list(available_pollutants)
        else:
            selected_pollutants = st.multiselect(
                "Choose specific pollutants:",
                options=sorted(available_pollutants),
                default=sorted(available_pollutants)[:10]
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
        st.error("⚠️ No data matches your current filter selection. Please adjust the filters.")
        return
    
    # Professional metrics
    st.markdown('<div class="section-header"><h2 class="section-title">📈 Executive Summary</h2></div>', unsafe_allow_html=True)
    create_enhanced_metrics(df, filtered_df)
    
    # Professional insights
    st.markdown("<br>", unsafe_allow_html=True)
    create_professional_insights(filtered_df)
    
    # Tabs
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Temporal Trends",
        "🗺️ Geographic Analysis",
        "⚠️ Risk Assessment",
        "🏆 Country Rankings",
        "🔬 Pollutant Analysis",
        "📊 Advanced Analytics"
    ])
    
    with tab1:
        st.markdown('<div class="section-header"><h3 class="section-title">Emission Trends Over Time</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box-light">
                💡 <strong>Interpretation Guide:</strong> The blue area shows actual emission volumes, 
                while the red dashed line indicates the overall trend using polynomial regression. 
                Peaks and valleys are automatically annotated.
            </div>
        """, unsafe_allow_html=True)
        
        fig = plot_emissions_trend_advanced(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Year-over-Year Performance</h3></div>', unsafe_allow_html=True)
        
        yearly = filtered_df.groupby('reportingYear')['Releases'].sum().reset_index()
        yearly['YoY_%'] = yearly['Releases'].pct_change() * 100
        
        fig_yoy = go.Figure()
        colors = ['#48bb78' if x < 0 else '#f56565' for x in yearly['YoY_%']]
        
        fig_yoy.add_trace(go.Bar(
            x=yearly['reportingYear'],
            y=yearly['YoY_%'],
            marker_color=colors,
            marker_line=dict(color='white', width=1),
            text=yearly['YoY_%'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=11)
        ))
        
        fig_yoy.update_layout(
            title='Annual Percentage Change in Emissions',
            xaxis_title='Year',
            yaxis_title='Change (%)',
            height=400,
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_yoy, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-header"><h3 class="section-title">Geographic Distribution</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box-light">
                💡 <strong>Interactive Features:</strong> Hover over countries to see exact emission values. 
                Darker red indicates higher pollution levels. Use the year slider to analyze temporal changes.
            </div>
        """, unsafe_allow_html=True)
        
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
            color_continuous_scale=[[0, '#667eea'], [1, '#f56565']]
        )
        
        fig_countries.update_layout(
            height=max(400, len(country_totals) * 25),
            template='plotly_white',
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
                📊 <strong>Dual Perspective:</strong> The left chart shows emission volume distribution 
                (what percentage of total emissions comes from each risk category), while the right chart 
                displays the number of different pollutants in each category.
            </div>
        """, unsafe_allow_html=True)
        
        fig_risk = plot_risk_distribution_comprehensive(filtered_df)
        st.plotly_chart(fig_risk, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">Temporal Risk Evolution</h3></div>', unsafe_allow_html=True)
        
        fig_area = plot_risk_area_chart(filtered_df)
        st.plotly_chart(fig_area, use_container_width=True)
        
        # Stats table
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">📋 Detailed Risk Statistics</h3></div>', unsafe_allow_html=True)
        
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
            label=" Download Scorecard (CSV)",
            data=csv,
            file_name="country_scorecard.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">🎬 Dynamic Country Rankings</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box-light">
                💡 <strong>Animation Controls:</strong> Click play to watch how country rankings evolve over time. 
                Use pause and the slider for detailed year-by-year exploration.
            </div>
        """, unsafe_allow_html=True)
        
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
            
            fig_p.update_traces(line=dict(color='#667eea', width=3), marker=dict(size=8))
            fig_p.update_layout(height=400, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)')
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
                color_continuous_scale=[[0, '#667eea'], [1, '#f56565']]
            )
            
            fig_cp.update_layout(
                height=400,
                template='plotly_white',
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_cp, use_container_width=True)
    
    with tab6:
        st.markdown('<div class="section-header"><h3 class="section-title">🔗 Cross-Country Correlation Analysis</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box-light">
                💡 <strong>Correlation Interpretation:</strong> Values close to +1 (red) indicate countries 
                with highly synchronized emission patterns, suggesting similar industrial structures or policy coordination. 
                Values close to -1 (blue) indicate opposite trends.
            </div>
        """, unsafe_allow_html=True)
        
        if len(selected_countries) >= 2:
            fig_corr = plot_correlation_matrix(filtered_df, selected_countries)
            if fig_corr:
                st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.warning("⚠️ Please select at least 2 countries to view correlation analysis")
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">📥 Data Export Center</h3></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_full = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Full Dataset",
                data=csv_full,
                file_name="filtered_emissions.csv",
                mime="text/csv",
                help="Download complete filtered dataset"
            )
        
        with col2:
            summary = filtered_df.groupby(['countryName', 'reportingYear', 'Risk_Category']).agg({
                'Releases': 'sum',
                'Pollutant': 'count'
            }).reset_index()
            csv_summary = summary.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=" Summary Report",
                data=csv_summary,
                file_name="summary_report.csv",
                mime="text/csv",
                help="Aggregated summary by country, year, and risk"
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
                label=" Pivot Table",
                data=csv_pivot,
                file_name="emissions_pivot.csv",
                mime="text/csv",
                help="Pivot table: countries × years"
            )
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h3 class="section-title">🔍 Raw Data Explorer</h3></div>', unsafe_allow_html=True)
        
        if st.checkbox("Display detailed data table"):
            search = st.text_input("🔎 Search by country or pollutant name:")
            
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
