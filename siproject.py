import requests
import sqlite3
   
# Create or connect to the SQLite database
conn = sqlite3.connect('combined.db')
c = conn.cursor()

# Create movies table
c.execute('''CREATE TABLE IF NOT EXISTS movies
             (id INTEGER PRIMARY KEY,
              title TEXT UNIQUE,
              year TEXT,
              imdb_rating TEXT,
              genre TEXT)''') 

# List of movie titles
movies = ["Barbie",
          "Home Alone",
          "3 Idiots",
          "Spy Kids",
          "Flipped",
          "The Godfather",
          "The Shawshank Redemption",
          "Pulp Fiction",
          "The Dark Knight",
          "Schindler's List",
          "Forrest Gump",
          "The Lord of the Rings: The Return of the King",
          "Fight Club",
          "Inception",
          "The Matrix",
          "The Silence of the Lambs",
          "Star Wars: Episode V - The Empire Strikes Back",
          "Goodfellas",
          "The Lord of the Rings: The Fellowship of the Ring",
          "The Lord of the Rings: The Two Towers",
          "The Green Mile",
          "The Godfather: Part II",
          "Se7en",
          "The Usual Suspects",
          "The Lion King",
          "Gladiator",
          "Saving Private Ryan",
          "The Departed",
          "The Prestige",
          "The Pianist",
          "The Dark Knight Rises",
          "The Avengers",
          "Titanic",
          "Jurassic Park",
          "The Terminator",
          "The Truman Show",
          "Back to the Future",
          "Ghostbusters",
          "Shershaah",
          "Good Will Hunting",
          "Braveheart",
          "The Shining",
          "Psycho",
          "The Sixth Sense",
          "The Exorcist",
          "A Clockwork Orange",
          "American History X",
          "The Good, the Bad and the Ugly",
          "A Fistful of Dollars",
          "For a Few Dollars More",
          "Unforgiven",
          "No Country for Old Men",
          "Fargo",
          "The Big Lebowski",
          "O Brother, Where Art Thou?",
          "True Grit",
          "The Revenant",
          "Birdman or (The Unexpected Virtue of Ignorance)",
          "The Grand Budapest Hotel",
          "Moonrise Kingdom",
          "The Royal Tenenbaums",
          "Fantastic Mr. Fox",
          "Isle of Dogs",
          "Reservoir Dogs",
          "Jackie Brown",
          "Kill Bill: Vol. 1",
          "Kill Bill: Vol. 2",
          "Death Proof",
          "Django Unchained",
          "The Hateful Eight",
          "Once Upon a Time in Hollywood",
          "Spirited Away",
          "My Neighbor Totoro",
          "Princess Mononoke",
          "Howl's Moving Castle",
          "Ponyo",
          "Castle in the Sky",
          "Kiki's Delivery Service",
          "Nausicaä of the Valley of the Wind",
          "Porco Rosso", 
          " Lagaan ", 
          " Dilwale Dulhania Le Jayenge ", 
          " 3 Idiots ", 
          " PK ", 
          " Gully Boy ", 
          " Queen ", 
          " Taare Zameen Par ", 
          " Zindagi Na Milegi Dobara ", 
          " Dangal ",
          " Swades ", 
          " Rang De Basanti ", 
          " Barfi! ", 
          " Andhadhun ", 
          " Mughal-E-Azam ",
          " Chak De! India ", 
          " Kahaani ", 
          " Dil Chahta Hai ",
          " Gangs of Wasseypur ",
          " Bajrangi Bhaijaan ", 
          " Kabhi Khushi Kabhie Gham ", 
          " Vicky Donor ",
          " Om Shanti Om ", 
          " My Name Is Khan ", 
          " Devdas "]

# API key
api_key = "524429c9"  # Remember to replace this with your actual API key

# Iterate through the list of movies
for movie in movies:
    # Replace spaces with %20 for URL encoding
    encoded_title = "+".join(movie.split())
    
    # Construct the API URL
    api_url = f"http://www.omdbapi.com/?t={encoded_title}&apikey=524429c9"
    
    # Send a GET request to the API
    response = requests.get(api_url)
    
    # Parse the JSON response
    data = response.json()
    
    # Check if data is retrieved successfully
    if data.get('Response') == 'True':
        # Extract relevant information
        title = data.get('Title')
        year = data.get('Year')
        imdb_rating = data.get('imdbRating')
        genre = data.get('Genre')
        
        # Insert data into the database, ignoring duplicates
        c.execute('''INSERT OR IGNORE INTO movies (title, year, imdb_rating, genre) 
                     VALUES (?, ?, ?, ?)''', (title, year, imdb_rating, genre))
    else:
        print(f"Failed to retrieve data for {movie}")

    # Commit the changes to the database
    conn.commit()

# Fetch the first 5 movies from the database
c.execute("SELECT * FROM movies LIMIT 5")
first_five_movies = c.fetchall()


def create_database():
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, 'combined.db')
    conn = sqlite3.connect(full_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies (
                 id INTEGER PRIMARY KEY,
                 title TEXT UNIQUE,
                 year TEXT,
                 imdb_rating TEXT,
                 genre TEXT)''')   
    conn.commit()
    conn.close()

# Print the details of the first 5 movies just for funzies
for movie in first_five_movies:
    print(f"Title: {movie[1]}")
    print(f"Year: {movie[2]}")
    print(f"IMDB Rating: {movie[3]}")
    print(f"Genre: {movie[4]}")
    print("\n")


conn.close()

#his is for a test