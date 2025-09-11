#!/usr/bin/python3
import mysql.connector
import csv

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    ''')
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                "INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (row['user_id'], row['name'], row['email'], row['age'])
            )
    connection.commit()
    cursor.close()
