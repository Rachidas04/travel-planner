# Travel Planner

Travel Planner is a student-focused application designed to help users
explore travel destinations based on their budget and interests.

This project was created for INFO8021 DevOps Strategy and Automation.

## Technologies

- Python and Flask
- HTML and CSS
- PostgreSQL
- Git and GitHub

## Initial website

The initial website includes a Home page and an About Us page.

## Database

The PostgreSQL database contains tables for users, trip preferences,
interests, destinations and recommendations.

- `schema.sql` defines the tables and relationships.
- `initialise_db.py` creates the database and tables.
- `populate_db.py` adds sample data.

The destination costs and sample user are fictional and are used for
testing only.

## Running the website

Create and activate a Python virtual environment, then install the
packages:

    python -m pip install -r requirements.txt

Start the application:

    python -m flask --app travelplanner run

Open the local address shown in the terminal.