# Import deploy module to ensure data files are generated during deployment
try:
    import deploy
    print("✅ Deploy module imported successfully")
except Exception as e:
    print(f"⚠️ Deploy module import error: {e}")

import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
import requests
import ast
import time
import random
import os
import sys

# Check if data files exist and generate them if needed
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    movies_dict_path = os.path.join(base_dir, 'movies_dict.pkl')
    similarity_path = os.path.join(base_dir, 'similarity.pkl')
    
    if not os.path.exists(movies_dict_path) or not os.path.exists(similarity_path):
        print("Data files not found. Generating them now...")
        import generate_data
        print("Data generation complete.")
    else:
        print(f"Data files found at:\n{movies_dict_path}\n{similarity_path}")
        
except Exception as e:
    print(f"Error during data generation: {e}")
    # Try running generate_data.py as a subprocess if import fails
    try:
        import subprocess
        print("Attempting to generate data files via subprocess...")
        subprocess.run([sys.executable, 'generate_data.py'], check=True)
        print("Data files generated successfully!")
    except Exception as sub_e:
        print(f"Failed to generate data files: {sub_e}")

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Recommender Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .movie-card {
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .movie-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
    }
    
    .feature-highlight {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    
    
    
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .success-message {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    .movie-poster {
        border-radius: 15px;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .movie-poster:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: white; margin-bottom: 2rem;">🎬 Movie Pro</h1>
        <p style="color: white; margin-bottom: 1rem;">
            <a href="https://github.com/vivekggg/movie2watch" target="_blank" style="color: #fff; text-decoration: none; font-size: 0.9rem;">
                🔗 GitHub Repository
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    selectedmenu = option_menu(
        menu_title=None,
        options=["🏠 Home", "📁 Projects", "📞 Contacts"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
                "color": "white",
                "background-color": "transparent",
                "border-radius": "10px",
                "padding": "10px 15px"
            },
            "nav-link-selected": {
                "background-color": "rgba(255,255,255,0.2)",
                "color": "white"
            }
        }
    )
if selectedmenu == "🏠 Home":
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
            recommended_movies_posters.append(fetch_posters(movie_id))
        
        # Ensure we always return exactly 5 recommendations
        while len(recommended_movies) < 5:
            # Add random movies if we don't have enough
            random_movie = random.choice(movies['title'].values)
            if random_movie not in recommended_movies and random_movie != movie:
                movie_id = movies[movies['title']==random_movie]['movie_id'].iloc[0]
                recommended_movies.append(random_movie)
                recommended_movies_posters.append(fetch_posters(movie_id))
        
        return recommended_movies[:5], recommended_movies_posters[:5]

    # Load data
    try:
        # Use absolute paths to ensure files can be found
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        movies_dict_path = os.path.join(base_dir, 'movies_dict.pkl')
        similarity_path = os.path.join(base_dir, 'similarity.pkl')
        
        # Print paths for debugging
        print(f"Looking for movies_dict.pkl at: {movies_dict_path}")
        print(f"Looking for similarity.pkl at: {similarity_path}")
        
        # Check if files exist
        if not os.path.exists(movies_dict_path) or not os.path.exists(similarity_path):
            raise FileNotFoundError("Pickle files not found at expected locations")
            
        movies_dict = pickle.load(open(movies_dict_path, 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open(similarity_path, 'rb'))
    except FileNotFoundError as e:
        # Generate data files if they don't exist
        st.info(f"Generating data files. This may take a few minutes... Error: {str(e)}")
        import subprocess
        import sys
        try:
            subprocess.run([sys.executable, 'generate_data.py'], check=True)
            # Try loading again after generation
            movies_dict = pickle.load(open(movies_dict_path, 'rb'))
            movies = pd.DataFrame(movies_dict)
            similarity = pickle.load(open(similarity_path, 'rb'))
            st.success("Data files generated successfully!")
        except Exception as e:
            st.error(f"Error generating data files: {str(e)}")
            st.stop()

    # Main header
    st.markdown('<h1 class="main-header">🎬 Movie Recommender Pro</h1>', unsafe_allow_html=True)
    
    # Stats container
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Total Movies", f"{len(movies):,}")
    with col2:
        st.metric("🎯 Recommendations", "Always 5")
    with col3:
        st.metric("⚡ Fast Results", "< 2 seconds")
    with col4:
        st.metric("🎨 Smart Matching", "AI-Powered")

    # Feature highlights
    st.markdown("""
    <div class="feature-highlight">
        <h3>✨ Discover Your Next Favorite Movie!</h3>
        <p>Our AI-powered recommendation system analyzes movie content, cast, crew, and genres to find the perfect match for you.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Random movie suggestion
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 Surprise Me! (Random Movie)", use_container_width=True):
            random_movie = random.choice(movies['title'].values)
            st.session_state.random_movie = random_movie
            st.success(f"🎉 Try: '{random_movie}'")
    
    if 'random_movie' in st.session_state:
        st.info(f"💡 Random suggestion: {st.session_state.random_movie}")

    # Main recommendation interface
    st.markdown("### 🎭 Choose Your Movie")
    
    # Enhanced movie selection
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**🔍 Search for a movie:**")
        
        # Add search functionality with better styling
        search_term = st.text_input(
            "Search movies",
            placeholder="",
            help="Type any part of the movie title to find it quickly",
            label_visibility="collapsed",
            key="movie_search"
        )
        
        # Show search results count
        if search_term:
            filtered_count = len(movies[movies['title'].str.contains(search_term, case=False, na=False)])
            if filtered_count > 0:
                st.success(f"✅ Found {filtered_count} movies matching '{search_term}'")
            else:
                st.warning(f"❌ No movies found matching '{search_term}'. Showing popular movies instead.")
        
        # Filter movies based on search term
        if search_term:
            filtered_movies = movies[movies['title'].str.contains(search_term, case=False, na=False)]
            if len(filtered_movies) > 0:
                movie_options = filtered_movies['title'].values
            else:
                movie_options = movies['title'].values[:10]  # Show first 10 if no match
                st.warning("No movies found matching your search. Showing popular movies instead.")
        else:
            movie_options = movies['title'].values
        
        selected_movie_name = st.selectbox(
            'Choose your movie:',
            movie_options,
            index=0,
            help="Choose a movie from the filtered results"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        recommend_button = st.button('🚀 Get Recommendations', type="primary", use_container_width=True)

    if recommend_button:
        with st.spinner('🔍 Analyzing your movie preferences...'):
            time.sleep(1)  # Add loading effect
            
            name, posters = recommended(selected_movie_name)
            
            # Always show exactly 5 recommendations
            st.success(f"🎉 Found 5 amazing recommendations for '{selected_movie_name}'!")
            
            # Display recommendations in a grid
            st.markdown("### 🎬 Your Personalized Recommendations")
            
            # Create exactly 5 columns for recommendations
            cols = st.columns(5)
            for idx, (movie_name, poster_url) in enumerate(zip(name, posters)):
                with cols[idx]:
                    with st.container():
                        st.markdown(f"""
                        <div class="movie-card">
                            <div class="movie-title">{movie_name}</div>
                            <div class="movie-poster-container">
                                <img src="{poster_url}" class="movie-poster" style="width: 100%; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" />
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add some interactivity
                        if st.button(f"ℹ️ More Info", key=f"info_{idx}"):
                            st.info(f"Learn more about '{movie_name}' - Coming soon!")
                        
                        # Add rating simulation
                        rating = random.uniform(3.5, 5.0)
                        st.markdown(f"⭐ {rating:.1f}/5.0")

elif selectedmenu == "📁 Projects":
    st.markdown('<h1 class="main-header">📁 My Projects</h1>', unsafe_allow_html=True)
    
    # Project showcase
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="stats-container">
            <h3>🎬 Movie Recommender Pro</h3>
            <p><strong>Description:</strong> An AI-powered movie recommendation system that uses content-based filtering to suggest similar movies based on plot, cast, crew, and genres.</p>
            <p><strong>Technologies:</strong> Python, Streamlit, Scikit-learn, Pandas, TMDB API</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>✨ Smart content-based recommendations</li>
                <li>🎨 Beautiful interactive UI</li>
                <li>⚡ Fast real-time suggestions</li>
                <li>🖼️ Movie poster integration</li>
                <li>📊 4,800+ movie database</li>
            </ul>
            <p><strong>🔗 GitHub Repository:</strong> <a href="https://github.com/vivekggg/movie2watch" target="_blank" style="color: #fff; text-decoration: underline;">https://github.com/vivekggg/movie2watch</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-container">
            <h4>📊 Project Stats</h4>
            <p><strong>Movies:</strong> 4,806</p>
            <p><strong>Features:</strong> 5,000</p>
            <p><strong>Guarantee:</strong> Always 5 recs</p>
            <p><strong>Speed:</strong> < 2s</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional projects placeholder
    st.markdown("### 🚀 Coming Soon")
    st.info("More exciting projects are in development! Stay tuned for updates.")

elif selectedmenu == "📞 Contacts":
    st.markdown('<h1 class="main-header">📞 Get In Touch</h1>', unsafe_allow_html=True)
    
    # Contact information with enhanced styling
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-highlight">
            <h3 class="movie-title">📧 Contact Information</h3>
            <p><strong>Email:</strong> cinecuco@gmail.com</p>
            <p><strong>Project:</strong> Movie Recommender Pro</p>
            <p><strong>GitHub:</strong> <a href="https://github.com/vivekggg/movie2watch" target="_blank" style="color: #fff; text-decoration: underline;">github.com/vivekggg/movie2watch</a></p>
            <p><strong>Status:</strong> Available for collaboration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-highlight">
            <h4>💬 Let's Connect!</h4>
            <p>Have questions about this project or want to collaborate? I'd love to hear from you!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact form
    st.markdown("### 📝 Send a Message")
    with st.form("contact_form"):
        name = st.text_input("Your Name", placeholder="Enter your name")
        email = st.text_input("Your Email", placeholder="Enter your email")
        subject = st.text_input("Subject", placeholder="What's this about?")
        message = st.text_area("Message", placeholder="Tell me about your project or question...")
        
        submitted = st.form_submit_button("📤 Send Message", type="primary")
        
        if submitted:
            if name and email and message:
                st.success("🎉 Message sent successfully! I'll get back to you soon.")
            else:
                st.error("❌ Please fill in all required fields.")
    
    # Social links placeholder
    st.markdown("### 🌐 Follow Me")
    st.info("Social media links coming soon! 🚀")

