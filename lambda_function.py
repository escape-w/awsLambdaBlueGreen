##listing POC resource based on thier tag

import os
import boto3
#import tabulate

#email   = os.environ['email']
email   = ['devendra.sahu@nagarro.com']
region  = os.environ['region']
#region  = 'us-east-2'
sdrEmail= os.environ['sdrEmail']
#sdrEmail= 'devendra.sahu@nagarro.com'
CHARSET = 'UTF-8'
instanceDetail=[]

ec2_client = boto3.client('ec2', region_name=region)
ses_client = boto3.client('ses', region_name=region)

ec2Response = ec2_client.describe_instances(Filters=[{'Name':'tag:Name','Values':['*_POC']}])            
instances_full_details = ec2Response['Reservations']

def send_html_email(**arguments):
    ##checking whether supplied email address is whitelisted or not?
    emailData=ses_client.list_verified_email_addresses()['VerifiedEmailAddresses']
    res = [ele for ele in email if(ele in emailData)]
    
    if not res:
        print('no')
        exit()

    emailAsString = ''.join(arguments['email'])

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                emailAsString,
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": arguments['HTML_EMAIL_CONTENT'],
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "AWS Lambda Blue Green Deployment",
            },
        },
        Source=arguments['sdrEmail'],
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

def ec2Report():
    for instance_detail in instances_full_details:
        group_instances = instance_detail['Instances']
        instanceData=[]
        for instance in group_instances:
            instanceData.append(instance['InstanceId'])
            instanceData.append(instance['InstanceType'])
            InstanceTag=(instance['Tags'])
            for i in InstanceTag:
                if i['Key'] == 'Name':
                    instanceData.append(i)
        instanceDetail.append(instanceData)
    if len(instanceDetail) > 0:
        return instanceDetail
    else:
        return False

def lambda_handler(event, context):
    newData=ec2Report()
    if not bool(newData):
    #newData=tabulate.tabulate(ec2Report(), headers=['InstanseId', 'InstanseType', 'Tag'])
        print('no data')
        exit()
    else:
        print('data')

    HTML_EMAIL_CONTENT = f"""
            <html>
            <head></head>
            <body>
            <h1 style='text-align:center'>This is version 2</h1>
            <blockquote>
            {newData}
            </blockquote>
            <p>Regards,AWS Lambda Blue Green Deployment</p>
            </body>
            </html>
    """

    if send_html_email(sdrEmail=sdrEmail, HTML_EMAIL_CONTENT=HTML_EMAIL_CONTENT,email=email):
        print('success')
    else:
        print('fail')