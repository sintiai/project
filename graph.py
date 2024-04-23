import matplotlib.pyplot as plt
import pandas as pd

def graph_spotify():
    df = pd.read_csv('spotify_calculations.csv')
    df.plot.bar(x='Artist Name', y='Average Rating', color='pink')
    plt.show()

def graph_imdb():
    df = pd.read_csv('imdb_calculations.csv')
    df.plot.bar(x='Description', y='Average Rating', color='pink')
    plt.show()

def genre_imdb():
    df = pd.read_csv('genre_calculations.csv')
    df.plot.bar(x='Genre', y='Average Rating', color='blue')
    plt.title('Average IMDb Rating by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Average Rating')
    plt.show()

#def movie_count():


def main():
    graph_spotify()
    graph_imdb()
    genre_imdb()


if __name__ == "__main__":
    main() 