from database import get_connection
from api_fetch import fetch_all_data
 
def insert_competitions(competitions):
    conn = get_connection()
    cursor = conn.cursor()

  
    for comp in competitions:
        category = comp.get("category", {})
        if category:
            cursor.execute("""INSERT OR IGNORE INTO categories (category_id, category_name) VALUES (?, ?)""",
                           (category.get("id"),
                            category.get("name")))
            

            cursor.execute("""INSERT OR IGNORE INTO competitions (competition_id, competition_name, parent_id, type, gender, category_id) VALUES (?, ?, ?, ?, ?, ?)""",
                           (comp.get("id"),
                            comp.get("name"),
                            comp.get("parent_id"),
                            comp.get("type", "singles"),
                            comp.get("gender", "men"),
                            category.get("id") if category else None)) 
    conn.commit()
    conn.close()
            
                           
def insert_complexes(complexes):
    conn = get_connection()
    cursor = conn.cursor()
 
    for complex in complexes:
        cursor.execute("""
            INSERT OR IGNORE INTO complexes (complex_id, complex_name) VALUES (?, ?)""",
            (complex.get("id"),
             complex.get("name")))
        
        venues = complex.get("venues", [])
        for venue in venues:
            cursor.execute("""INSERT OR IGNORE INTO venues (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           (venue.get("id"),
                            venue.get("name"),
                            venue.get("city_name", ""),
                            venue.get("country_name", ""),
                            venue.get("country_code", ""),
                            venue.get("timezone", ""),
                            complex.get("id")))
    conn.commit()
    conn.close()


def insert_rankings(rankings):
    conn = get_connection()
    cursor = conn.cursor()
 
    total = 0
    for ranking_week in rankings:
        competitor_rankings = ranking_week.get("competitor_rankings", [])
 
        for entry in competitor_rankings:
            competitor = entry.get("competitor", {})
 
            cursor.execute("""INSERT OR IGNORE INTO competitors (competitor_id, name, country, country_code, abbreviation) VALUES (?, ?, ?, ?, ?)""",
                           (competitor.get("id"),
                            competitor.get("name"),
                            competitor.get("country", ""),
                            competitor.get("country_code", ""),
                            competitor.get("abbreviation", "")))
    
            cursor.execute("""INSERT INTO competitor_rankings (rank, movement, points, competitions_played, competitor_id) VALUES (?, ?, ?, ?, ?)""",
                           (entry.get("rank", 0),
                            entry.get("movement", 0),
                            entry.get("points", 0),
                            entry.get("competitions_played", 0),
                            competitor.get("id")))
            total += 1
    conn.commit()
    conn.close() 
            

def insert_all():
    data = fetch_all_data()
    insert_competitions(data["competitions"])
    insert_complexes(data["complexes"])
    insert_rankings(data["rankings"])
 
if __name__ == "__main__":
    insert_all()

                    
           
                
                
             
            
            
 
               