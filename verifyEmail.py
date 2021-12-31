import boto3
import argparse

#val=input("Enter email for verification:")
myParser=argparse.ArgumentParser(prog='verifyEmail', description='It will confirming receipt for receiving email from AWS')

myParser.add_argument('--Email', action='store', required='True', metavar='"Receipt email id"', help='Balnk')

args = myParser.parse_args()

val=args.Email

def verify_email_identity(email):
    ses_client = boto3.client("ses", region_name="us-east-2")
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )
    print(response)

verify_email_identity(val)