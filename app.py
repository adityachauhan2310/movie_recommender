import streamlit as st
import pickle
import pandas as pd
import requests

OMDB_API_KEY = "c9b88354"

def get_movie_poster(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Poster") and response["Poster"] != "N/A":
        return response["Poster"]

    return "https://via.placeholder.com/300x450?text=No+Image+Available"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        poster_url = get_movie_poster(movie_title)  # Fetch poster from OMDb
        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters

# Load Data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie_name)

    cols = st.columns(5)  # Create 5 columns for posters
    for idx, movie in enumerate(recommendations):
        with cols[idx]:
            st.image(posters[idx], caption=movie, use_container_width=True)
