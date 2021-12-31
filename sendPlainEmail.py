import boto3

def send_plain_email():
    ses_client = boto3.client("ses", region_name="us-east-2")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "devendra.sahu@nagarro.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello, world!",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source="devendra.sahu@nagarro.com",
    )

    print(response)

send_plain_email()