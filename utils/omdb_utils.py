import requests
OMDB_API_KEY = 'INSERT KEY HERE'
OMDB_API_URL = 'http://www.omdbapi.com/'

def search_movies_by_title(title):
    params = {
        'apikey': OMDB_API_KEY,
        's': title
    }
    print(f"Searching OMDb for title: {title} with API key: {OMDB_API_KEY}")
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return data['Search']
    return None

def fetch_movie_details(imdb_id):
    params = {
        'apikey': OMDB_API_KEY,
        'i': imdb_id
    }
    print(f"Fetching details for IMDb ID: {imdb_id} with API key: {OMDB_API_KEY}")
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        movie_data = response.json()
        if movie_data['Response'] == 'True':
            return {
                'Title': movie_data['Title'],
                'Year': movie_data['Year'],
                'Genre': movie_data['Genre'],
                'Director': movie_data['Director'],
                'IMDb ID': movie_data['imdbID'],
                'Poster': movie_data.get('Poster', 'No poster available'),
                'Runtime': movie_data.get('Runtime', 'N/A'),  # Add Runtime
                'Rating': movie_data.get('Ratings', [{'Value': 'N/A'}])[0]['Value']  # Add Rating
            }
    return None
