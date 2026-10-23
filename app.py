"""
Egyptian Real Estate Executive Analytics Cockpit
Stretched Compact Layout (Fills Full Screen, No Free Gap at Bottom)
Fixed Overlaps, Truncated Labels, and Restored Vibrant Colors
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & VIEWPORT OPTIMIZATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Egyptian Real Estate Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for stretched, full-screen dashboard without bottom gap
st.markdown("""
<style>
    /* Clean light background matching previous version */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Hide top default Streamlit header bar completely to reclaim space */
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    
    /* Main block container: optimized padding to fill vertical height */
    .block-container {
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
        max-width: 100% !important;
    }

    /* Minimal spacing between rows */
    div[data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.4rem !important;
    }

    /* Streamlit container cards: crisp white, clear light borders */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 6px 10px 4px 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        gap: 0.15rem !important;
    }

    /* Left Filter Panel Styling */
    .filter-panel-title {
        font-size: 1.0rem;
        font-weight: 800;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 0.35rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Clean Multiselect Tag styling */
    span[data-baseweb="tag"] {
        background-color: #eff6ff !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 4px !important;
        color: #1e40af !important;
        font-size: 0.72rem !important;
        padding: 1px 5px !important;
    }
    span[data-baseweb="tag"] span {
        color: #1e40af !important;
    }

    /* Compact Top Header Bar */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2px 2px 5px 2px;
        border-bottom: 1.5px solid #e2e8f0;
        margin-bottom: 4px;
    }
    .nav-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 6px;
        letter-spacing: -0.01em;
    }
    .nav-badge {
        font-size: 0.72rem;
        padding: 2px 8px;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        color: #2563eb;
        font-weight: 700;
    }

    /* KPI metric cards: slightly taller and cleaner */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 6px 9px;
        height: 56px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-card:hover {
        border-color: #cbd5e1;
    }
    .kpi-top {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 0.65rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        flex-shrink: 0;
    }
    .kpi-value {
        font-size: 1.15rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.15;
        margin-top: 1px;
    }
    .kpi-sub {
        font-size: 0.62rem;
        color: #64748b;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Chart Header */
    .chart-header {
        font-size: 0.76rem;
        font-weight: 700;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 4px;
        padding: 1px 2px;
    }
    .chart-indicator {
        width: 8px;
        height: 8px;
        border-radius: 2px;
        display: inline-block;
        flex-shrink: 0;
    }

    /* Match Badge in Filter Column */
    .filter-count-badge {
        background: #ecfdf5;
        border: 1px solid #6ee7b7;
        color: #047857;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 0.80rem;
        font-weight: 700;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 6px;
    }

    /* Clean widget labels */
    .stRadio label, .stSlider label, .stMultiSelect label {
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        color: #334155 !important;
    }

    /* Scroll ONLY inside the left filter column (dashboard itself never scrolls) */
    div[data-testid="stColumn"]:has(.filter-scroll-anchor) {
        max-height: calc(100vh - 12px);
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 6px;
    }
    div[data-testid="stColumn"]:has(.filter-scroll-anchor)::-webkit-scrollbar {
        width: 8px;
    }
    div[data-testid="stColumn"]:has(.filter-scroll-anchor)::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    div[data-testid="stColumn"]:has(.filter-scroll-anchor)::-webkit-scrollbar-track {
        background: transparent;
    }
    .filter-scroll-anchor {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. DATA LOADING & ROBUST CLEANING
# -----------------------------------------------------------------------------
def clean_numeric_rooms(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().lower()
    if s == 'none':
        return 0.0
    if s == 'studio':
        return 1.0
    if s == '7+':
        return 7.0
    try:
        return float(s)
    except:
        return np.nan

@st.cache_data(show_spinner=False)
def load_data():
    dfs = pd.read_csv("Sell (Cleaned).csv")
    dfr = pd.read_csv("Rent (Cleaned).csv")

    dfs["bed_num"] = dfs["bedrooms"].apply(clean_numeric_rooms)
    dfs["bath_num"] = dfs["bathrooms"].apply(clean_numeric_rooms)
    dfr["bed_num"] = dfr["bedrooms"].apply(clean_numeric_rooms)
    dfr["bath_num"] = dfr["bathrooms"].apply(clean_numeric_rooms)

    if "price_per_sqm" not in dfs.columns:
        dfs["price_per_sqm"] = dfs["price_egp"] / dfs["area_value"]
    if "price_per_sqm" not in dfr.columns:
        dfr["price_per_sqm"] = dfr["price_egp"] / dfr["area_value"]

    dfs["price_million"] = dfs["price_egp"] / 1e6
    dfr["price_thousand"] = dfr["price_egp"] / 1e3

    dfs["market_type"] = "Buy"
    dfr["market_type"] = "Rent"

    return dfs, dfr

dfs_raw, dfr_raw = load_data()


# -----------------------------------------------------------------------------
# 3. ROOT 2-COLUMN LAYOUT: PERMANENT FILTERS (LEFT) & DASHBOARD (RIGHT)
# -----------------------------------------------------------------------------
col_filters, col_main = st.columns([1.18, 4.82], gap="small")

# --- LEFT COLUMN: PERMANENTLY VISIBLE FILTER PANEL ---
with col_filters:
    st.markdown('<span class="filter-scroll-anchor"></span>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="filter-panel-title">🔍 Market Filters</div>', unsafe_allow_html=True)

        market_mode = st.radio(
            "Select Market Mode",
            options=["🏢 Buy (Sale)", "🔑 Rent", "⚖️ Compare (All)"],
            index=0
        )

        if market_mode == "🏢 Buy (Sale)":
            base_df = dfs_raw
        elif market_mode == "🔑 Rent":
            base_df = dfr_raw
        else:
            common_cols = ["city", "town", "property_type", "price_egp", "area_value", "bed_num", "bath_num", "bedrooms", "lat", "lon", "price_per_sqm"]
            base_df = pd.concat([dfs_raw[common_cols], dfr_raw[common_cols]], ignore_index=True)

        # City filter
        available_cities = sorted(base_df["city"].dropna().unique().tolist())
        selected_cities = st.multiselect(
            "Governorate / City",
            options=available_cities,
            default=available_cities,
            placeholder="All Cities"
        )
        if not selected_cities:
            selected_cities = available_cities

        # Town filter
        available_towns = sorted(base_df["town"].dropna().unique().tolist())
        selected_towns = st.multiselect(
            "Town",
            options=available_towns,
            default=[],
            placeholder="All Towns"
        )
        if not selected_towns:
            selected_towns = available_towns

        # Property Type filter
        available_types = sorted(base_df["property_type"].dropna().unique().tolist())
        default_types = [t for t in ["Apartment", "Villa", "Duplex", "Twin House", "Townhouse", "Chalet"] if t in available_types]
        if not default_types:
            default_types = available_types[:5]

        selected_types = st.multiselect(
            "Property Type",
            options=available_types,
            default=default_types,
            placeholder="All Types"
        )
        if not selected_types:
            selected_types = available_types

        # Bedrooms filter
        bed_options = ["Studio", "1", "2", "3", "4", "5", "6", "7+"]
        selected_beds = st.multiselect(
            "Bedrooms",
            options=bed_options,
            default=bed_options,
            placeholder="All Bedrooms"
        )
        if not selected_beds:
            selected_beds = bed_options

        # Dynamic Price Slider
        if market_mode == "🏢 Buy (Sale)":
            max_p = float(dfs_raw["price_million"].quantile(0.99))
            price_range = st.slider("Price Range (M EGP)", 0.5, round(max_p, 1), (0.5, round(max_p, 1)), step=0.5)
        elif market_mode == "🔑 Rent":
            max_p = float(dfr_raw["price_thousand"].quantile(0.99))
            price_range = st.slider("Monthly Rent (K EGP)", 1.0, round(max_p, 1), (1.0, round(max_p, 1)), step=1.0)
        else:
            price_range = None

        # Area Slider
        max_a = int(base_df["area_value"].quantile(0.99))
        area_range = st.slider("Property Area (sqm)", 20, max_a, (30, min(600, max_a)), step=10)

        # Map Sampling Limit
        sample_size = st.slider("Map Sampling Limit", 500, 3000, 1500, step=100)


# -----------------------------------------------------------------------------
# 4. FILTERING ENGINE
# -----------------------------------------------------------------------------
def filter_df(df, is_rent=False):
    # Map selected bed strings to column values
    bed_match = df["bedrooms"].astype(str).str.strip().str.lower().apply(
        lambda x: "Studio" if x == "studio" else (x.title() if x in ["1", "2", "3", "4", "5", "6", "7+"] else x)
    )
    mask = (
        df["city"].isin(selected_cities) &
        df["town"].isin(selected_towns) &
        df["property_type"].isin(selected_types) &
        bed_match.isin(selected_beds) &
        (df["area_value"] >= area_range[0]) &
        (df["area_value"] <= area_range[1])
    )
    if price_range is not None:
        if is_rent:
            mask = mask & (df["price_thousand"] >= price_range[0]) & (df["price_thousand"] <= price_range[1])
        else:
            mask = mask & (df["price_million"] >= price_range[0]) & (df["price_million"] <= price_range[1])
    return df[mask].copy()

filtered_dfs = filter_df(dfs_raw, is_rent=False)
filtered_dfr = filter_df(dfr_raw, is_rent=True)

if market_mode == "🏢 Buy (Sale)":
    active_df = filtered_dfs
elif market_mode == "🔑 Rent":
    active_df = filtered_dfr
else:
    active_df = pd.concat([filtered_dfs, filtered_dfr], ignore_index=True)

total_count = len(active_df)
raw_total = len(base_df)
coverage_pct = (total_count / raw_total * 100) if raw_total > 0 else 0

# Match badge and reset button in the left filter column
with col_filters:
    st.markdown(f'<div class="filter-count-badge">🟢 <b>{total_count:,}</b> properties match</div>', unsafe_allow_html=True)
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()


# -----------------------------------------------------------------------------
# 5. RIGHT COLUMN: TOP NAV, 6 KPIS, AND STRETCHED 2x3 CHART GRID
# -----------------------------------------------------------------------------
with col_main:
    # Top Header
    st.markdown("""
    <div class="top-navbar">
        <div class="nav-title">
            <span>🇪🇬</span> Egyptian Real Estate Market Intelligence
        </div>
        <div class="nav-badge">Live Market Benchmarks</div>
    </div>
    """, unsafe_allow_html=True)

    # 6 Compact KPI Cards
    k1, k2, k3, k4, k5, k6 = st.columns(6, gap="small")

    if market_mode == "🏢 Buy (Sale)":
        med_price = active_df["price_million"].median() if total_count > 0 else 0
        med_sqm = active_df["price_per_sqm"].median() if total_count > 0 else 0
        med_area = active_df["area_value"].median() if total_count > 0 else 0
        avg_beds = active_df["bed_num"].mean() if total_count > 0 else 0

        val_k1 = f"{total_count:,}"
        sub_k1 = f"{coverage_pct:.1f}% market"
        
        val_k2 = f"{med_price:.2f} M"
        sub_k2 = "Median Sale EGP"

        val_k3 = f"{med_sqm:,.0f}"
        sub_k3 = "EGP / SQM"

        val_k4 = f"{med_area:.0f} sqm"
        sub_k4 = "Median Area"

        val_k5 = f"{avg_beds:.1f} Beds"
        sub_k5 = "Average Rooms"

        val_k6 = f"{coverage_pct:.1f}%"
        sub_k6 = f"{len(selected_cities)} Cities"

    elif market_mode == "🔑 Rent":
        med_rent = active_df["price_egp"].median() if total_count > 0 else 0
        med_sqm = active_df["price_per_sqm"].median() if total_count > 0 else 0
        med_area = active_df["area_value"].median() if total_count > 0 else 0
        avg_beds = active_df["bed_num"].mean() if total_count > 0 else 0

        val_k1 = f"{total_count:,}"
        sub_k1 = f"{coverage_pct:.1f}% rentals"

        val_k2 = f"{med_rent:,.0f}"
        sub_k2 = "Monthly Rent EGP"

        val_k3 = f"{med_sqm:,.1f}"
        sub_k3 = "EGP / SQM / mo"

        val_k4 = f"{med_area:.0f} sqm"
        sub_k4 = "Median Area"

        val_k5 = f"{avg_beds:.1f} Beds"
        sub_k5 = "Average Rooms"

        val_k6 = f"{coverage_pct:.1f}%"
        sub_k6 = f"{len(selected_cities)} Cities"

    else:
        sale_med = filtered_dfs["price_million"].median() if len(filtered_dfs) > 0 else 0
        rent_med = filtered_dfr["price_egp"].median() if len(filtered_dfr) > 0 else 0
        gross_yield = (rent_med * 12) / (sale_med * 1e6) * 100 if (sale_med > 0 and rent_med > 0) else 0

        val_k1 = f"{total_count:,}"
        sub_k1 = f"Sale: {len(filtered_dfs):,} | Rent: {len(filtered_dfr):,}"

        val_k2 = f"{sale_med:.2f} M"
        sub_k2 = "Median Sale EGP"

        val_k3 = f"{rent_med:,.0f}"
        sub_k3 = "Monthly Rent EGP"

        val_k4 = f"{gross_yield:.1f}%"
        sub_k4 = "Est. Gross Yield"

        val_k5 = f"{active_df['area_value'].median():.0f} sqm" if total_count > 0 else "0 sqm"
        sub_k5 = "Median Area"

        val_k6 = f"{coverage_pct:.1f}%"
        sub_k6 = "Sample Coverage"

    kpis = [
        (k1, "Matching Units", val_k1, sub_k1, "#3182ce"),
        (k2, "Avg / Med Price", val_k2, sub_k2, "#38a169"),
        (k3, "Price / SQM", val_k3, sub_k3, "#00b4d8"),
        (k4, "Area / Yield", val_k4, sub_k4, "#d97706"),
        (k5, "Bedrooms", val_k5, sub_k5, "#805ad5"),
        (k6, "Coverage", val_k6, sub_k6, "#e53e3e")
    ]

    for col, title, val, sub, col_dot in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-dot" style="background:{col_dot};"></span>
                    <span>{title}</span>
                </div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)


    # -------------------------------------------------------------------------
    # 6. STRETCHED 2x3 CHART GRID (Fills Free Bottom Space & Fixes Truncation)
    # -------------------------------------------------------------------------
    # Height calibrated to 285px to fill screen perfectly without scrolling
    PLOT_HEIGHT = 285
    PLOTLY_CONFIG = {
        'displayModeBar': False,
        'staticPlot': False,
        'responsive': True
    }

    # Restored Spectral Palette
    SPECTRAL_PALETTE = ['#d53e4f', '#fc8d59', '#fee08b', '#99d594', '#3288bd', '#805ad5', '#e65100', '#00897b']

    # ----------------- ROW 1 -----------------
    r1c1, r1c2, r1c3 = st.columns(3, gap="small")

    # --- CHART 1: GEOSPATIAL MAP (Top Left - Clean OpenStreetMap) ---
    with r1c1:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-header">
                <span class="chart-indicator" style="background:#3182ce;"></span>
                <span>📍 Geographic Property Distribution</span>
            </div>
            """, unsafe_allow_html=True)
            
            geo_df = active_df.dropna(subset=["lat", "lon"]).copy()
            if len(geo_df) > 0:
                n_sample = min(sample_size, len(geo_df))
                sample_map = geo_df.sample(n=n_sample, random_state=42).copy()

                if market_mode == "🔑 Rent":
                    sample_map["price_disp"] = sample_map["price_egp"].apply(lambda v: f"{v:,.0f} EGP / mo")
                else:
                    sample_map["price_disp"] = (sample_map["price_egp"] / 1e6).apply(lambda v: f"{v:,.2f} M EGP")
                sample_map["area_disp"] = sample_map["area_value"].apply(lambda v: f"{v:,.0f} sqm")

                fig_map = px.scatter_map(
                    sample_map,
                    lat="lat",
                    lon="lon",
                    color="property_type" if market_mode != "⚖️ Compare (All)" else "market_type",
                    color_discrete_sequence=SPECTRAL_PALETTE,
                    custom_data=["property_type", "price_disp", "area_disp"],
                    zoom=5.2,
                    center={"lat": 29.8, "lon": 31.3},
                    height=PLOT_HEIGHT
                )
                fig_map.update_traces(
                    marker=dict(size=5, opacity=0.85),
                    hovertemplate="<b>%{customdata[0]}</b><br>💰 %{customdata[1]}<br>📐 %{customdata[2]}<extra></extra>"
                )
                fig_map.update_layout(
                    map_style="open-street-map",
                    margin=dict(l=0, r=0, t=4, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False
                )
                st.plotly_chart(fig_map, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No GPS coordinates for selected criteria.")


    # --- CHART 2: DONUT CHART (Top Center - Fixed Text Overlap) ---
    with r1c2:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-header">
                <span class="chart-indicator" style="background:#d53e4f;"></span>
                <span>🍩 Market Concentration (Property Type)</span>
            </div>
            """, unsafe_allow_html=True)

            if total_count > 0:
                type_counts = active_df["property_type"].value_counts().head(6)

                fig_donut = go.Figure(data=[go.Pie(
                    labels=type_counts.index,
                    values=type_counts.values,
                    hole=0.64,
                    domain=dict(x=[0, 0.72]),
                    marker=dict(colors=SPECTRAL_PALETTE[:len(type_counts)], line=dict(color="#ffffff", width=2)),
                    textinfo="percent",
                    textposition="inside",
                    textfont=dict(color="#ffffff", size=10, family="Arial Black"),
                    hoverinfo="label+value+percent",
                    showlegend=True
                )])
                
                top_name = type_counts.index[0]
                top_share = (type_counts.iloc[0] / total_count * 100) if total_count > 0 else 0
                fig_donut.update_layout(
                    height=PLOT_HEIGHT,
                    margin=dict(l=5, r=5, t=5, b=5),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="right",
                        x=1.05,
                        font=dict(size=9, color="#475569")
                    ),
                    annotations=[
                        dict(
                            text=f"<b>{top_share:.1f}%</b><br><span style='font-size:9px;color:#64748b;font-weight:600;'>{top_name}</span>",
                            x=0.36, y=0.5,
                            font=dict(size=16, color="#2563eb"),
                            showarrow=False
                        )
                    ]
                )
                st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No property records.")


    # --- CHART 3: HORIZONTAL BAR CHART (Top Right - Fixed Label Truncation) ---
    with r1c3:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-header">
                <span class="chart-indicator" style="background:#38a169;"></span>
                <span>📊 Top Locations by Volume (Viridis)</span>
            </div>
            """, unsafe_allow_html=True)

            if total_count > 0:
                city_counts = active_df["city"].value_counts().head(7).iloc[::-1]
                max_bar = city_counts.max()

                fig_hbar = go.Figure(go.Bar(
                    x=city_counts.values,
                    y=city_counts.index,
                    orientation='h',
                    marker=dict(
                        color=list(range(len(city_counts))),
                        colorscale='Viridis',
                        showscale=False,
                        line=dict(color='#ffffff', width=1)
                    ),
                    text=city_counts.values,
                    texttemplate='%{text:,}',
                    textposition='outside',
                    textfont=dict(size=10, color='#0f172a', family="Arial Black")
                ))
                fig_hbar.update_layout(
                    height=PLOT_HEIGHT,
                    # Headroom on right (r=50) & xaxis range prevents any label truncation
                    margin=dict(l=10, r=50, t=10, b=25),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(
                        range=[0, max_bar * 1.25],
                        showgrid=True,
                        gridcolor="#e2e8f0",
                        zeroline=False,
                        tickfont=dict(size=9, color="#64748b")
                    ),
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(size=9, color="#1e293b", weight="bold")
                    )
                )
                st.plotly_chart(fig_hbar, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No location records.")


    # ----------------- ROW 2 -----------------
    r2c1, r2c2, r2c3 = st.columns(3, gap="small")

    # --- CHART 4: CORRELATION MATRIX (Bottom Left - Fixed Y-Axis Clipping) ---
    with r2c1:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-header">
                <span class="chart-indicator" style="background:#0284c7;"></span>
                <span>🔢 Feature Correlation Matrix</span>
            </div>
            """, unsafe_allow_html=True)

            if total_count > 10:
                corr_subset = active_df[["price_egp", "area_value", "bed_num", "bath_num", "price_per_sqm"]].rename(columns={
                    "price_egp": "Price",
                    "area_value": "Area",
                    "bed_num": "Beds",
                    "bath_num": "Baths",
                    "price_per_sqm": "SQM"
                })
                corr_matrix = corr_subset.corr().round(2)

                fig_corr = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='Blues',
                    text=corr_matrix.values,
                    texttemplate="%{text:.2f}",
                    textfont=dict(size=10, color="#0f172a", family="Arial Black"),
                    showscale=False
                ))
                fig_corr.update_layout(
                    height=PLOT_HEIGHT,
                    # l=55 provides ample room so Y-axis labels ('Price', 'Area', 'Beds') are never clipped
                    margin=dict(l=55, r=15, t=10, b=30),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(tickfont=dict(size=9, color="#1e293b", weight="bold")),
                    yaxis=dict(tickfont=dict(size=9, color="#1e293b", weight="bold"), autorange="reversed")
                )
                st.plotly_chart(fig_corr, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("Insufficient data for correlation.")


    # --- CHART 5: BOX PLOT (Bottom Center - Spectral Palette Restored) ---
    with r2c2:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-header">
                <span class="chart-indicator" style="background:#fc8d59;"></span>
                <span>📦 Price Range by Property Type (Spectral)</span>
            </div>
            """, unsafe_allow_html=True)

            if total_count > 0:
                top_types_box = active_df["property_type"].value_counts().head(4).index.tolist()
                box_data = active_df[active_df["property_type"].isin(top_types_box)].copy()
                
                q95 = box_data["price_egp"].quantile(0.95)
                box_data = box_data[box_data["price_egp"] <= q95]

                if market_mode == "🔑 Rent":
                    box_data["y_val"] = box_data["price_egp"] / 1e3
                    y_title = "Monthly Rent (Thousand EGP)"
                else:
                    box_data["y_val"] = box_data["price_egp"] / 1e6
                    y_title = "Sale Price (Million EGP)"

                fig_violin = go.Figure()
                for i, ptype in enumerate(top_types_box):
                    sub = box_data[box_data["property_type"] == ptype]
                    c_color = SPECTRAL_PALETTE[i % len(SPECTRAL_PALETTE)]
                    fig_violin.add_trace(go.Box(
                        x=sub["property_type"],
                        y=sub["y_val"],
                        name=ptype,
                        marker_color=c_color,
                        boxpoints=False,
                        line=dict(width=1.8)
                    ))

                fig_violin.update_layout(
                    height=PLOT_HEIGHT,
                    margin=dict(l=15, r=10, t=10, b=25),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    xaxis=dict(
                        tickfont=dict(size=9, color="#1e293b", weight="bold"),
                        showgrid=False
                    ),
                    yaxis=dict(
                        title=dict(text=y_title, font=dict(size=9, color="#475569", weight="bold")),
                        showgrid=True,
                        gridcolor="#e2e8f0",
                        tickfont=dict(size=9, color="#64748b")
                    )
                )
                st.plotly_chart(fig_violin, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("No distribution records.")


    # --- CHART 6: MEDIAN PROPERTY PRICE BY LOCATION (Bottom Right) ---
    with r2c3:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-header">
                <span class="chart-indicator" style="background:#2563eb;"></span>
                <span>🏙️ Median Property Price by Location</span>
            </div>
            """, unsafe_allow_html=True)

            if total_count > 0:
                loc_df = active_df.dropna(subset=["city"]).copy()
                if market_mode == "🔑 Rent":
                    loc_df["loc_price"] = loc_df["price_egp"] / 1e3
                    loc_unit = "K EGP"
                    loc_suffix = "K"
                else:
                    loc_df["loc_price"] = loc_df["price_egp"] / 1e6
                    loc_unit = "M EGP"
                    loc_suffix = "M"

                loc_agg = (
                    loc_df.groupby("city")["loc_price"]
                    .agg(median="median", count="count")
                    .dropna(subset=["median"])
                    .sort_values("median", ascending=True)
                )

                if len(loc_agg) > 0:
                    max_loc = loc_agg["median"].max()
                    loc_text = [
                        f"{v:,.1f} {loc_suffix}  (n={int(c):,})"
                        for v, c in zip(loc_agg["median"], loc_agg["count"])
                    ]

                    fig_loc = go.Figure(go.Bar(
                        x=loc_agg["median"],
                        y=loc_agg.index,
                        orientation="h",
                        marker=dict(
                            color=list(range(len(loc_agg))),
                            colorscale="Viridis",
                            showscale=False,
                            line=dict(color="#ffffff", width=1)
                        ),
                        text=loc_text,
                        textposition="outside",
                        textfont=dict(size=9, color="#0f172a", family="Arial Black"),
                        hoverinfo="y+text"
                    ))
                    fig_loc.update_layout(
                        height=PLOT_HEIGHT,
                        margin=dict(l=10, r=110, t=8, b=28),
                        bargap=0.16,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(
                            range=[0, max_loc * 1.5],
                            title=dict(text=f"Median Price ({loc_unit})", font=dict(size=9, color="#475569", weight="bold")),
                            showgrid=True,
                            gridcolor="#e2e8f0",
                            zeroline=False,
                            tickfont=dict(size=9, color="#64748b")
                        ),
                        yaxis=dict(
                            showgrid=False,
                            tickfont=dict(size=9, color="#1e293b", weight="bold")
                        )
                    )
                    st.plotly_chart(fig_loc, use_container_width=True, config=PLOTLY_CONFIG)
                else:
                    st.info("No location data.")
            else:
                st.info("No records available.")
