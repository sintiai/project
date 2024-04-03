import requests
from bs4 import BeautifulSoup

def scrape_billboard_artist_100(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        artist_elements = soup.find_all('span', class_='chart-list-item__title-text')
        rank_elements = soup.find_all('span', class_='chart-list-item__rank')
        artists = [(rank.text.strip(), artist.text.strip()) for rank, artist in zip(rank_elements, artist_elements)]
        return artists
    else:
        print('Failed to retrieve data from the website')
        return None

def query_seatgeek_api(artists):
    for rank, artist in artists:
        query = artist.replace(" ", "-")
        url = f"https://api.seatgeek.com/2/events?q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for event in data["events"]:
                print(f"Artist: {artist}, Location: {event['venue']['city']}, Date: {event['datetime_local']}")
        else:
            print(f"Failed to retrieve data from SeatGeek for artist: {artist}")

billboard_url = 'https://www.billboard.com/charts/artist-100/'
artists_data = scrape_billboard_artist_100(billboard_url)

if artists_data:
    query_seatgeek_api(artists_data)