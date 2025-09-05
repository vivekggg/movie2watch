"""
Data Generation Script for Movie Recommendation App
This script generates the required pickle files for the application.
Run this script before deploying to generate the similarity matrix and movies dictionary.
"""

import pandas as pd
import numpy as np
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import nltk

def download_nltk_data():
    """Download required NLTK data"""
    try:
        nltk.download('punkt', quiet=True)
    except:
        print("NLTK data download failed, but continuing...")

def process_movies_data():
    """Process the movies data and generate similarity matrix"""
    print("Loading movie data...")
    
    # Load the data
    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')
    
    # Merge the datasets
    movies = movies.merge(credits, on='title')
    
    # Select relevant columns
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    
    # Drop null values
    movies.dropna(inplace=True)
    
    print("Processing movie features...")
    
    # Function to convert string representations of lists to actual lists
    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    # Apply conversion to genres and keywords
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)

    # Function to get top 3 cast members
    def convert3(obj):
        L = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter != 3:
                L.append(i['name'])
                counter += 1
            else:
                break
        return L

    movies['cast'] = movies['cast'].apply(convert3)

    # Function to get director
    def fetch_director(obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L

    movies['crew'] = movies['crew'].apply(fetch_director)

    # Convert overview to list of words
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    # Remove spaces from all text features
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])

    # Combine all features into tags
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    # Create new dataframe with movie_id, title, and tags
    new_df = movies[['movie_id','title','tags']].copy()

    # Convert tags list to string
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

    # Convert to lowercase
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

    print("Applying text processing...")
    
    # Initialize Porter Stemmer
    ps = PorterStemmer()

    def stem(text):
        y = []
        for i in text.split():
            y.append(ps.stem(i))
        return " ".join(y)

    # Apply stemming
    new_df['tags'] = new_df['tags'].apply(stem)

    print("Creating similarity matrix...")
    
    # Create CountVectorizer
    cv = CountVectorizer(max_features=5000, stop_words='english')

    # Transform tags to vectors
    vectors = cv.fit_transform(new_df['tags']).toarray()

    # Calculate cosine similarity
    similarity = cosine_similarity(vectors)

    print("Saving files...")
    
    # Save the files
    pickle.dump(new_df.to_dict(), open('movies_dict.pkl','wb'))
    pickle.dump(similarity, open('similarity.pkl','wb'))

    print(f"Files generated successfully!")
    print(f"Movies: {len(new_df)}")
    print(f"Similarity matrix shape: {similarity.shape}")

if __name__ == "__main__":
    print("Movie Recommendation Data Generator")
    print("=" * 40)
    
    try:
        download_nltk_data()
        process_movies_data()
        print("\nData generation completed successfully!")
        print("You can now run the Streamlit app with: streamlit run app.py")
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure you have the required CSV files in the directory.")
