import pickle
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load movie data and similarity matrix
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Streamlit app configuration
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6 !important;
        font-family: 'Arial', sans-serif !important;
        padding: 12rem 12rem !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    .main-container {
        width: 60% !important;
        margin: auto !important;
        text-align: center !important;
    }
    img.movie-poster {
        border-radius: 15px !important;
        transition: transform 0.3s !important;
    }
    img.movie-poster:hover {
        transform: scale(1.05) !important;
    }
    .title {
        font-weight: 500 !important;
        margin-top: 20px !important;
        font-size: 25px !important;
        text-align: center !important;
    }
    .custom-text-1 {
        font-size: 30px !important;
        font-family: 'Verdana', sans-serif !important;
    }
    .custom-text {
        font-size: 20px !important;
        font-family: 'Verdana', sans-serif !important;
    }
    .stSelectbox {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #A067FA !important;
        border-radius: 10px !important;
        padding: 2px !important;
    }
    .stButton > button {
        margin-top: 10px !important;
        transition: background-color 0.3s !important;
        padding: 10px 20px !important;
        font-size: 20px !important;
    }
    .stButton > button:hover {
        background-color: #A067FA !important;
        color: #FFFFFF !important;
    }
    .stButton > button:active {
        background-color: #A067FA !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.title("🎬 Movie Recommendation System")
st.markdown("<p class='custom-text-1'>This is a content-based movie recommendation system done by machine learning</p>", unsafe_allow_html=True)

st.markdown("<p class='custom-text'>Select a movie to get personalized recommendations!</p>", unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie:',
    movie_list,
    key="movie_select"
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, os.getenv('TMDB_API_KEY'))
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    return "http://image.tmdb.org/t/p/w500" + poster_path if poster_path else "https://via.placeholder.com/500"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_names = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_names, recommended_movies_posters

if st.button('Show Recommendations'):
    recommended_movies_names, recommended_movies_posters = recommend(selected_movie)
    
    st.write("## Recommended Movies")
    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]
    for i, col in enumerate(columns):
        with col:
            # Wrap the image in an HTML div for applying custom CSS class
            st.markdown(f"""
                <div>
                    <img src="{recommended_movies_posters[i]}" class="movie-poster" style="width: 100%;">
                    <p class="title">{recommended_movies_names[i]}</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
