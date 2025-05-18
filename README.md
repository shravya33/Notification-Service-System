# Notification-Service-System
A Python-based notification system that sends emails and SMS messages, with tracking in a MySQL database.

## Features

- Send email notifications via Gmail SMTP
- Send SMS notifications via Twilio
- Track notification status in MySQL database

## Prerequisites

- Python 3.x
- MySQL server (running)
- A Gmail account with [App Password](https://myaccount.google.com/apppasswords) enabled
- Twilio account (for SMS functionality)

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/shravya33/Notification-Service-System.git
```

### 2. Update the credentials accordingly in the .env file and configure it
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install the dependencies
```
pip install mysql-connector-python python-dotenv twilio
```

### 4. Initialize the database and run the system
Before running the ```system.py``` file, make sure you have edited this section according to your needs:
```python
if __name__ == "__main__":
    initialize_database()
    
    # example
    send_notification(
        user_name="user", #name of the user
        notification_type="email", # set type as "email" or "sms" accordingly
        message="This is a test email",
        contact_info="receiver@gmail.com"  # replace this with actual email/phone
    )
    
    print("Notification sent successfully. Please check the database.")
```
Now, run the python file. This will create a database (if not already existing) to store the notifications and send the notification to the given email or phone number.
```
python system.py
```

#### Testing
To test the functionalities, you can run ```test_email.py``` and ```test_sms.py``` respectively.
