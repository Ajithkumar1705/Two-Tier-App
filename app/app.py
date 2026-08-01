from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    "host": os.environ.get("DB_HOST", "db"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME", "appdb"),
}

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy"}, 200
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        cursor.execute("INSERT INTO messages (name) VALUES (%s)", (name,))
        conn.commit()
    cursor.execute("SELECT name FROM messages ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return render_template("index.html", rows=rows)
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
