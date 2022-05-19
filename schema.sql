CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    name TEXT,
    des TEXT,
    created_at TIMESTAMP,
    visible INTEGER
);

CREATE TABLE subthreads (
    id SERIAL PRIMARY KEY,
    name TEXT,
    content TEXT,
    thread_id INTEGER REFERENCES threads,
    user_id INTEGER REFERENCES users,
    visible INTEGER
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    subthread_id INTEGER REFERENCES subthreads,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    visible INTEGER
);