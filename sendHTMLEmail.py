import boto3

email = ['devendra.sahu@nagarro.com']
ses_client = boto3.client("ses", region_name="us-east-2")

def send_html_email():
    
    emailData=ses_client.list_verified_email_addresses()['VerifiedEmailAddresses']
    res = [ele for ele in email if(ele in emailData)]
    
    if not res:
        print('no')
        exit()

    CHARSET = "UTF-8"
    Data='test'
    HTML_EMAIL_CONTENT = f"""
        <html>
        <head></head>
        <body>
        <h1 style='text-align:center'>This is version 1</h1>
        <blockquote>
        {Data}
        </blockquote>
        <p>Regards,AWS Lambda Blue Green Deployment</p>
        </body>
        </html>
    """
    str = ''.join(email)
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                str,
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source=email[0],
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

print(send_html_email())
