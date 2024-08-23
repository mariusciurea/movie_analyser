import streamlit as st
from src.get_movie_data import CinemagiaScraper

st.title("Movie Analyzer")


def clean_movies_data(df):
    """Clean up the movies DataFrame by filtering out invalid ratings and converting data types."""
    df = df[df['imdb_rating'].str.strip() != '0']
    df['imdb_rating'] = df['imdb_rating'].astype(float)
    return df


def display_movie_statistics(df):
    """Display movie statistics using Streamlit metrics."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Number of movies", len(df))
    col2.metric("Average rating", f'{df["imdb_rating"].mean():.2f}')
    col3.metric("Movies over 8", len(df[df['imdb_rating'] >= 8]))
    movies_over_9 = df[df['imdb_rating'] >= 9]
    col4.metric("Movies over 9", len(movies_over_9))


with st.sidebar:
    number_of_pages = st.number_input("Please insert the number of pages")
    filter_button = st.button("Filter", type="primary")

if number_of_pages and filter_button:
    scraper = CinemagiaScraper(int(number_of_pages))
    scraper.scrape()
    movies = scraper.get_movies()
    movies = clean_movies_data(movies)
    display_movie_statistics(movies)
    st.table(movies)
