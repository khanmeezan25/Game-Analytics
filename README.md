# Project Overview
The Tennis Analytics Dashboard is a data analytics application developed using Python, SQLite, Streamlit, and the Sportradar Tennis API. The project collects tennis-related data, stores it in a relational database, and provides an interactive dashboard for analysis and visualization.

# Features
API Integration using Sportradar Tennis API
SQLite Database Management
Competitor Ranking Analysis
Competition and Category Analysis
Venue and Complex Analysis
Country-wise Competitor Statistics
Interactive Streamlit Dashboard
Search and Filter Functionality
Leaderboard Visualization

# Technology Stack
Python
SQLite
Streamlit
Pandas
Requests
Sportradar Tennis API

# Project Structure
Game-Analytics-Dashboard
│
├── app.py
├── api_fetch.py
├── insert_data.py
├── database.py
├── queries.py
├── tennis.db
├── requirements.txt
├── README.md
└── SQL_Queries_Document.pdf

# Database Tables
Categories
Competitions
Complexes
Venues
Competitors
Competitor Rankings

# Workflow
Fetch data from Sportradar API
Transform JSON data
Store data in SQLite database
Execute SQL queries
Display results using Streamlit dashboard

# Dashboard Pages

# Home Page
Displays key statistics and top competitors.

# Search & Filter
Allows users to search competitors and apply filters.

# Competitor Details
Provides detailed information about individual competitors.

# Country Analysis
Displays country-wise competitor statistics.

# Leaderboard
Shows top-ranked competitors and highest point holders.

# Installation
Clone the repository:
git clone <repository-url>

Install dependencies:
pip install -r requirements.txt

Run the application:
python -m streamlit run app.py

Replace API_KEY with your own Sportradar API key
