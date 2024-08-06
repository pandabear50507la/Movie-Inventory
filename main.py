from utils.csv_utils import initialize_csv, add_movie, view_movies, search_movie, delete_movie, update_movie, suggest_shelf_position
from utils.omdb_utils import search_movies_by_title, fetch_movie_details
from utils.title_utils import format_title_for_storage, normalize_title_for_search

def main():
    initialize_csv()
    while True:
        print("\nMovie Collection Inventory")
        print("1. Add Movie by Title")
        print("2. Delete Movie")
        print("3. View Movies")
        print("4. Search Movie")
        print("5. Update Movie")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter movie title: ")
            print(f"Searching for movies with title: {title}")
            movies = search_movies_by_title(title)
            if movies:
                print("Select the correct movie by entering the corresponding number:")
                for idx, movie in enumerate(movies):
                    print(f"{idx + 1}. {movie['Title']} ({movie['Year']})")
                selection = input("Enter number: ")
                try:
                    selected_movie = movies[int(selection) - 1]
                    print(f"Fetching details for IMDb ID: {selected_movie['imdbID']}")
                    movie_details = fetch_movie_details(selected_movie['imdbID'])
                    if movie_details:
                        formatted_title = format_title_for_storage(movie_details['Title'])
                        add_movie(movie_details, formatted_title)
                    else:
                        print("Movie details not found.")
                except (IndexError, ValueError):
                    print("Invalid selection.")
            else:
                print("No movies found with that title.")
        elif choice == '2':
            title = input("Enter the title of the movie to delete: ")
            delete_movie(title)
        elif choice == '3':
            view_movies()
        elif choice == '4':
            title = input("Enter title to search: ")
            search_movie(title, normalize_title_for_search)
        elif choice == '5':
            title = input("Enter title to update: ")
            update_movie(title)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()