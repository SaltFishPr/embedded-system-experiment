DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS record;
CREATE TABLE user (
    username TEXT PRIMARY KEY,
    phone_number TEXT NOT NULL,
    residence TEXT NOT NULL
);
CREATE TABLE record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username INTEGER NOT NULL,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES user (username)
);