import sqlite3
import pandas as pd
from flask import Flask, render_template, request, jsonify
import os
from collections import Counter

# Initialize Flask app
app = Flask(__name__)

# Database file path
db_file = 'twitter_dataf.db'

# Function to create SQLite connection
def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create table and insert data if running for the first time
def init_db():
    if not os.path.exists(db_file):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE tweets (
                id TEXT PRIMARY KEY,
                author_id TEXT,
                text TEXT,
                like_count INTEGER,
                place_id TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        
        # Load the TSV file with updated column names
        data_file = 'Twitter.tsv'
        df = pd.read_csv(data_file, sep='\t', usecols=['id', 'author_id', 'text', 'like_count', 'place_id', 'created_at'])

        # Insert the data into the SQLite database
        df.to_sql('tweets', conn, if_exists='append', index=False)

        conn.close()

# Function to search for a term in the tweets
def search_tweets(term):
    conn = get_db_connection()
    
    query = """
    SELECT 
        COUNT(*) AS total_tweets,
        COUNT(DISTINCT author_id) AS unique_users,
        AVG(like_count) AS avg_likes,
        COUNT(DISTINCT place_id) AS unique_places,
        strftime('%H:00', created_at) AS hour,
        author_id,
        COUNT(*) AS user_tweet_count
    FROM tweets
    WHERE text LIKE ?
    GROUP BY author_id, hour
    """
    
    rows = conn.execute(query, ('%' + term + '%',)).fetchall()
    
    total_tweets = sum(row['user_tweet_count'] for row in rows)
    unique_users = len(set(row['author_id'] for row in rows))
    avg_likes = sum(row['avg_likes'] for row in rows) / len(rows) if rows else 0
    unique_places = len(set(row['unique_places'] for row in rows))
    
    # Find the most frequent tweet time
    hour_counts = Counter(row['hour'] for row in rows)
    most_frequent_hour = max(hour_counts, key=hour_counts.get) if hour_counts else "N/A"
    
    # Find the user with the most tweets
    user_tweet_counts = Counter({row['author_id']: row['user_tweet_count'] for row in rows})
    most_active_user, max_tweets = user_tweet_counts.most_common(1)[0] if user_tweet_counts else ("N/A", 0)
    
    conn.close()
    
    result = [
        f"Total number of tweets containing the term '{term}': {total_tweets}",
        f"Number of unique users: {unique_users}",
        f"Average number of likes: {avg_likes:.2f}",
        f"Number of unique place IDs: {unique_places}",
        f"Most frequent tweet time (hour): {most_frequent_hour}",
        f"User with the most tweets: User ID {most_active_user} with {max_tweets} tweets"
    ]
    
    return result

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    term = request.form['term']
    result = search_tweets(term)
    return jsonify({"result": result})

# Run initialization
if __name__ == '__main__':
    init_db()
    app.run(debug=True)