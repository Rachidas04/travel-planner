CREATE TABLE users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE destination (
    destination_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    destination_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    estimated_cost DECIMAL(10, 2) NOT NULL,
    activities TEXT,
    travel_information TEXT
);

CREATE TABLE interest (
    interest_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    interest_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE trip_preference (
    preference_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    budget DECIMAL(10, 2) NOT NULL,
    start_date DATE,
    end_date DATE,
    preferred_month INTEGER,

    FOREIGN KEY (user_id) REFERENCES users(user_id),

    CHECK (budget >= 0),
    CHECK (preferred_month BETWEEN 1 AND 12),
    CHECK (end_date >= start_date)
);

CREATE TABLE preference_interest (
    preference_id INTEGER NOT NULL,
    interest_id INTEGER NOT NULL,

    PRIMARY KEY (preference_id, interest_id),

    FOREIGN KEY (preference_id)
        REFERENCES trip_preference(preference_id),

    FOREIGN KEY (interest_id)
        REFERENCES interest(interest_id)
);

CREATE TABLE recommendation (
    recommended_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    preference_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,

    FOREIGN KEY (preference_id)
        REFERENCES trip_preference(preference_id),

    FOREIGN KEY (destination_id)
        REFERENCES destination(destination_id)
);