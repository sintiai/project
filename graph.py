import matplotlib.pyplot as plt
import pandas as pd

#graph for calculate_average_popularity_by_artist
def graph_spotify():
    df = pd.read_csv('spotify_calculations.csv')
    df.plot.bar(x='Artist Name', y='Average Rating', color='pink')
    plt.show()

#graph for calculate_average_imdb_rating
def graph_imdb():
    df = pd.read_csv('imdb_calculations.csv')
    df.plot.bar(x='Description', y='Average Rating', color='pink')
    plt.show()
#graph for calculate_movie_count_by_genre
def genre_imdb():
    df = pd.read_csv('genre_calculations.csv')
    df.plot.bar(x='Genre', y='Average Rating', color='blue')
    plt.title('Average IMDb Rating by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Average Rating')
    plt.show()


def main():
    graph_spotify()
    graph_imdb()
    genre_imdb()


if __name__ == "__main__":
    main() 