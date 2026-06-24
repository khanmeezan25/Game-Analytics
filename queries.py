import pandas as pd
from database import get_connection


def run_query(sql, params=()):
    conn = get_connection()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df


# ══════════════════════════════════════════
# COMPETITIONS QUERIES (7)
# ═══════════════════════════════════════════

def all_competitions_with_category():
    return run_query("""
        SELECT c.competition_name, cat.category_name
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
    """)


def competitions_count_by_category():
    return run_query("""
        SELECT cat.category_name, COUNT(c.competition_id) as total
        FROM categories cat
        JOIN competitions c ON cat.category_id = c.category_id
        GROUP BY cat.category_name
        ORDER BY total DESC
    """)


def doubles_competitions():
    return run_query("""
        SELECT competition_name, gender, category_id
        FROM competitions
        WHERE type = 'doubles'
    """)


def competitions_by_category_name(category_name):
    return run_query("""
        SELECT c.competition_name, c.type, c.gender
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
        WHERE cat.category_name = ?
    """, (category_name,))


def parent_and_sub_competitions():
    return run_query("""
        SELECT 
            p.competition_name as parent_name,
            c.competition_name as sub_competition
        FROM competitions c
        JOIN competitions p ON c.parent_id = p.competition_id
    """)


def competition_types_by_category():
    return run_query("""
        SELECT cat.category_name, c.type, COUNT(*) as total
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name, c.type
        ORDER BY cat.category_name
    """)


def top_level_competitions():
    return run_query("""
        SELECT competition_name, type, gender
        FROM competitions
        WHERE parent_id IS NULL
    """)


# ═══════════════════════════════════════════
# VENUES & COMPLEXES QUERIES (7)
# ═══════════════════════════════════════════

def all_venues_with_complex():
    return run_query("""
        SELECT v.venue_name, c.complex_name
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
    """)


def venues_count_by_complex():
    return run_query("""
        SELECT c.complex_name, COUNT(v.venue_id) as total_venues
        FROM complexes c
        JOIN venues v ON c.complex_id = v.complex_id
        GROUP BY c.complex_name
        ORDER BY total_venues DESC
    """)


def venues_by_country(country_name):
    return run_query("""
        SELECT venue_name, city_name, country_name, timezone
        FROM venues
        WHERE country_name = ?
    """, (country_name,))


def all_venues_with_timezone():
    return run_query("""
        SELECT venue_name, city_name, country_name, timezone
        FROM venues
        ORDER BY timezone
    """)


def complexes_with_multiple_venues():
    return run_query("""
        SELECT c.complex_name, COUNT(v.venue_id) as total_venues
        FROM complexes c
        JOIN venues v ON c.complex_id = v.complex_id
        GROUP BY c.complex_name
        HAVING total_venues > 1
        ORDER BY total_venues DESC
    """)


def venues_grouped_by_country():
    return run_query("""
        SELECT country_name, COUNT(*) as total_venues
        FROM venues
        GROUP BY country_name
        ORDER BY total_venues DESC
    """)


def venues_by_complex_name(complex_name):
    return run_query("""
        SELECT v.venue_name, v.city_name, v.country_name
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        WHERE c.complex_name = ?
    """, (complex_name,))


# ═══════════════════════════════════════════
# RANKINGS QUERIES (6)
# ═══════════════════════════════════════════

def all_competitors_with_rank():
    return run_query("""
        SELECT co.name, co.country, cr.rank, cr.points
        FROM competitors co
        JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
        ORDER BY cr.rank
    """)


def top_5_competitors():
    return run_query("""
        SELECT co.name, co.country, cr.rank, cr.points
        FROM competitors co
        JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
        ORDER BY cr.rank
        LIMIT 5
    """)


def stable_rank_competitors():
    return run_query("""
        SELECT co.name, co.country, cr.rank, cr.movement
        FROM competitors co
        JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
        WHERE cr.movement = 0
    """)


def total_points_by_country(country_name):
    return run_query("""
        SELECT co.country, SUM(cr.points) as total_points
        FROM competitors co
        JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
        WHERE co.country = ?
        GROUP BY co.country
    """, (country_name,))


def competitors_count_by_country():
    return run_query("""
        SELECT country, COUNT(*) as total_competitors
        FROM competitors
        GROUP BY country
        ORDER BY total_competitors DESC
    """)


def highest_points_competitor():
    return run_query("""
        SELECT co.name, co.country, cr.points, cr.rank
        FROM competitors co
        JOIN competitor_rankings cr ON co.competitor_id = cr.competitor_id
        ORDER BY cr.points DESC
        LIMIT 1
    """)


if __name__ == "__main__":
    print(all_competitions_with_category())
    print(top_5_competitors())
    print(venues_grouped_by_country())