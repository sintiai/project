import sqlite3
import csv

def calculate_average_imdb_rating():
    conn = sqlite3.connect('combined.db')
    c = conn.cursor()
    c.execute("SELECT AVG(CAST(imdb_rating AS REAL)) FROM movies")
    average_rating = c.fetchone()[0]
    conn.close()
    return average_rating

def calculate_average_popularity_by_genre():
    conn = sqlite3.connect('combined.db')
    c = conn.cursor()
    c.execute("SELECT genre, AVG(CAST(imdb_rating AS REAL)) FROM movies GROUP BY genre")
    average_popularity_by_genre = c.fetchall()
    conn.close()
    return average_popularity_by_genre

def calculate_movie_count_by_genre():
    conn = sqlite3.connect('combined.db')
    c = conn.cursor()
    c.execute("SELECT genre, COUNT(*) FROM movies GROUP BY genre")
    movie_count_by_genre = c.fetchall()
    conn.close()
    return movie_count_by_genre

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
            file.write(f"{item}\n")

def main():
    # average IMDb rating
    average_imdb_rating = calculate_average_imdb_rating()
    print(average_imdb_rating)
    #print(f"Average IMDb Rating: {average_imdb_rating:.2f}")

    # average popularity by artist
    average_popularity_by_artist = calculate_average_popularity_by_artist()
    print(average_popularity_by_artist)
    with open('spotify_calculations.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        title = ('Artist Name', 'Average Rating')
        writer.writerow(title)
        for row in average_popularity_by_artist:
            writer.writerow(row)
    
    # Write data to text files dynamically
    #write_to_file([(f"Average IMDb Rating: {average_imdb_rating:.2f}")], 'average_imdb_rating.txt')
    #write_to_file([(f"{artist}: {average_popularity:.2f}") for artist, average_popularity in average_popularity_by_artist], 'average_popularity_by_artist.txt')

    average_rating_by_genre = calculate_average_popularity_by_genre()
    print("Average IMDb rating by genre:")
    for genre, average_rating in average_rating_by_genre:
        print(f"{genre}: {average_rating:.2f}")
    with open('genre_calculations.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Genre', 'Average Rating'))
        for row in average_rating_by_genre:
            writer.writerow(row)

    movie_count_by_genre = calculate_movie_count_by_genre()
    print("Movie Count by Genre:")
    for genre, count in movie_count_by_genre:
        print(f"{genre}: {count}")
    with open('genre_movie_count.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Genre', 'Movie Count'))
        for row in movie_count_by_genre:
            writer.writerow(row)

    with open('imdb_calculations.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Description', 'Average Rating'))
        writer.writerow(('Avergage IMDB Rating', average_imdb_rating))

if __name__ == "__main__":
    main()

    