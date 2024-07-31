from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

# Load the merged pickle file and item similarity matrix
df = pd.read_pickle(open('movie_df.pkl', 'rb'))
item_similarity = pd.read_pickle(open('item_similarity.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('movie_title').strip().lower()
    recommendations = get_recommendations(user_input)

    if recommendations:
        return render_template('recommend.html', recommendations=recommendations)
    else:
        return render_template('recommend.html', error="No recommendations found for the given movie title. Please check the title and try again.")

@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('query').strip().lower()
    matching_titles = df.index[df.index.str.lower().str.startswith(query)].tolist()
    return jsonify(matching_titles[:10])  # Return only the top 10 suggestions

def get_recommendations(movie):
    try:
        movie_index = df.index.get_loc(movie)
        similar_movies = sorted(list(enumerate(item_similarity[movie_index])), key=lambda x: x[1], reverse=True)[0:11]
        recommended_movies = [(df.index[i[0]], df.iloc[i[0]].poster_url) for i in similar_movies]
        return recommended_movies
    except (KeyError, IndexError):
        return []

if __name__ == '__main__':
    app.run(debug=True)
