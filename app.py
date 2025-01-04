import pickle
import streamlit as st
import requests
from dotenv import load_dotenv
import os

st.header("Movie Recommendation System Using Machine Learning")
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Load environment variables from .env file
load_dotenv()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendations',
    movie_list
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, os.getenv('TMDB_API_KEY'))
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    poster = "http://image.tmdb.org/t/p/w500" + poster_path
    return poster

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])
    recommended_movies_names = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies_names, recommended_movies_posters


if st.button('Show recommendation'):
    recommended_movies_names, recommnded_movies_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_names[0])
        st.image(recommnded_movies_posters[0])
    with col2:
        st.text(recommended_movies_names[1])
        st.image(recommnded_movies_posters[1])
    with col3:
        st.text(recommended_movies_names[2])
        st.image(recommnded_movies_posters[2])
    with col4:
        st.text(recommended_movies_names[3])
        st.image(recommnded_movies_posters[3])
    with col5:
        st.text(recommended_movies_names[4])
        st.image(recommnded_movies_posters[4])
        