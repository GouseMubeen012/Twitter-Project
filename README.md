# Twitter-Project
# POTATO (Panel-based Open Term-level Aggregate Twitter Observatory)

POTATO is a prototype website that allows users to search for terms in tweets and get aggregate information about the people who tweeted about those terms.

## Project Overview

This project implements a Flask-based web application that ingests tweet data from a TSV file into a SQLite database and provides a search functionality to analyze tweets containing specific terms.

### Features

- Data ingestion from TSV file to SQLite database
- Search functionality for tweets containing specific terms
- Aggregate analysis including:
  - Total number of tweets
  - Number of unique users
  - Average number of likes
  - Number of unique place IDs
  - Most frequent tweet time
  - User with the most tweets on the search term

## Files in this Repository

- `potato.py`: Main Flask application file containing the backend logic
- `index.html`: HTML template for the web interface

## How to Use

1. Clone this repository to your local machine
2. Ensure you have Python and the required libraries installed (Flask, pandas, sqlite3)
3. Place your Twitter data TSV file in the project directory and name it `Twitter.tsv`
4. Run the Flask application: `python potato.py`
5. Open a web browser and go to `http://localhost:5000`
6. Enter a search term in the provided input field and submit to see the analysis results

## Technologies Used

- Python
- Flask
- SQLite
- Pandas
- HTML/JavaScript

## Future Improvements

- Implement more advanced privacy protections
- Optimize data ingestion for larger datasets
- Add more detailed analytics and visualizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
