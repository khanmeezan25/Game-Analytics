import requests
import time

API_KEY = "qZMwwAdcppDPHbA3YkSj4dzaALJOVTTKiAX0hOnj"

BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en"

def fetch_data(url):
    
    try:
        response = requests.get(url)
        print(f"Data Fetching Sucessfully{url}")
        

        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 401:
            return None
        
        elif response.status_code == 429:
            time.sleep(10)
            return fetch_data(url)
        
        else:
            print(f"Error! : {response.status_code} ")
            return None
        
    except Exception as e:
        print(f"Error: {e}") 
        return None   
    


# -------- COMPETITION DATA API --------

def fetch_competitions():
     url = f"https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=qZMwwAdcppDPHbA3YkSj4dzaALJOVTTKiAX0hOnj"
     data = fetch_data(url)

     if data:
          competitions = data.get("competitions", [])
          return competitions
     return []


# -------- COMPLEXES DATA API --------

def fetch_complexes():
    url = f"https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=qZMwwAdcppDPHbA3YkSj4dzaALJOVTTKiAX0hOnj"
    data = fetch_data(url)
    
    if data:
        complexes = data.get("complexes", [])
        return complexes
    return []


# -------- RANKINGS DATA API --------

def fetch_rankings():
    url = f"https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key=qZMwwAdcppDPHbA3YkSj4dzaALJOVTTKiAX0hOnj"

    data = fetch_data(url)

    if data:
        rankings = data.get("rankings", [])
        return rankings
    return[]


def fetch_all_data():
    competitions = fetch_competitions()
    time.sleep(1)
    
    complexes = fetch_complexes()
    time.sleep(1)
    
    rankings = fetch_rankings()
 
    return {
        "competitions": competitions,
        "complexes": complexes,
        "rankings": rankings
    }
 
 
if __name__ == "__main__":
    data = fetch_all_data()
    print("Type:", type(data))
    print(data)
    


         
    
   
 


