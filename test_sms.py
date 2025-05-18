def test_sms():
    try:
        client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        message = client.messages.create(
            body="This is just a SMS for testing",
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to="+91 1234567890"  # use an actual phone number here
        )
        print(f"SMS sent! SID: {message.sid}")
    except Exception as e:
        print(f"SMS failed: {str(e)}")
