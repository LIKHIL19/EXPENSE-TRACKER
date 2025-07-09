CREATE DATABASE IF NOT EXISTS expenses_tracker;
USE expenses_tracker;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    num VARCHAR(50) NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    date VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS budgets (
    user_id INT PRIMARY KEY,
    monthly_budget FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
