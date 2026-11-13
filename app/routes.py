from flask import render_template
from app import app
import os
import psycopg
from flask import request


@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Rachida'}

    destinations = [
        {'name': 'Barcelona', 'interest': 'City and beach'},
        {'name': 'Paris', 'interest': 'Culture and history'},
        {'name': 'London', 'interest': 'Food and sightseeing'}
    ]

    return render_template(
        'index.html',
        title='Home',
        user=user,
        destinations=destinations
    )


@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/budget')
def budget_search():
    budget = request.args.get('budget', type=float)
    results = None

    if budget is not None and budget >= 0:
        with psycopg.connect(
            host="localhost",
            port=5432,
            dbname="travel_planner",
            user="postgres",
            password=os.environ.get("DB_PASSWORD"),
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT destination_name, country, estimated_cost
                    FROM destination
                    WHERE estimated_cost <= %s
                    ORDER BY estimated_cost
                    """,
                    (budget,),
                )
                results = cursor.fetchall()

    return render_template(
        'budget.html',
        title='Search by Budget',
        results=results,
        budget=budget,
    )