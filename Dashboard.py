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

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        padding-bottom: 2rem;
    }
    .insight-box {
        background-color: #e7f3ff;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #000000;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #000000;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #000000;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Risk classification
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
        st.error("⚠️ Dataset file not found!")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        st.stop()

def create_enhanced_metrics(df, filtered_df):
    """Create summary metrics"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    years = sorted(filtered_df['reportingYear'].unique())
    if len(years) >= 2:
        total_current = filtered_df[filtered_df['reportingYear'] == years[-1]]['Releases'].sum()
        total_previous = filtered_df[filtered_df['reportingYear'] == years[-2]]['Releases'].sum()
        yoy_change = ((total_current - total_previous) / total_previous * 100) if total_previous > 0 else 0
    else:
        yoy_change = 0
    
    with col1:
        st.metric("Total Emissions", f"{filtered_df['Releases'].sum() / 1e9:.2f}B kg",
                 delta=f"{yoy_change:+.1f}% YoY" if yoy_change != 0 else None)
    
    with col2:
        st.metric("Countries", len(filtered_df['countryName'].unique()),
                 delta=f"of {len(df['countryName'].unique())}")
    
    with col3:
        st.metric("Pollutants", len(filtered_df['Pollutant'].unique()),
                 delta=f"{len(filtered_df['Pollutant'].unique())/len(df['Pollutant'].unique())*100:.0f}%")
    
    with col4:
        year_span = filtered_df['reportingYear'].max() - filtered_df['reportingYear'].min() + 1
        st.metric("Year Range", f"{filtered_df['reportingYear'].min()}-{filtered_df['reportingYear'].max()}",
                 delta=f"{year_span} years")
    
    with col5:
        if filtered_df['Releases'].sum() > 0:
            high_risk_pct = (filtered_df[filtered_df['Risk_Category'] == 'High Risk']['Releases'].sum() / 
                            filtered_df['Releases'].sum() * 100)
        else:
            high_risk_pct = 0
        st.metric("High Risk %", f"{high_risk_pct:.1f}%", delta="of total")

def plot_emissions_trend_advanced(df):
    """Time series with trend"""
    yearly_data = df.groupby('reportingYear')['Releases'].sum().reset_index()
    yearly_data['Releases_MT'] = yearly_data['Releases'] / 1_000_000
    
    x = yearly_data['reportingYear'].values
    y = yearly_data['Releases_MT'].values
    z = np.polyfit(x, y, 2)
    p = np.poly1d(z)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=yearly_data['reportingYear'], y=yearly_data['Releases_MT'],
        mode='lines+markers', name='Actual Emissions',
        line=dict(color='#1f77b4', width=3), marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_data['reportingYear'], y=p(x),
        mode='lines', name='Trend',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    max_year = yearly_data.loc[yearly_data['Releases_MT'].idxmax()]
    min_year = yearly_data.loc[yearly_data['Releases_MT'].idxmin()]
    
    fig.add_annotation(x=max_year['reportingYear'], y=max_year['Releases_MT'],
                      text=f"Peak: {max_year['Releases_MT']:.0f}M kg", showarrow=True)
    fig.add_annotation(x=min_year['reportingYear'], y=min_year['Releases_MT'],
                      text=f"Low: {min_year['Releases_MT']:.0f}M kg", showarrow=True)
    
    fig.update_layout(title='Total Emissions Over Time', xaxis_title='Year',
                     yaxis_title='Emissions (Million kg)', height=450, template='plotly_white')
    return fig

def plot_interactive_map_with_labels(df, year):
    """Choropleth map"""
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
    
    fig = px.choropleth(year_data, locations='ISO', color='Releases_Billion',
                       hover_name='countryName', hover_data={'Releases_Billion': ':.2f', 'ISO': False},
                       color_continuous_scale='Reds', scope='europe',
                       title=f'Geographic Distribution - {year}',
                       labels={'Releases_Billion': 'Emissions (B kg)'})
    
    fig.update_traces(marker_line_width=0.5, marker_line_color='white')
    fig.update_layout(height=600, geo=dict(showframe=True, showcoastlines=True,
                                           projection_type='natural earth'))
    return fig

def plot_risk_distribution_comprehensive(df):
    """Risk distribution charts"""
    risk_totals = df.groupby('Risk_Category')['Releases'].sum().reset_index()
    risk_totals['Percentage'] = (risk_totals['Releases'] / risk_totals['Releases'].sum() * 100)
    risk_totals['Releases_Billion'] = risk_totals['Releases'] / 1e9
    
    pollutant_counts = df.groupby('Risk_Category')['Pollutant'].nunique().reset_index()
    pollutant_counts.columns = ['Risk_Category', 'Count']
    risk_totals = risk_totals.merge(pollutant_counts, on='Risk_Category')
    
    fig = make_subplots(rows=1, cols=2,
                       subplot_titles=('Emission Volume', 'Pollutant Count'),
                       specs=[[{'type': 'pie'}, {'type': 'bar'}]])
    
    color_map = {
        'High Risk': '#dc3545', 'Medium Risk': '#ff7f0e',
        'Climate Impact': '#2ca02c', 'Other': '#7f7f7f'
    }
    
    colors = [color_map.get(cat, '#cccccc') for cat in risk_totals['Risk_Category']]
    
    # Donut chart - FIXED: pull labels outside to avoid overlap
    fig.add_trace(go.Pie(
        labels=risk_totals['Risk_Category'],
        values=risk_totals['Releases_Billion'],
        hole=0.4,
        marker=dict(colors=colors),
        textposition='outside',  # FIXED: moved text outside
        textinfo='label+percent',
        pull=[0.05, 0.05, 0.05, 0.05]  # FIXED: slight pull for separation
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=risk_totals['Risk_Category'], y=risk_totals['Count'],
        marker=dict(color=colors), text=risk_totals['Count'],
        textposition='outside'
    ), row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    fig.update_xaxes(title_text='Risk Category', row=1, col=2)
    fig.update_yaxes(title_text='Number of Pollutants', row=1, col=2)
    
    return fig

def create_risk_classification_details():
    """Risk classification section"""
    st.markdown("### 📊 Scientific Risk Classification")
    st.info("**Methodology**: All 68 pollutants categorized using WHO, EPA, IARC, and international treaty standards.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔴 High Risk (27)", "🟠 Medium Risk (27)", 
                                       "🟢 Climate Impact (10)", "⚪ Other (4)"])
    
    with tab1:
        info = RISK_JUSTIFICATIONS['High Risk']
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.warning(f"**Health Effects:** {info['health_effects']}")
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        with st.expander("View all 27 pollutants"):
            for p in POLLUTANT_RISK['High Risk']:
                st.markdown(f"- {p}")
    
    with tab2:
        info = RISK_JUSTIFICATIONS['Medium Risk']
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.info(f"**Health Effects:** {info['health_effects']}")
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        with st.expander("View all 27 pollutants"):
            for p in POLLUTANT_RISK['Medium Risk']:
                st.markdown(f"- {p}")
    
    with tab3:
        info = RISK_JUSTIFICATIONS['Climate Impact']
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.success(f"**Effects:** {info['health_effects']}")
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        with st.expander("View all 10 pollutants"):
            for p in POLLUTANT_RISK['Climate Impact']:
                st.markdown(f"- {p}")
    
    with tab4:
        info = RISK_JUSTIFICATIONS['Other']
        st.markdown(f"**Definition:** {info['description']}")
        st.markdown("**Criteria:**")
        for criterion in info['criteria']:
            st.markdown(f"- {criterion}")
        st.markdown(f"**Effects:** {info['health_effects']}")
        st.markdown(f"**Regulatory Basis:** {info['regulatory_basis']}")
        with st.expander("View all 4 pollutants"):
            for p in POLLUTANT_RISK['Other']:
                st.markdown(f"- {p}")

def plot_risk_area_chart(df):
    """Stacked area chart"""
    risk_data = df.groupby(['reportingYear', 'Risk_Category'])['Releases'].sum().reset_index()
    risk_data['Releases_MT'] = risk_data['Releases'] / 1_000_000
    
    fig = px.area(risk_data, x='reportingYear', y='Releases_MT', color='Risk_Category',
                 title='Emissions by Risk Category Over Time',
                 labels={'reportingYear': 'Year', 'Releases_MT': 'Emissions (M kg)'},
                 color_discrete_map={'High Risk': '#dc3545', 'Medium Risk': '#ff7f0e',
                                    'Climate Impact': '#2ca02c', 'Other': '#7f7f7f'})
    
    fig.update_layout(height=450, template='plotly_white')
    return fig

def plot_top_polluters_race(df, pollutant, top_n=10):
    """Animated bar chart - FIXED to show all years"""
    pollutant_data = df[df['Pollutant'] == pollutant]
    
    if len(pollutant_data) == 0:
        return None
    
    # Get all unique years in the dataset
    all_years = sorted(df['reportingYear'].unique())
    
    top_countries = (pollutant_data.groupby('countryName')['Releases']
                    .sum().nlargest(top_n).index.tolist())
    
    race_data = pollutant_data[pollutant_data['countryName'].isin(top_countries)]
    yearly = race_data.groupby(['reportingYear', 'countryName'])['Releases'].sum().reset_index()
    yearly['Releases_MT'] = yearly['Releases'] / 1_000_000
    
    # FIXED: Fill in missing year-country combinations with zero
    from itertools import product
    all_combinations = pd.DataFrame(list(product(all_years, top_countries)),
                                    columns=['reportingYear', 'countryName'])
    yearly = all_combinations.merge(yearly, on=['reportingYear', 'countryName'], how='left')
    yearly['Releases_MT'] = yearly['Releases_MT'].fillna(0)
    
    yearly = yearly.sort_values(['reportingYear', 'Releases_MT'], ascending=[True, False])
    
    fig = px.bar(yearly, x='Releases_MT', y='countryName',
                animation_frame='reportingYear', orientation='h',
                title=f'Top {top_n} Countries - {pollutant}',
                labels={'Releases_MT': 'Emissions (M kg)', 'countryName': 'Country'},
                color='Releases_MT', color_continuous_scale='Reds',
                range_x=[0, yearly['Releases_MT'].max() * 1.1])
    
    fig.update_layout(height=500, template='plotly_white', showlegend=False)
    return fig

def plot_correlation_matrix(df, selected_countries):
    """Correlation matrix"""
    if len(selected_countries) < 2:
        return None
    
    pivot_data = df[df['countryName'].isin(selected_countries)].pivot_table(
        index='reportingYear', columns='countryName', values='Releases', aggfunc='sum')
    
    corr_matrix = pivot_data.corr()
    
    fig = px.imshow(corr_matrix, text_auto='.2f', aspect='auto',
                   color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                   title='Emission Pattern Correlation')
    
    fig.update_layout(height=500, template='plotly_white')
    return fig

def generate_automated_insights(df):
    """Generate meaningful insights"""
    insights = []
    
    # Trend with more context
    yearly = df.groupby('reportingYear')['Releases'].sum()
    first = yearly.iloc[0]
    last = yearly.iloc[-1]
    trend_pct = ((last - first) / first * 100)
    first_year = yearly.index[0]
    last_year = yearly.index[-1]
    
    if trend_pct < -10:
        insights.append(('success', f"📉 **Environmental Progress**: Total emissions decreased by {abs(trend_pct):.1f}% from {first_year} to {last_year}, indicating effective policy implementation"))
    elif trend_pct > 10:
        insights.append(('danger', f"📈 **Concerning Trend**: Emissions increased {trend_pct:.1f}% from {first_year} to {last_year}, requiring urgent policy intervention"))
    else:
        insights.append(('warning', f"➡️ **Stable Pattern**: Emissions changed by {trend_pct:+.1f}% from {first_year} to {last_year}, suggesting limited progress"))
    
    # Top emitter with context
    top_country = df.groupby('countryName')['Releases'].sum().idxmax()
    top_value = df.groupby('countryName')['Releases'].sum().max() / 1e9
    total = df['Releases'].sum() / 1e9
    top_pct = (top_value / total * 100)
    insights.append(('warning', f"🏭 **Largest Contributor**: {top_country} accounts for {top_pct:.1f}% of total emissions ({top_value:.1f}B kg)"))
    
    # Best improver with specific data
    country_trends = {}
    for country in df['countryName'].unique():
        country_data = df[df['countryName'] == country].groupby('reportingYear')['Releases'].sum()
        if len(country_data) >= 2:
            change_pct = ((country_data.iloc[-1] - country_data.iloc[0]) / country_data.iloc[0] * 100)
            country_trends[country] = change_pct
    
    if country_trends:
        best_country = min(country_trends, key=country_trends.get)
        best_improvement = country_trends[best_country]
        if best_improvement < 0:
            insights.append(('success', f"🌟 **Best Performer**: {best_country} achieved {abs(best_improvement):.1f}% emission reduction, demonstrating successful environmental policies"))
    
    # High risk with actual numbers
    if df['Releases'].sum() > 0:
        hr_total = df[df['Risk_Category'] == 'High Risk']['Releases'].sum() / 1e9
        hr_pct = (df[df['Risk_Category'] == 'High Risk']['Releases'].sum() / df['Releases'].sum() * 100)
        if hr_pct > 1:
            insights.append(('danger', f"⚠️ **Health Alert**: {hr_pct:.2f}% of emissions ({hr_total:.2f}B kg) are from High Risk pollutants (carcinogens, heavy metals, POPs)"))
        else:
            insights.append(('success', f"✅ **Positive Risk Profile**: Only {hr_pct:.2f}% from High Risk pollutants, majority are climate gases"))
    
    return insights

# Main Application
def main():
    st.markdown('<p class="main-header">🌍 European Air Emissions Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive Analysis of Industrial Air Pollutant Releases (2007-2024)</p>', unsafe_allow_html=True)
    
    # Load data - NO GREEN BOX SHOWN
    df = load_data()
    
    # Sidebar - IMPROVED FILTERS
    st.sidebar.header("🎛️ Interactive Filters")
    st.sidebar.markdown("---")
    
    # Year filter
    st.sidebar.subheader("📅 Year Selection")
    year_preset = st.sidebar.radio("Quick Presets:", 
                                   ["Custom Range", "Last 5 Years", "Last 10 Years", "All Years (2007-2024)"])
    
    min_year = int(df['reportingYear'].min())
    max_year = int(df['reportingYear'].max())
    
    if year_preset == "Last 5 Years":
        year_range = (max_year - 4, max_year)
    elif year_preset == "Last 10 Years":
        year_range = (max_year - 9, max_year)
    elif year_preset == "All Years (2007-2024)":
        year_range = (min_year, max_year)
    else:
        year_range = st.sidebar.slider("Custom Year Range:", min_year, max_year, (min_year, max_year))
    
    st.sidebar.markdown(f"**Selected: {year_range[0]}-{year_range[1]}** ({year_range[1] - year_range[0] + 1} years)")
    st.sidebar.markdown("---")
    
    # Country filter - MORE VISIBLE
    st.sidebar.subheader("🌍 Countries")
    all_countries = sorted(df['countryName'].unique())
    
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        if st.button("✅ Select All", use_container_width=True):
            selected_countries = all_countries
    with col_b:
        if st.button("❌ Clear All", use_container_width=True):
            selected_countries = []
    
    selected_countries = st.sidebar.multiselect(
        f"Choose countries ({len(all_countries)} available):",
        options=all_countries,
        default=all_countries,  # Show all by default
        help="Select one or more countries to analyze"
    )
    
    st.sidebar.markdown(f"**Selected: {len(selected_countries)} countries**")
    st.sidebar.markdown("---")
    
    # Risk filter - MORE DETAILED
    st.sidebar.subheader("⚠️ Risk Categories")
    st.sidebar.markdown("*Based on WHO/EPA/IARC standards*")
    
    risk_selection = st.sidebar.multiselect(
        "Select risk levels:",
        options=['High Risk (27 pollutants)', 'Medium Risk (27 pollutants)', 
                'Climate Impact (10 pollutants)', 'Other (4 pollutants)'],
        default=['High Risk (27 pollutants)', 'Medium Risk (27 pollutants)', 
                'Climate Impact (10 pollutants)', 'Other (4 pollutants)'],
        help="High Risk: carcinogens, heavy metals, POPs\nMedium Risk: criteria air pollutants\nClimate Impact: greenhouse gases"
    )
    
    # Clean risk category names
    risk_categories = [r.split(' (')[0] for r in risk_selection]
    
    st.sidebar.markdown(f"**Selected: {len(risk_categories)} categories**")
    st.sidebar.markdown("---")
    
    # Pollutant filter - MORE INFORMATIVE
    st.sidebar.subheader("🔬 Pollutants")
    available_pollutants = df[df['Risk_Category'].isin(risk_categories)]['Pollutant'].unique()
    
    col_c, col_d = st.sidebar.columns(2)
    with col_c:
        if st.button("✅ All", key="all_poll", use_container_width=True):
            selected_pollutants = sorted(available_pollutants)
    with col_d:
        if st.button("❌ None", key="none_poll", use_container_width=True):
            selected_pollutants = []
    
    selected_pollutants = st.sidebar.multiselect(
        f"Select specific pollutants ({len(available_pollutants)} available):",
        options=sorted(available_pollutants),
        default=sorted(available_pollutants),  # Show all by default
        help="Filter by specific pollutant types"
    )
    
    st.sidebar.markdown(f"**Selected: {len(selected_pollutants)} pollutants**")
    
    # Apply filters
    filtered_df = df[
        (df['reportingYear'] >= year_range[0]) &
        (df['reportingYear'] <= year_range[1]) &
        (df['countryName'].isin(selected_countries)) &
        (df['Risk_Category'].isin(risk_categories)) &
        (df['Pollutant'].isin(selected_pollutants))
    ]
    
    if len(filtered_df) == 0:
        st.error("⚠️ No data matches your filter criteria. Please adjust filters.")
        return
    
    # Metrics
    st.markdown("---")
    create_enhanced_metrics(df, filtered_df)
    st.markdown("---")
    
    # IMPROVED KEY INSIGHTS
    st.subheader("🔍 Key Insights & Analysis")
    insights = generate_automated_insights(filtered_df)
    
    for insight_type, message in insights:
        if insight_type == 'success':
            st.markdown(f'<div class="success-box">{message}</div>', unsafe_allow_html=True)
        elif insight_type == 'warning':
            st.markdown(f'<div class="warning-box">{message}</div>', unsafe_allow_html=True)
        elif insight_type == 'danger':
            st.markdown(f'<div class="danger-box">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="insight-box">{message}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Trends", "🗺️ Geography", "⚠️ Risk", "🏆 Rankings", "🔬 Pollutants", "📊 Analytics"
    ])
    
    with tab1:
        st.subheader("Temporal Trends")
        st.info("💡 Trend line uses polynomial regression. Peaks/lows auto-annotated.")
        
        fig = plot_emissions_trend_advanced(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Year-over-Year Changes")
        
        yearly = filtered_df.groupby('reportingYear')['Releases'].sum().reset_index()
        yearly['YoY_%'] = yearly['Releases'].pct_change() * 100
        
        fig_yoy = go.Figure()
        colors = ['green' if x < 0 else 'red' for x in yearly['YoY_%']]
        
        fig_yoy.add_trace(go.Bar(
            x=yearly['reportingYear'], y=yearly['YoY_%'],
            marker_color=colors, text=yearly['YoY_%'].round(1),
            textposition='outside'
        ))
        
        fig_yoy.update_layout(title='Year-over-Year Changes', xaxis_title='Year',
                             yaxis_title='Change (%)', height=400, template='plotly_white')
        
        st.plotly_chart(fig_yoy, use_container_width=True)
    
    with tab2:
        st.subheader("Geographic Distribution")
        st.info("💡 Hover over countries for values. ISO codes shown on map.")
        
        map_year = st.slider("Select Year:", min_value=int(filtered_df['reportingYear'].min()),
                            max_value=int(filtered_df['reportingYear'].max()),
                            value=int(filtered_df['reportingYear'].max()))
        
        fig_map = plot_interactive_map_with_labels(filtered_df, map_year)
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Country Comparison")
        
        country_totals = filtered_df.groupby('countryName')['Releases'].sum().reset_index()
        country_totals['Billion'] = country_totals['Releases'] / 1e9
        country_totals = country_totals.sort_values('Billion', ascending=True)
        
        fig_countries = px.bar(country_totals, x='Billion', y='countryName', orientation='h',
                              title='Total Emissions by Country',
                              labels={'Billion': 'Emissions (B kg)'},
                              color='Billion', color_continuous_scale='Reds')
        
        fig_countries.update_layout(height=max(400, len(country_totals) * 25),
                                   template='plotly_white', showlegend=False)
        
        st.plotly_chart(fig_countries, use_container_width=True)
    
    with tab3:
        st.subheader("Risk-Based Analysis")
        
        create_risk_classification_details()
        
        st.markdown("---")
        st.subheader("Distribution by Risk")
        st.warning("💡 Left: emission volume. Right: pollutant count.")
        
        fig_risk = plot_risk_distribution_comprehensive(filtered_df)
        st.plotly_chart(fig_risk, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Risk Trends Over Time")
        st.info("💡 Stacked area shows evolution by risk category.")
        
        fig_area = plot_risk_area_chart(filtered_df)
        st.plotly_chart(fig_area, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📋 Risk Statistics")
        
        risk_stats = filtered_df.groupby('Risk_Category').agg({
            'Releases': 'sum', 'Pollutant': 'nunique', 'countryName': 'nunique'
        }).reset_index()
        
        risk_stats.columns = ['Risk', 'Total (kg)', 'Pollutants', 'Countries']
        risk_stats['Total (B kg)'] = risk_stats['Total (kg)'] / 1e9
        risk_stats['% of Total'] = (risk_stats['Total (kg)'] / risk_stats['Total (kg)'].sum() * 100).round(2)
        risk_stats = risk_stats[['Risk', 'Total (B kg)', '% of Total', 'Pollutants', 'Countries']]
        risk_stats = risk_stats.sort_values('Total (B kg)', ascending=False)
        
        st.dataframe(risk_stats, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("Country Rankings")
        st.info("💡 Comprehensive scorecard with YoY changes.")
        
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
                'Country': country, 'Total (B kg)': round(total, 2),
                'YoY %': round(yoy, 1), 'Pollutants': pollutants
            })
        
        scorecard_df = pd.DataFrame(scorecard).sort_values('Total (B kg)', ascending=False)
        st.dataframe(scorecard_df, use_container_width=True, hide_index=True)
        
        csv = scorecard_df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "scorecard.csv", "text/csv")
        
        st.markdown("---")
        st.subheader("🎬 Animated Rankings")
        st.warning("💡 Play to see rankings change over time.")
        
        anim_pollutant = st.selectbox("Select pollutant:",
                                     options=sorted(filtered_df['Pollutant'].unique()))
        
        if anim_pollutant:
            fig_race = plot_top_polluters_race(filtered_df, anim_pollutant)
            if fig_race:
                st.plotly_chart(fig_race, use_container_width=True)
    
    with tab5:
        st.subheader("Pollutant Deep Dive")
        st.info("💡 Detailed analysis of specific pollutants.")
        
        detail_pollutant = st.selectbox("Select pollutant:",
                                       options=sorted(filtered_df['Pollutant'].unique()),
                                       key="detail")
        
        if detail_pollutant:
            pdata = filtered_df[filtered_df['Pollutant'] == detail_pollutant]
            risk = pdata['Risk_Category'].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Risk", risk)
            with col2:
                st.metric("Total", f"{pdata['Releases'].sum() / 1e9:.2f}B kg")
            with col3:
                st.metric("Countries", pdata['countryName'].nunique())
            with col4:
                st.metric("Years", pdata['reportingYear'].nunique())
            
            st.markdown("---")
            
            yearly_p = pdata.groupby('reportingYear')['Releases'].sum().reset_index()
            yearly_p['MT'] = yearly_p['Releases'] / 1_000_000
            
            fig_p = px.line(yearly_p, x='reportingYear', y='MT',
                          title=f'{detail_pollutant} - Trend',
                          labels={'reportingYear': 'Year', 'MT': 'Emissions (M kg)'},
                          markers=True)
            fig_p.update_layout(height=400, template='plotly_white')
            st.plotly_chart(fig_p, use_container_width=True)
            
            st.markdown("---")
            st.subheader(f"Top 10 Countries - {detail_pollutant}")
            
            country_p = pdata.groupby('countryName')['Releases'].sum().reset_index()
            country_p['MT'] = country_p['Releases'] / 1_000_000
            country_p = country_p.sort_values('MT', ascending=False).head(10)
            
            fig_cp = px.bar(country_p, x='MT', y='countryName', orientation='h',
                          title=f'Top Contributors',
                          labels={'MT': 'Emissions (M kg)'},
                          color='MT', color_continuous_scale='Reds')
            fig_cp.update_layout(height=400, template='plotly_white', showlegend=False)
            st.plotly_chart(fig_cp, use_container_width=True)
    
    with tab6:
        st.subheader("Advanced Analytics")
        
        st.markdown("### 🔗 Correlation Analysis")
        st.info("💡 Values near +1 (red) = synchronized patterns. Near -1 (blue) = opposite trends.")
        
        if len(selected_countries) >= 2:
            fig_corr = plot_correlation_matrix(filtered_df, selected_countries)
            if fig_corr:
                st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.warning("Select at least 2 countries")
        
        st.markdown("---")
        st.markdown("### 📥 Data Export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_full = filtered_df.to_csv(index=False)
            st.download_button("📄 Full Data", csv_full, "filtered.csv", "text/csv")
        
        with col2:
            summary = filtered_df.groupby(['countryName', 'reportingYear', 'Risk_Category']).agg({
                'Releases': 'sum', 'Pollutant': 'count'
            }).reset_index()
            csv_summary = summary.to_csv(index=False)
            st.download_button("📊 Summary", csv_summary, "summary.csv", "text/csv")
        
        with col3:
            pivot = filtered_df.pivot_table(
                index='countryName', columns='reportingYear',
                values='Releases', aggfunc='sum', fill_value=0
            )
            csv_pivot = pivot.to_csv()
            st.download_button("📈 Pivot", csv_pivot, "pivot.csv", "text/csv")
        
        st.markdown("---")
        st.markdown("### 🔍 Data Table")
        
        if st.checkbox("Show data table"):
            search = st.text_input("🔎 Search:")
            
            display = filtered_df.copy()
            if search:
                display = display[
                    display['countryName'].str.contains(search, case=False) |
                    display['Pollutant'].str.contains(search, case=False)
                ]
            
            st.write(f"Showing {len(display):,} records")
            st.dataframe(
                display[['countryName', 'reportingYear', 'Pollutant', 'Risk_Category', 'Releases']],
                use_container_width=True
            )

if __name__ == "__main__":
    main()
