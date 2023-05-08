import json
import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image

def lambda_handler(event, context):
 # TODO implement
 print("S3 event : {0}".format(event['Records'][0]['eventName']))
 print("S3 Bucket Name : {0}".format(event['Records'][0]['s3']['bucket']['name']))
 print("S3 Object Name : {0}".format(event['Records'][0]['s3']['object']['key']))
 
 client = boto3.client('ses')
 s3_client = boto3.client('s3')
 subject = "New object received on {0} bucket".format(str(event['Records'][0]['s3']['bucket']['name']))
 bucketName = event['Records'][0]['s3']['bucket']['name']
 objectName = event['Records'][0]['s3']['object']['key']
 objectSize = event['Records'][0]['s3']['object']['size']
 objectType = event['Records'][0]['s3']['object']['key'].split('.')[1]
 print("S3 Object Type: {0}".format(objectType))
 if (objectType == "jpg" or objectType == "jpeg" or objectType == "png"):
     for record in event['Records']:
         bucket = record['s3']['bucket']['name']
         key = unquote_plus(record['s3']['object']['key'])
         tmpkey = key.replace('/', '')
         download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
         upload_path = '/tmp/resized-{}'.format(tmpkey)
         s3_client.download_file(bucket, objectName, download_path)
         resize_image(download_path, upload_path)
         s3_client.upload_file(upload_path, '{}-resized'.format(bucket), 'resized-{}'.format(objectName))
 body = """
 <br>
 S3 URI : s3://{0}/{1} <br>
 Object Name : {1} <br>
 Object Size: {2} bytes<br>
 Object Type: .{3} <br>
 """.format(bucketName,objectName,objectSize,objectType)
 
 message = {"Subject" : {"Data" : subject}, "Body" : {"Html" : {"Data" : body}}}
 
 response = client.send_email(Source = "pdpavandesai@gmail.com",Destination = {"ToAddresses" : ["pdpavandesai@yahoo.com"]}, Message = message)
 
 return {
 'statusCode': 200
 #’body’: json.dumps(‘Hello from Lambda!’)
 }
 
def resize_image(image_path, resized_path):
  with Image.open(image_path) as image:
    image.thumbnail(tuple(x / 2 for x in image.size))
    image.save(resized_path)
