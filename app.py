import streamlit as st
import pandas as pd
import requests
import pickle
from decouple import config


key = config('API')


similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie}?api_key={key}&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']
def fetch_link(movie):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie}?api_key={key}&language=en-US')
    data = response.json()
    return data['homepage']


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),
                         reverse=True, key=lambda x: x[1])[1:7]
    recommend_movies = []
    recommend_movies_poster = []
    links = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0], :].id
        recommend_movies.append(movies_df.iloc[i[0], :].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
        links.append(fetch_link(movie_id))
    return recommend_movies, recommend_movies_poster,links


st.title('Movie Recommender System')
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)
movies_list = movies_df['title'].values
selected_movie_name = st.selectbox('Select Your Fav Movie', movies_list)
if st.button('Recommend'):
    names, poster,links = recommend(selected_movie_name)
    col1, col2 = st.columns(2)
    with col1:

        st.markdown(
            f"<h3 style='text-align: center; color:#fafafa; '>{names[0]}</h3>", unsafe_allow_html=True)
        st.image(poster[0])
  
    with col2:
        st.markdown(
            f"<h3 style='text-align: center; color:#fafafa; '>{names[1]}</h3>", unsafe_allow_html=True)

        st.image(poster[1])
    with col1:
        st.markdown(
            f"<h3 style='text-align: center; color:#fafafa; '>{names[2]}</h3>", unsafe_allow_html=True)

        st.image(poster[2])
    with col2:
        st.markdown(
            f"<h3 style='text-align: center; color:#fafafa; '>{names[3]}</h3>", unsafe_allow_html=True)
        st.image(poster[3])
    with col1:
        st.markdown(
            f"<h3 style='text-align: center; color:#fafafa; '>{names[4]}</h3>", unsafe_allow_html=True)
        st.image(poster[4])
    with col2:
        st.markdown(
            f"<h3 style='text-align: center; color:#fafafa; '>{names[5]}</h3>", unsafe_allow_html=True)
        st.image(poster[5])
