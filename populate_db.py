import os

import psycopg


# Sample destination costs are fictional and are for testing only.
destinations = [
    ("Barcelona", "Spain", 500, "Beach and sightseeing", "Sample travel information"),
    ("Madrid", "Spain", 450, "Museums and food", "Sample travel information"),
    ("Paris", "France", 650, "Museums and sightseeing", "Sample travel information"),
    ("Nice", "France", 600, "Beach and sightseeing", "Sample travel information"),
    ("Rome", "Italy", 550, "History and food", "Sample travel information"),
    ("Milan", "Italy", 600, "Shopping and sightseeing", "Sample travel information"),
    ("Lisbon", "Portugal", 450, "Food and sightseeing", "Sample travel information"),
    ("Porto", "Portugal", 400, "Food and sightseeing", "Sample travel information"),
    ("Amsterdam", "Netherlands", 650, "Museums and cycling", "Sample travel information"),
    ("Berlin", "Germany", 500, "History and museums", "Sample travel information"),
    ("Prague", "Czechia", 400, "History and sightseeing", "Sample travel information"),
    ("Budapest", "Hungary", 400, "Thermal baths and history", "Sample travel information"),
    ("Athens", "Greece", 500, "History and food", "Sample travel information"),
    ("Dubrovnik", "Croatia", 600, "Beach and history", "Sample travel information"),
    ("Vienna", "Austria", 600, "Museums and music", "Sample travel information"),
    ("Copenhagen", "Denmark", 700, "Food and cycling", "Sample travel information"),
    ("Stockholm", "Sweden", 700, "Museums and sightseeing", "Sample travel information"),
    ("Krakow", "Poland", 350, "History and food", "Sample travel information"),
    ("Valletta", "Malta", 500, "History and beach", "Sample travel information"),
    ("Edinburgh", "Scotland", 450, "History and sightseeing", "Sample travel information"),
]

interests = [
    ("Beach",),
    ("History",),
    ("Food",),
    ("Museums",),
    ("Sightseeing",),
]


# Get the database password from the Terminal environment.
password = os.environ.get("DB_PASSWORD")

if not password:
    raise ValueError(
        "Please set DB_PASSWORD in the terminal before running this file."
    )


# Connect to the Travel Planner database.
with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="travel_planner",
    user="postgres",
    password=password,
) as connection:

    with connection.cursor() as cursor:

        # Add each destination if it is not already in the database.
        for name, country, cost, activities, information in destinations:
            cursor.execute(
                """
                INSERT INTO destination
                    (
                        destination_name,
                        country,
                        estimated_cost,
                        activities,
                        travel_information
                    )
                SELECT %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM destination
                    WHERE destination_name = %s
                      AND country = %s
                )
                """,
                (
                    name,
                    country,
                    cost,
                    activities,
                    information,
                    name,
                    country,
                ),
            )

        # Add interests without duplicating existing names.
        cursor.executemany(
            """
            INSERT INTO interest (interest_name)
            VALUES (%s)
            ON CONFLICT (interest_name) DO NOTHING
            """,
            interests,
        )

        # Add a fictional user for testing.
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            """,
            (
                "Sample User",
                "sample@example.com",
                "test-account-no-login",
            ),
        )

        # Find the sample user's ID.
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE email = %s
            """,
            ("sample@example.com",),
        )

        user_id = cursor.fetchone()[0]

        # Find an existing preference for the sample user.
        cursor.execute(
            """
            SELECT preference_id
            FROM trip_preference
            WHERE user_id = %s
            LIMIT 1
            """,
            (user_id,),
        )

        preference = cursor.fetchone()

        # If no preference exists, create one.
        if preference:
            preference_id = preference[0]
        else:
            cursor.execute(
                """
                INSERT INTO trip_preference
                    (
                        user_id,
                        budget,
                        start_date,
                        end_date,
                        preferred_month
                    )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING preference_id
                """,
                (
                    user_id,
                    600,
                    "2027-06-01",
                    "2027-06-07",
                    6,
                ),
            )

            preference_id = cursor.fetchone()[0]

        # Find the ID of the Beach interest.
        cursor.execute(
            """
            SELECT interest_id
            FROM interest
            WHERE interest_name = %s
            """,
            ("Beach",),
        )

        interest_id = cursor.fetchone()[0]

        # Link the sample preference to Beach.
        cursor.execute(
            """
            INSERT INTO preference_interest
                (preference_id, interest_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            (preference_id, interest_id),
        )

        # Find Barcelona's destination ID.
        cursor.execute(
            """
            SELECT destination_id
            FROM destination
            WHERE destination_name = %s
              AND country = %s
            LIMIT 1
            """,
            ("Barcelona", "Spain"),
        )

        destination_id = cursor.fetchone()[0]

        # Add Barcelona as an example recommendation.
        cursor.execute(
            """
            INSERT INTO recommendation
                (preference_id, destination_id)
            SELECT %s, %s
            WHERE NOT EXISTS (
                SELECT 1
                FROM recommendation
                WHERE preference_id = %s
                  AND destination_id = %s
            )
            """,
            (
                preference_id,
                destination_id,
                preference_id,
                destination_id,
            ),
        )


print("Sample data added successfully!")