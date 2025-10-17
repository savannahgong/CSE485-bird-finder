import requests
import json
from typing import List, Dict, Any
from requests.exceptions import RequestException

def get_recent_observations(region_code='US-CA', max_results=10):
    """
    Fetches recent bird observations from the eBird API for a specified region.
    """
    api_token = 'a3e6ct65n6dl'
    url = f'https://api.ebird.org/v2/data/obs/{region_code}/recent'
    
    headers = {
        'X-eBirdApiToken': api_token
    }
    
    params = {
        'maxResults': max_results
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def display_observations(observations):
    """
    Displays the list of bird observations in a user-friendly format.
    """
    if not observations:
        print("No observations found.")
        return
    
    for i, obs in enumerate(observations, 1):
        print(f"{i}. {obs.get('comName')}\n")

def main():
    print("Welcome to the eBird Bird Finder!")
    
    region = 'US-CA'
    observations = get_recent_observations(region_code=region, max_results=15)
    
    if observations:
        display_observations(observations)
        
        # let user pick a bird for more details
        try:
            choice = int(input("Enter the number of a bird to see more details (or 0 to exit): "))
            if 1 <= choice <= len(observations):
                selected_bird = observations[choice - 1]
                print(f"\n=== Detailed Information ===")
                print(f"Common Name: {selected_bird.get('comName')}")
                print(f"Scientific Name: {selected_bird.get('sciName')}")
                print(f"Location: {selected_bird.get('locName')}")
                print(f"Date Observed: {selected_bird.get('obsDt')}")
                print(f"Quantity: {selected_bird.get('howMany', 'N/A')}\n")

                main() # restart to allow another selection
        except ValueError:
            print("Invalid input. Exiting.")
    else:
        print("Failed to retrieve data. Please check your API key and region code.")

if __name__ == "__main__":
    main()
