import sqlite3

def calculate_average_imdb_rating():
    conn = sqlite3.connect('combined.db')
    c = conn.cursor()
    c.execute("SELECT AVG(CAST(imdb_rating AS REAL)) FROM movies")
    average_rating = c.fetchone()[0]
    conn.close()
    return average_rating

def calculate_average_popularity_by_artist():
    conn = sqlite3.connect('combined.db')
    c = conn.cursor()
    c.execute("SELECT Artists.artist_name, AVG(TopTracks.popularity) FROM TopTracks JOIN Artists ON TopTracks.artist_id = Artists.artist_id GROUP BY Artists.artist_name")
    average_popularity_by_artist = c.fetchall()
    conn.close()
    return average_popularity_by_artist

def write_to_file(data, filename):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item[0]}: {item[1]:.2f}\n")

def main():
    # average IMDb rating
    average_imdb_rating = calculate_average_imdb_rating()
    print(f"Average IMDb Rating: {average_imdb_rating:.2f}")

    #  average popularity by artist
    average_popularity_by_artist = calculate_average_popularity_by_artist()
    print("\nAverage Popularity by Artist:")
    for artist, average_popularity in average_popularity_by_artist:
        print(f"{artist}: {average_popularity:.2f}")

    # Write data to text files
    write_to_file([(f"Average IMDb Rating", average_imdb_rating)], 'average_imdb_rating.txt')
    write_to_file(average_popularity_by_artist, 'average_popularity_by_artist.txt')

if __name__ == "__main__":
    main()