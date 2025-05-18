import os
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from dotenv import load_dotenv
from mysql.connector import Error
from datetime import datetime

# loading environment
load_dotenv()

DB_CONFIG = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'), #use your own password here
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'notification_system'),
    'raise_on_warnings': True
}

EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': os.getenv('SMTP_PORT', 587),
    'email': os.getenv('EMAIL_ADDRESS'),
    'password': os.getenv('EMAIL_PASSWORD')
}

TWILIO_CONFIG = {
    'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
    'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
    'from_number': os.getenv('TWILIO_PHONE_NUMBER')
}

def create_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def initialize_database():
    conn = None
    try:
        conn = mysql.connector.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host']
        )
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS notifications (id INT AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(255) NOT NULL, type ENUM('email', 'sms', 'in-app') NOT NULL, message TEXT NOT NULL, status ENUM('pending', 'sent', 'failed') DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, INDEX user_index (user_name))")
        conn.commit()
        print("Database initialized successfully")
        
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def send_email(receiver_email, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = 'New Notification'
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = receiver_email

        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.sendmail(EMAIL_CONFIG['email'], receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_sms(phone_number, message):
    try:
        client = Client(TWILIO_CONFIG['account_sid'], TWILIO_CONFIG['auth_token'])
        message = client.messages.create(
            body=message,
            from_=TWILIO_CONFIG['from_number'],
            to=phone_number
        )
        return message.sid is not None
    except Exception as e:
        print(f"SMS error: {e}")
        return False

def send_notification(user_name, notification_type, message, contact_info):
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notifications (user_name, type, message) VALUES (%s, %s, %s)", (user_name, notification_type, message))
        notification_id = cursor.lastrowid
        conn.commit()

        success = False
        if notification_type == 'email':
            success = send_email(contact_info, message)
        elif notification_type == 'sms':
            success = send_sms(contact_info, message)
        
        status = 'sent' if success else 'failed'
        cursor.execute("UPDATE notifications SET status = %s WHERE id = %s"
                       , (status, notification_id))
        conn.commit()

        return success

    except Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_user_notifications(user_name):
    conn = create_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, type, message, status, created_at FROM notifications WHERE user_name= %s ORDER BY created_at DESC"
                       , (user_name,))
        return cursor.fetchall()
    except Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    initialize_database()
    
    # example
    send_notification(
        user_name="user", # user name
        notification_type="email", # set type as "email" or "sms" accordingly
        message="This is a test email",
        contact_info="receiver@gmail.com"  # replace this with actual email/phone
    )
    
    notifications = get_user_notifications("user")
    for notification in notifications:
        print(f"[{notification['created_at']}] {notification['type'].upper()}: {notification['message']} ({notification['status']})")
