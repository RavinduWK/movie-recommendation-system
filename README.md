# Movies Recommender System

This is a content-based movie recommendation system built using machine learning. The system recommends movies based on the similarity of movies.

## Features

- Select a movie from the list to get recommendations
- Display recommended movies with their posters

## Installation

1. Clone the repository:

   ```sh
   https://github.com/RavinduWK/movie-recommendation-system.git
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   - Create a [.env](http://_vscodecontentref_/1) file in the root directory
   - Add your TMDB API key to the [.env](http://_vscodecontentref_/2) file:
     ```env
     TMDB_API_KEY=your_api_key_here
     ```

## Usage

1. Run the application:

   ```sh
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Select a movie from the dropdown to get recommendations.
