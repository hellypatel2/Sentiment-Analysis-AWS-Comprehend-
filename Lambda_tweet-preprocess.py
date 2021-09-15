import json
import urllib.parse
import boto3
import re

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    list = []
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    aws = boto3.resource('s3')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response["Body"].iter_chunks(5000)
        filename = "/tmp/processed-tweets-b00868907.json"
        jsonfile = open(filename, "w")
        for line in content:
            url = re.sub(r'http\S+', " ", line.decode('utf-8', "ignore"))
            letters = re.sub(r'\W+', ' ', url)
            comprehend = boto3.client('comprehend')
            if (not letters):
                continue;
            else:
                resp = comprehend.detect_sentiment(Text=letters, LanguageCode="en")
                list.append(resp)
        jsonfile.write(json.dumps(list))
        jsonfile.close()
        aws.meta.client.upload_file(filename, 'twitterdata-b00868907', 'output.json')

    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e
