CREATE TABLE users(
id SERIAL PRIMARY KEY,
name TEXT,
phone TEXT,
aadhaar TEXT
);

CREATE TABLE centers(
id SERIAL PRIMARY KEY,
name TEXT,
location TEXT,
queue INT
);

CREATE TABLE bookings(
id SERIAL PRIMARY KEY,
user_id INT,
center_id INT,
slot TEXT
);
