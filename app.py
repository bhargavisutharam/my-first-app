from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

# Replace with your AWS RDS PostgreSQL credentials
DB_CONFIG = {
    'host': 'database-1.cb088y2a4qbi.ap-southeast-2.rds.amazonaws.com',
    'dbname': 'database-1',
    'user': 'postgres',
    'password': 'zeal1234',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG['host'],
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG['port']
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        try:
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
            conn.commit()
        except Exception as e:
            print("Insert error:", e)
            conn.rollback()

    cur.execute("SELECT name, email FROM users;")
    users = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("index.html", users=users)

if __name__ == "__main__":
    create_table()
    app.run(debug=True, host="0.0.0.0", port=5000)