from flask import render_template
from app import app


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