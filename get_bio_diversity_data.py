import requests
import pandas as pd

def get_bio_diversity_data(lat, lon):
    # API endpoint and parameters
    api_url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        "decimalLatitude": f"{lat},{lat + 0.0300}",
        "decimalLongitude": f"{lon},{lon + 0.0300}",
        "limit": 300
    }
    
    # Fetch data
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = pd.json_normalize(data['results'])

        # Total species
        total_species = results['species'].nunique()

        # Total animals
        total_animals = results[results['kingdom'] == 'Animalia'].shape[0]

        # Total plants
        total_plants = results[results['kingdom'] == 'Plantae'].shape[0]

        # Endangered species (mock example, needs IUCN cross-reference)
        endangered_species = results[results['threatStatus'] == 'Endangered'] if 'threatStatus' in results.columns else pd.DataFrame()

        # Protected species (mock example, needs external cross-reference or metadata filtering)
        protected_species = results[results['speciesKey'].notnull() & (results['basisOfRecord'].str.contains('preserved|observation', na=False))]

        # Print results
        results = {
            "total_species" : total_species,
            "total_animals" : total_animals,
            "Total Plants" : total_plants,
            "Endangered Species" : len(endangered_species),
            "Protected Species" : protected_species['species'].nunique() if not protected_species.empty else 0
        }
        return results
    else:
        print(f"Error: {response.status_code}")

# Example usage
# get_bio_diversity_data(40.6300, -74.0300)
