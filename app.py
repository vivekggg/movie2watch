import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
import requests

with st.sidebar:
    selectedmenu=option_menu(
        menu_title="Main Menu",
        options=["Home","Projects","Contacts"],
        default_index=0,
        orientation="horizontal",
    )
if selectedmenu=="Home":
    def fetch_posters(movie_id):
        try:
            response = requests.get(
                f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=cf6b9abd89d5c0bff0a66c4b2a50feea&language=en-US'
            )
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
        except Exception:
            return "https://via.placeholder.com/500x750?text=No+Image"

    def recommended(movie):
        movie_index = movies[movies['title']==movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id
            
            recommended_movies.append(movies.iloc[i[0]].title)
            #fetch poster from API
            recommended_movies_posters.append(fetch_posters(movie_id))
        return recommended_movies, recommended_movies_posters

    movies_dict =pickle.load(open('movies_dict.pkl','rb'))
    movies =pd.DataFrame(movies_dict)

    similarity = pickle.load(open('similarity.pkl','rb'))

    st.title('Movie Recommender System')

    selected_movie_name = st.selectbox('How would you like to be contacted?', movies['title'].values)

    if st.button('Recommend'):
        name, posters = recommended(selected_movie_name)
        # Filter out movies with placeholder images
        filtered = [(n, p) for n, p in zip(name, posters) if "via.placeholder.com" not in p]
        cols = st.columns(len(filtered))
        for idx, (movie_name, poster_url) in enumerate(filtered):
            with cols[idx]:
                st.text(movie_name)
                st.image(poster_url)

elif selectedmenu == "Projects":
    st.title("My Projects")
    st.markdown("""
    - 🎬 Movie Recommender System
    """)

elif selectedmenu == "Contacts":
    st.title("Contact Me")
    st.markdown("""
    - 📧 Email: cinecuco@gmail.com
    """)                

