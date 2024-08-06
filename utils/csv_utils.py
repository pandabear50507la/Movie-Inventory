import csv
from datetime import datetime
from utils.title_utils import format_title_for_storage

MOVIE_CSV = 'movies.csv'

def initialize_csv():
    """Initialize the CSV file with headers if it doesn't exist."""
    try:
        with open(MOVIE_CSV, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Year', 'Genre', 'Director', 'IMDb ID', 'Date Added', 'Barcode', 'Runtime', 'Poster', 'Rating'])
            print("CSV file created with headers.")
    except FileExistsError:
        print("CSV file already exists. No need to initialize.")

def add_movie(movie_details, formatted_title):
    """Add a movie to the CSV file."""
    barcode = input("Enter movie barcode (or press Enter to skip): ")
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Ensure that 'suggest_shelf_position' is defined and works as expected
    position = suggest_shelf_position(formatted_title)
    
    print(f"Suggested shelf position for '{formatted_title}': {position}")
    
    print(f"Adding movie with details: {movie_details}, formatted title: {formatted_title}, date added: {date_added}, barcode: {barcode}")
    with open(MOVIE_CSV, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            formatted_title, 
            movie_details['Year'], 
            movie_details['Genre'], 
            movie_details['Director'],
            movie_details['IMDb ID'],
            date_added,
            barcode,
            movie_details['Runtime'],
            movie_details['Poster'],
            movie_details.get('Rating', 'N/A')  # Rating is handled here
        ])
    print(f'Movie "{formatted_title}" added to the collection.')

def delete_movie(title, filename='movies.csv'):
    rows = []
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    rows = [row for row in rows if row['Title'] != title]
    
    with open(filename, 'w', newline='') as file:
        fieldnames = ['Title', 'Year', 'Genre', 'Director', 'IMDb ID', 'Date Added', 'Barcode', 'Runtime', 'Poster']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Deleted movie with title: {title}")

def view_movies():
    try:
        with open(MOVIE_CSV, newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)
            rows.sort(key=lambda row: row[0].lower())  # Sort by title
            
            # Print header
            print("Movie Collection Inventory")
            print("-" * 50)
            
            # Print rows
            for idx, row in enumerate(rows, start=1):
                print(f"{idx}.")
                print(f"  Title: {row[0]}")
                print(f"  Year: {row[1]}")
                print(f"  Genre: {row[2]}")
                print(f"  Director: {row[3]}")
                print(f"  IMDb ID: {row[4]}")
                print(f"  Date Added: {row[5]}")
                
                # Handle missing columns gracefully
                if len(row) > 6:
                    print(f"  Barcode: {row[6]}")
                else:
                    print("  Barcode: N/A")
                
                if len(row) > 7:
                    print(f"  Runtime: {row[7]}")
                else:
                    print("  Runtime: N/A")
                
                if len(row) > 8:
                    print(f"  Poster: {row[8]}")
                else:
                    print("  Poster: N/A")
                
                if len(row) > 9:
                    print(f"  Rating: {row[9]}")
                else:
                    print("  Rating: N/A")
                
                print("-" * 50)  # Separator line
    except FileNotFoundError:
        print(f"File '{MOVIE_CSV}' not found. Please make sure the CSV file exists.")

def remove_copy(title, filename='movies.csv'):
    rows = []
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    # Create a new list without the first occurrence of the title to be removed
    rows_to_keep = []
    title_found = False
    for row in rows:
        if row['Title'] == title and not title_found:
            title_found = True  # Skip only the first occurrence of the title
        else:
            rows_to_keep.append(row)
    
    with open(filename, 'w', newline='') as file:
        fieldnames = ['Title', 'Year', 'Genre', 'Director', 'IMDb ID', 'Date Added', 'Barcode', 'Runtime', 'Poster']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_to_keep)
    
    print(f"Removed one copy of movie with title: {title}")

def search_movie(title, normalized_title_for_search):
    normalized_title = normalized_title_for_search(title)
    print(f"Searching for title: {title}, normalized for search: {normalized_title}")
    try:
        with open(MOVIE_CSV, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            found = False
            for idx, row in enumerate(reader, start=1):
                stored_title = row[0].lower()
                if normalized_title in normalized_title_for_search(stored_title):
                    print(f"{idx}.")
                    print(f"  Title: {row[0]}")
                    print(f"  Year: {row[1]}")
                    print(f"  Genre: {row[2]}")
                    print(f"  Director: {row[3]}")
                    print(f"  IMDb ID: {row[4]}")
                    print(f"  Date Added: {row[5]}")
                    print(f"  Barcode: {row[6]}")
                    print(f"  Runtime: {row[7]}")
                    print(f"  Poster: {row[8]}")
                    print(f"  Rating: {row[9]}")
                    print("-" * 40)  # Separator line
                    found = True
            if not found:
                print(f'No movies found with title containing "{title}".')
    except FileNotFoundError:
        print(f"File '{MOVIE_CSV}' not found. Please make sure the CSV file exists.")

def update_movie(title):
    try:
        with open(MOVIE_CSV, newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    except FileNotFoundError:
        print("Movie CSV file not found.")
        return

    for idx, row in enumerate(rows):
        if row['Title'] == title:
            print(f"Updating movie: {title}")
            new_title = input(f"Enter new title (leave blank to keep '{row['Title']}'): ") or row['Title']
            new_year = input(f"Enter new year (leave blank to keep '{row['Year']}'): ") or row['Year']
            new_genre = input(f"Enter new genre (leave blank to keep '{row['Genre']}'): ") or row['Genre']
            new_director = input(f"Enter new director (leave blank to keep '{row['Director']}'): ") or row['Director']
            new_imdb_id = input(f"Enter new IMDb ID (leave blank to keep '{row['IMDb ID']}'): ") or row['IMDb ID']
            new_barcode = input(f"Enter new barcode (leave blank to keep '{row['Barcode']}'): ") or row['Barcode']
            new_runtime = input(f"Enter new runtime (leave blank to keep '{row['Runtime']}'): ") or row['Runtime']
            new_poster = input(f"Enter new poster URL (leave blank to keep '{row['Poster']}'): ") or row['Poster']
            new_rating = input(f"Enter new rating (leave blank to keep '{row['Rating']}'): ") or row['Rating']
            new_date_added = row['Date Added']

            # Update the row in memory
            rows[idx] = {
                'Title': new_title,
                'Year': new_year,
                'Genre': new_genre,
                'Director': new_director,
                'IMDb ID': new_imdb_id,
                'Date Added': new_date_added,
                'Barcode': new_barcode,
                'Runtime': new_runtime,
                'Poster': new_poster,
                'Rating': new_rating
            }
            break
    else:
        print(f"No movie found with title '{title}'")
        return

    # Write the updated rows back to the CSV
    with open(MOVIE_CSV, 'w', newline='') as file:
        fieldnames = ['Title', 'Year', 'Genre', 'Director', 'IMDb ID', 'Date Added', 'Barcode', 'Runtime', 'Poster', 'Rating']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Movie '{title}' updated to '{new_title}'")

    
# Make sure to include the necessary functions
def suggest_shelf_position(new_title, filename='movies.csv'):
    """Suggest where to place a new movie on the shelf based on its title."""
    titles = []
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            titles = [row['Title'] for row in reader]
    except FileNotFoundError:
        print(f"File '{filename}' not found. Suggesting position may not be accurate.")
    
    titles.sort(key=lambda t: t.lower())
    
    for i, title in enumerate(titles):
        if new_title.lower() < title.lower():
            return i + 1  # Position after index
    
    return len(titles) + 1  # Append to the end if not found