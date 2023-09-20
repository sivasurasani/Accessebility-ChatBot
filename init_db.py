import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO products (title, author) VALUES (?, ?)",
            ('JAVA', 'Tanenbaum')
            )

cur.execute("INSERT INTO products (title, author) VALUES (?, ?)",
            ('Machine learning', 'John Paul Mueller')
            )
cur.execute("INSERT INTO products (title, author) VALUES (?, ?)",
            ('Python', 'ABC')
            )
cur.execute("INSERT INTO products (title, author) VALUES (?, ?)",
            ('Artifical Intelligence', 'John Paul Mueller')
            )

connection.commit()
connection.close()
