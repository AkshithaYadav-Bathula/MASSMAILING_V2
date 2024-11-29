from flask import Flask, request, jsonify, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from send_email import send_email

app = Flask(__name__)

# Flask-Session Configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False
Session(app)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akshb17",  # Adjusted for your environment
    database="massmailing"
)
cursor = db.cursor()

# Register route
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed_password))
        db.commit()
        return jsonify({"message": "User registered successfully!"})
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({"message": f"Error: {err}"}), 400

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user[3], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

# Send email route
@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    to = data['to']
    cc = data['cc']
    bcc = data['bcc']
    subject = data['subject']
    body = data['body']
    
    try:
        message = send_email(to, cc, bcc, subject, body)
        
        # Log email details in the database
        recipients = [to] + cc.split(',') + bcc.split(',')
        for recipient in recipients:
            cursor.execute(
                "INSERT INTO email_status (recipient, subject, status, sent_time) VALUES (%s, %s, %s, NOW())",
                (recipient, subject, "Sent")
            )
        db.commit()
        
        return jsonify({"message": message})
    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)}), 400

# Get email status route
@app.route('/get_email_status', methods=['GET'])
def get_email_status():
    cursor.execute("SELECT * FROM email_status")
    result = cursor.fetchall()
    emails = []

    for row in result:
        email = {
            "recipient": row[1],
            "subject": row[2],
            "status": row[3],
            "sent_time": row[4],
            "delivered_time": row[5],
            "opened_time": row[6],
            "spam": row[7]
        }
        emails.append(email)

    return jsonify(emails)

if __name__ == '__main__':
    app.run(debug=True)
