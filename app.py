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
    page_title="Game Analytics",
    page_icon="🎾",
    layout="wide"
)

st.title("🎾 Game Analytics Dashboard")
st.markdown("---")

# ── Sidebar Navigation ──────────────────────────────────────

st.sidebar.title("MENU")
page = st.sidebar.radio("----------", [
    "🏠 Home",
    "🔍 Search & Filter",
    "👤 Competitor Details",
    "🌍 Country Analysis",
    "🏆 Leaderboard"
])

if st.sidebar.button("🔄 Refresh Latest Data"):
    with st.spinner("Fetching latest data from API..."):
        insert_all()

    st.sidebar.success("Data Updated Successfully!")


# ═══════════════════════════════════════════════════════════
# PAGE 1 - HOME
# ═══════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.header("🏠 Home Page")
    st.markdown("---")

    # Summary Stats
    df_all = all_competitors_with_rank()
    df_countries = competitors_count_by_country()
    df_top = highest_points_competitor()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🧑 Total Competitors", len(df_all))

    with col2:
        st.metric("🌍 Countries Represented", len(df_countries))

    with col3:
        if not df_top.empty:
            st.metric("🏅 Highest Points", df_top["points"].iloc[0])

    st.markdown("---")

    # Top 5 table
    st.subheader("🏆 Top 5 Competitors")
    st.dataframe(top_5_competitors(), use_container_width=True)

    st.markdown("---")

    # Competitions overview
    st.subheader("📊 Competitions by Category")
    st.dataframe(competitions_count_by_category(), use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE 2 - SEARCH & FILTER
# ═══════════════════════════════════════════════════════════
elif page == "🔍 Search & Filter":
    st.header("🔍 Search & Filter Competitors")
    st.markdown("---")

    df = all_competitors_with_rank()

    # Filters
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

    # Apply filters
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

    st.markdown(f"**{len(filtered)} competitors found**")
    st.dataframe(filtered, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE 3 - COMPETITOR DETAILS
# ═══════════════════════════════════════════════════════════
elif page == "👤 Competitor Details":
    st.header("👤 Competitor Details")
    st.markdown("---")

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
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🏅 Rank", player["rank"])
        col2.metric("📈 Movement", player["movement"])
        col3.metric("⭐ Points", player["points"])
        col4.metric("🎾 Competitions Played", player["competitions_played"])

        st.markdown("---")
        st.subheader("📋 Full Details")
        st.table(player.to_frame().T)


# ═══════════════════════════════════════════════════════════
# PAGE 4 - COUNTRY ANALYSIS
# ═══════════════════════════════════════════════════════════
elif page == "🌍 Country Analysis":
    st.header("🌍 Country-Wise Analysis")
    st.markdown("---")

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

    st.subheader(" Competitors per Country")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader(" Top 10 Countries by Competitors")
    top10 = df.head(10).set_index("country")
    st.bar_chart(top10["total_competitors"])

    st.markdown("---")
    st.subheader(" Top 10 Countries by Avg Points")
    top10_points = df.nlargest(10, "avg_points").set_index("country")
    st.bar_chart(top10_points["avg_points"])


# ═══════════════════════════════════════════════════════════
# PAGE 5 - LEADERBOARD
# ═══════════════════════════════════════════════════════════
elif page == "🏆 Leaderboard":
    st.header("🏆 Leaderboard")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🥇 Top Ranked Competitors")
        conn = get_connection()
        df_rank = pd.read_sql_query("""
            SELECT co.name, co.country, cr.rank, cr.points
            FROM competitors co
            JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
            ORDER BY cr.rank
            LIMIT 10
        """, conn)
        conn.close()
        st.dataframe(df_rank, use_container_width=True)

    with col2:
        st.subheader(" Highest Points Competitors")
        conn = get_connection()
        df_points = pd.read_sql_query("""
            SELECT co.name, co.country, cr.points, cr.rank
            FROM competitors co
            JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
            ORDER BY cr.points DESC
            LIMIT 10
        """, conn)
        conn.close()
        st.dataframe(df_points, use_container_width=True)

    st.markdown("---")
    st.subheader(" Top 10 Players Points Chart")
    chart_data = df_points.set_index("name")
    st.bar_chart(chart_data["points"])