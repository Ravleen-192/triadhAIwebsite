import json
from email_send import *
from smtplib import SMTPResponseException
from urllib.parse import unquote
import json
import logging
import boto3
import botocore
from botocore.exceptions import ClientError

def create_presigned_url():
    # Generate a presigned URL for the S3 object
    bucketName = "triadhdigital-dev";
    value1="whitepaper/HeliosWhitepaper.pdf"
    
    s3_client = boto3.client('s3',region_name="us-east-1",config=boto3.session.Config(signature_version='s3v4',))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucketName,
                                                            'Key': value1},
                                                    ExpiresIn=10000)
    except Exception as e:
        print(e)
        logging.error(e)
        return "Error"
    # The response contains the presigned URL
    return response
    

   
def handler(event, context):
    print('received event:')
    print('received context:')
    print(context)
    print(event)
    surl = create_presigned_url()
    to_address = str(event['queryStringParameters']['email'])
    name =  unquote(str(event['queryStringParameters']['name']))
    title =  unquote(str(event['queryStringParameters']['title']))
    company =  unquote(str(event['queryStringParameters']['company']))
    phone =  unquote(str(event['queryStringParameters']['phone']))
    print(to_address)
    print(name)
    print(surl)
        
    try:
        es = email_sender()
        es.connect() 
        msg = compose_msg(to_address,name,surl) 
        es.send_email(to_address,msg)
        print("Message sent successfully")
        es.disconnect()
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Message sent successfully!')
        }
    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        return {
        'statusCode': error_code,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(error_message)
        }