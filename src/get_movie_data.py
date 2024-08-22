"""Get data about movies from cinemagia.ro"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from typing import List, Dict

__author__ = "Marius Ciurea"
__maintainer = __author__

__email__ = "marius.ciurea@itschool.ro"


p = Path(__file__).parent.parent
URL = "https://www.cinemagia.ro/filme/"
DATA_DIR = p / "data"


class CinemagiaScraper:
    """
    A class to scrape movie information from Cinemagia website.

    Attributes:
        num_pages (int): Number of pages to scrape.
        movies (List[Dict[str, str]]): List to store movie information.
    """

    def __init__(self, num_pages: int):
        """
        Initializes the CinemagiaScraper with the number of pages to scrape.

        Args:
            num_pages (int): The number of pages to scrape.
        """
        self.url = URL
        self.num_pages = num_pages
        self.movies = []

    def fetch_page(self, page_number: int):
        """
        Fetches the HTML content of a given page number.

        Args:
            page_number (int): The page number to fetch.

        Returns:
            Optional[str]: The HTML content of the page, or None if the request failed.
        """
        payload = {"pn": page_number}
        try:
            response = requests.get(self.url, params=payload)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page {page_number}: {e}")
            return None

    @staticmethod
    def parse_movie_data(html: str):
        """
        Parses the HTML content and extracts movie data.

        Args:
            html (str): The HTML content of the page.

        Returns:
            List[Dict[str, float]]: A list of dictionaries containing movie information.
        """
        soup = BeautifulSoup(html, 'lxml')
        movie_elements = soup.find_all('li', class_='movie')  # Adjust selector based on actual HTML structure
        # print(len(movie_elements))
        movies = []
        for element in movie_elements:

            title = element.find('div', class_='title').text.strip() if element.find('div', class_='title') else 'N/A'
            imdb_rating = element.find('a', class_='rating-imdb').text.strip() if element.find(
                'a', class_='rating-imdb') else 'N/A'
            if imdb_rating != 'N/A':
                imdb_rating = imdb_rating.split(':')[1]
            cast = element.find('ul', class_='cast').find_all('li')

            actors, directed, genre = 'N/A', 'N/A', 'N/A'

            for data in cast:
                if 'Cu' in data.text:
                    actors = data.text.strip()
                elif 'Regia' in data.text:
                    directed = data.text.strip()
                elif 'Gen film' in data.text:
                    genre = data.text.strip()
            movies.append({
                'title': title,
                'imdb_rating': imdb_rating,
                'Regia': directed,
                'Actors': actors,
                'Genre': genre,
            }),

        return movies

    def scrape(self):
        """
        Scrapes the specified number of pages and aggregates the movie data.
        """
        for page in range(1, self.num_pages + 1):
            html = self.fetch_page(page)
            if html:
                movies = self.parse_movie_data(html)
                self.movies.extend(movies)

    def get_movies(self) -> pd.DataFrame:
        """
        Returns the aggregated movie data.

        Returns:
            pd.DataFrame: A pandas DataFrame containing movie information.
        """
        return pd.DataFrame(self.movies)


if __name__ == "__main__":
    num_pages = 10
    scraper = CinemagiaScraper(num_pages)
    scraper.scrape()
    movies = scraper.get_movies()
    movies.to_csv('test.csv')
