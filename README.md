# 🎬 Movie Recommender Pro

An AI-powered movie recommendation system that uses content-based filtering to suggest similar movies based on plot, cast, crew, and genres.

## 🚀 Quick Start

**Clone and run the project:**


## ✨ Features

- 🎯 **Smart Recommendations**: AI-powered content-based filtering
- 🎨 **Beautiful UI**: Interactive and responsive design
- ⚡ **Fast Results**: Real-time recommendations in under 2 seconds
- 🖼️ **Movie Posters**: Integration with TMDB API for movie posters
- 📊 **Large Database**: 4,800+ movies in the database
- 🔍 **Smart Search**: Real-time movie search and filtering
- 📱 **Responsive Design**: Works on all devices

## 🚀 Live Demo

https://movie2watch-gpaedaczbhduinkn2wjtc6.streamlit.app/

**🔗 GitHub Repository**: [https://github.com/vivekggg/movie2watch](https://github.com/vivekggg/movie2watch)

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** - Web application framework
- **Scikit-learn** - Machine learning library
- **Pandas** - Data manipulation
- **NLTK** - Natural language processing
- **TMDB API** - Movie database and posters

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone https://github.com/vivekggg/movie2watch.git
cd movie2watch
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Generate Data Files

Before running the app, you need to generate the required data files:

```bash
python generate_data.py
```

This will create:
- `movies_dict.pkl` - Movie data dictionary
- `similarity.pkl` - Similarity matrix for recommendations

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 📁 Project Structure

```
movie2watch/
├── app.py                 # Main Streamlit application
├── generate_data.py       # Data generation script
├── requirements.txt       # Python dependencies
├── procfile              # Heroku deployment configuration
├── setup.sh              # Heroku setup script
├── README.md             # Project documentation
├── .gitignore            # Git ignore file
├── tmdb_5000_movies.csv  # Movie dataset
├── tmdb_5000_credits.csv # Credits dataset
└── venv/                 # Virtual environment (not in repo)
```

## 🎯 How It Works

1. **Data Processing**: The system processes movie data including:
   - Plot summaries (overview)
   - Genres
   - Keywords
   - Cast information
   - Crew information (especially directors)

2. **Feature Engineering**: 
   - Combines all text features into a single 'tags' field
   - Applies text preprocessing (lowercasing, stemming)
   - Uses CountVectorizer to create numerical features

3. **Similarity Calculation**:
   - Computes cosine similarity between movies
   - Creates a similarity matrix for all movie pairs

4. **Recommendation Engine**:
   - Finds the 5 most similar movies for any given movie
   - Displays recommendations with movie posters
   - Provides interactive search functionality

## 🚀 Deployment

### Deploy to Heroku

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create Heroku App**:
```bash
heroku create your-movie-recommender-app
```

3. **Set Environment Variables**:
```bash
heroku config:set TMDB_API_KEY=your_tmdb_api_key
```

4. **Deploy**:
```bash
git push heroku main
```

5. **Generate Data on Heroku**:
```bash
heroku run python generate_data.py
```

### Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub account
4. Select this repository
5. Deploy!

## 📊 Dataset

The application uses the TMDB 5000 Movie Dataset which includes:
- 4,806 movies
- Movie metadata (title, overview, genres, etc.)
- Cast and crew information
- Movie posters via TMDB API

## 🔧 Configuration

### TMDB API Setup

1. Get a free API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Replace the API key in `app.py`:
```python
response = requests.get(
    f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US'
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Vivek G**
- GitHub: [@vivekggg](https://github.com/vivekggg)
- Email: cinecuco@gmail.com
- **Repository**: [https://github.com/vivekggg/movie2watch](https://github.com/vivekggg/movie2watch)

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for movie data and posters
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Scikit-learn](https://scikit-learn.org/) for machine learning tools

## 📈 Future Enhancements

- [ ] User authentication and personalized recommendations
- [ ] Collaborative filtering integration
- [ ] Movie rating and review system
- [ ] Advanced filtering options (year, rating, etc.)
- [ ] Export recommendations functionality
- [ ] Mobile app version

---

⭐ **Star this repository if you found it helpful!**
