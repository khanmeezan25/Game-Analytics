import streamlit as st
import pandas as pd
from insert_data import insert_all
from queries import (
    all_competitors_with_rank,
    top_5_competitors,
    stable_rank_competitors,
    competitors_count_by_country,
    highest_points_competitor,
    all_competitions_with_category,
    competitions_count_by_category,
    doubles_competitions,
    top_level_competitions,
    all_venues_with_complex,
    venues_count_by_complex,
    venues_grouped_by_country,
)
from database import get_connection

st.set_page_config(
    page_title="Game Analytics | Tennis Dashboard",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
# CUSTOM CSS 
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

    :root {
        --clay: #C4622D;
        --clay-dark: #A84E22;
        --court-green: #1B4332;
        --court-green-light: #2D6A4F;
        --ivory: #FAF6F0;
        --card: #FFFFFF;
        --charcoal: #2B2622;
        --muted: #8A7F73;
        --gold: #D4A24C;
        --line: #E8E0D4;
    }

    /* ---------- base ---------- */
    .stApp {
        background-color: var(--ivory);
        font-family: 'Archivo', sans-serif;
        color: var(--charcoal);
    }

    [data-testid="stSidebar"] {
        background-color: var(--court-green);
        border-right: none;
    }

    [data-testid="stSidebar"] * {
        color: var(--ivory) !important;
    }

    [data-testid="stSidebar"] .stRadio {
        margin-top: 1.2rem;
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: 14px;
    }

    [data-testid="stSidebar"] .stRadio label {
        font-family: 'Archivo', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        padding: 0.6rem 0.8rem;
        margin: 0 !important;
        border-radius: 8px;
        width: 100%;
        transition: background-color 0.15s ease;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(250,246,240,0.08);
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(250,246,240,0.15);
    }

    section[data-testid="stSidebar"] button {
        background-color: var(--clay) !important;
        color: var(--ivory) !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        transition: background-color 0.15s ease;
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: var(--clay-dark) !important;
    }

    /* ---------- headings ---------- */
    h1 {
        font-family: 'Archivo Black', sans-serif !important;
        color: var(--court-green) !important;
        letter-spacing: -0.5px;
        font-size: 2.4rem !important;
        margin-bottom: 0 !important;
    }

    h2, h3 {
        font-family: 'Archivo', sans-serif !important;
        font-weight: 700 !important;
        color: var(--charcoal) !important;
    }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--clay);
        margin-bottom: 4px;
    }

    hr {
        border: none;
        border-top: 2px solid var(--line);
        margin: 1.2rem 0;
    }

    /* ---------- metric cards ---------- */
    [data-testid="stMetric"] {
        background-color: var(--card);
        border: 1px solid var(--line);
        border-left: 4px solid var(--clay);
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 1px 3px rgba(43,38,34,0.04);
    }

    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: var(--muted) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Archivo Black', sans-serif !important;
        color: var(--court-green) !important;
        font-size: 2rem !important;
    }

    /* ---------- dataframes / tables ---------- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stTable"] table {
        border-radius: 10px;
    }

    /* ---------- inputs ---------- */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border: 1px solid var(--line) !important;
        background-color: var(--card) !important;
    }

    .stSlider [data-baseweb="slider"] {
        padding-top: 6px;
    }

    /* ---------- section tag ---------- */
    .section-tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--court-green);
        background-color: rgba(27,67,50,0.08);
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 0.6rem;
    }

    /* ---------- rank badge ---------- */
    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        font-family: 'Archivo Black', sans-serif;
        font-size: 0.95rem;
        color: var(--ivory);
        background-color: var(--court-green);
        flex-shrink: 0;
    }
    .rank-badge.gold { background-color: var(--gold); color: var(--charcoal); }

    /* ---------- top banner ---------- */
    .hero-banner {
        background: linear-gradient(120deg, var(--court-green) 0%, var(--court-green-light) 100%);
        border-radius: 14px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.6rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        right: -40px;
        top: -40px;
        width: 180px;
        height: 180px;
        border: 3px solid rgba(250,246,240,0.08);
        border-radius: 50%;
    }
    .hero-title {
        font-family: 'Archivo Black', sans-serif;
        color: var(--ivory);
        font-size: 2rem;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        font-family: 'Archivo', sans-serif;
        color: rgba(250,246,240,0.75);
        font-size: 0.95rem;
        margin-top: 4px;
    }

    /* ---------- player card ---------- */
    .player-card {
        background-color: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1rem;
    }
    .player-name {
        font-family: 'Archivo Black', sans-serif;
        font-size: 1.6rem;
        color: var(--court-green);
        margin: 0;
    }
    .player-country {
        font-family: 'JetBrains Mono', monospace;
        color: var(--muted);
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }

    ::-webkit-scrollbar { height: 8px; width: 8px; }
    ::-webkit-scrollbar-thumb { background: var(--line); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
page = st.sidebar.radio("NAVIGATE", [
    "🏠 Home",
    "🔍 Search & Filter",
    "👤 Competitor Details",
    "🌍 Country Analysis",
    "🏆 Leaderboard"
], label_visibility="collapsed")

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

if st.sidebar.button("🔄  Refresh Latest Data", use_container_width=True):
    with st.spinner("Fetching latest data from API..."):
        insert_all()
    st.sidebar.success("Data updated successfully!")

st.sidebar.markdown(
    "<div style='position:fixed; bottom:1.2rem; font-family:JetBrains Mono; "
    "font-size:0.68rem; color:rgba(250,246,240,0.45);'>Powered by Sportradar API</div>",
    unsafe_allow_html=True
)


def section_tag(label):
    st.markdown(f"<span class='section-tag'>{label}</span>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# MAIN PAGE TITLE
# ═══════════════════════════════════════════════════════════
st.markdown(
    "<div style='text-align:center; padding:0.4rem 0 1.6rem 0;'>"
    "<span style='font-family:Archivo Black; font-size:2.8rem; font-weight:900; "
    "color:#1B4332; letter-spacing:-1px;'>🎾 Game Analytics</span>"
    "</div>",
    unsafe_allow_html=True
)


# ═══════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ═══════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown("""
        <div class="hero-banner">
            <p class="hero-sub" style="font-size:1.05rem;">Live competitor rankings, tournament structure & global coverage — at a glance.</p>
        </div>
    """, unsafe_allow_html=True)

    df_all = all_competitors_with_rank()
    df_countries = competitors_count_by_country()
    df_top = highest_points_competitor()

    section_tag("OVERVIEW")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Competitors", len(df_all))
    with col2:
        st.metric("Countries Represented", len(df_countries))
    with col3:
        if not df_top.empty:
            st.metric("Highest Points", f"{df_top['points'].iloc[0]:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        section_tag("TOP 5 COMPETITORS")
        st.dataframe(top_5_competitors(), use_container_width=True, hide_index=True)
    with col_b:
        section_tag("COMPETITIONS BY CATEGORY")
        st.dataframe(competitions_count_by_category(), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════
# PAGE 2 — SEARCH & FILTER
# ═══════════════════════════════════════════════════════════
elif page == "🔍 Search & Filter":
    st.markdown("<h1>Search &amp; Filter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8A7F73; margin-top:-8px;'>Narrow the field by name, country, rank or points.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    df = all_competitors_with_rank()

    col1, col2 = st.columns(2)
    with col1:
        search_name = st.text_input("🔎 Search by Name")
    with col2:
        countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
        selected_country = st.selectbox("🌍 Filter by Country", countries)

    col3, col4 = st.columns(2)
    with col3:
        min_rank = int(df["rank"].min()) if not df.empty else 1
        max_rank = int(df["rank"].max()) if not df.empty else 100
        rank_range = st.slider("🎯 Rank Range", min_rank, max_rank, (min_rank, max_rank))
    with col4:
        min_points = int(df["points"].min()) if not df.empty else 0
        max_points = int(df["points"].max()) if not df.empty else 10000
        points_threshold = st.slider("⭐ Min Points", min_points, max_points, min_points)

    filtered = df.copy()
    if search_name:
        filtered = filtered[filtered["name"].str.contains(search_name, case=False, na=False)]
    if selected_country != "All":
        filtered = filtered[filtered["country"] == selected_country]
    filtered = filtered[
        (filtered["rank"] >= rank_range[0]) &
        (filtered["rank"] <= rank_range[1]) &
        (filtered["points"] >= points_threshold)
    ]

    st.markdown("<br>", unsafe_allow_html=True)
    section_tag(f"{len(filtered)} COMPETITORS FOUND")
    st.dataframe(filtered, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════
# PAGE 3 — COMPETITOR DETAILS
# ═══════════════════════════════════════════════════════════
elif page == "👤 Competitor Details":
    st.markdown("<h1>Competitor Details</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8A7F73; margin-top:-8px;'>Full profile lookup for any ranked competitor.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT co.name, co.country, co.country_code, co.abbreviation,
               cr.rank, cr.movement, cr.points, cr.competitions_played
        FROM competitors co
        JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
        ORDER BY cr.rank
    """, conn)
    conn.close()

    selected = st.selectbox("Select Competitor", df["name"].tolist())

    if selected:
        player = df[df["name"] == selected].iloc[0]
        badge_class = "gold" if player["rank"] <= 3 else ""

        st.markdown(f"""
            <div class="player-card">
                <div style="display:flex; align-items:center; gap:14px;">
                    <span class="rank-badge {badge_class}">#{player['rank']}</span>
                    <div>
                        <p class="player-name">{player['name']}</p>
                        <p class="player-country">{player['country']} · {player['country_code']}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rank", player["rank"])
        col2.metric("Movement", player["movement"])
        col3.metric("Points", f"{player['points']:,}")
        col4.metric("Competitions Played", player["competitions_played"])

        st.markdown("<br>", unsafe_allow_html=True)
        section_tag("FULL RECORD")
        st.table(player.to_frame().T)


# ═══════════════════════════════════════════════════════════
# PAGE 4 — COUNTRY ANALYSIS
# ═══════════════════════════════════════════════════════════
elif page == "🌍 Country Analysis":
    st.markdown("<h1>Country-Wise Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8A7F73; margin-top:-8px;'>Where competitive strength is concentrated worldwide.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT co.country,
               COUNT(*) as total_competitors,
               ROUND(AVG(cr.points), 1) as avg_points
        FROM competitors co
        JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
        GROUP BY co.country
        ORDER BY total_competitors DESC
    """, conn)
    conn.close()

    section_tag("COMPETITORS PER COUNTRY")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        section_tag("TOP 10 — BY COMPETITOR COUNT")
        top10 = df.head(10).set_index("country")
        st.bar_chart(top10["total_competitors"], color="#C4622D")
    with col2:
        section_tag("TOP 10 — BY AVG POINTS")
        top10_points = df.nlargest(10, "avg_points").set_index("country")
        st.bar_chart(top10_points["avg_points"], color="#1B4332")


# ═══════════════════════════════════════════════════════════
# PAGE 5 — LEADERBOARD
# ═══════════════════════════════════════════════════════════
elif page == "🏆 Leaderboard":
    st.markdown("<h1>Leaderboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8A7F73; margin-top:-8px;'>Who's leading the pack, by rank and by points.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_tag("TOP RANKED COMPETITORS")
        conn = get_connection()
        df_rank = pd.read_sql_query("""
            SELECT co.name, co.country, cr.rank, cr.points
            FROM competitors co
            JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
            ORDER BY cr.rank
            LIMIT 10
        """, conn)
        conn.close()
        st.dataframe(df_rank, use_container_width=True, hide_index=True)

    with col2:
        section_tag("HIGHEST POINTS COMPETITORS")
        conn = get_connection()
        df_points = pd.read_sql_query("""
            SELECT co.name, co.country, cr.points, cr.rank
            FROM competitors co
            JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
            ORDER BY cr.points DESC
            LIMIT 10
        """, conn)
        conn.close()
        st.dataframe(df_points, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_tag("TOP 10 PLAYERS — POINTS CHART")
    chart_data = df_points.set_index("name")
    st.bar_chart(chart_data["points"], color="#D4A24C")