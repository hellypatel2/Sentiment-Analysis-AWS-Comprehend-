import json
import urllib.parse
import boto3
import csv,itertools

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    list=[]
    dict={}
   # https://www.nltk.org/nltk_data/
    STOP_WORDS = ['haven', 'down', 'can', "weren't", 'but', 'in', 'weren', 'above', 'which', 'all', 'ain', 'were', 'again', 'it', "couldn't", 'there', 'for', 'only', 'whom', 'hasn', 'doing', 'her', 'while', 'should', 'i', "needn't", 'nor', 'those', "hadn't", 'been', 'how', 'being', 'where', "you're", 'of', 'than', 'my', 'off', "mustn't", 'what', 'itself', "didn't", "don't", 'its', 'ours', 'very', 'further', 'at', "mightn't", 'why', 'll', 'between', 'below', "shan't", 'be', 'yourselves', 'she', 'ourselves', 'if', 'am', 'has', 'now', 'about', 'did', 'over', 'more', 'we', 's', 'couldn', 'isn', 'our', 'd', "doesn't", "wasn't", 'theirs', 'won', 'any', 'yourself', "shouldn't", 'their', 'too', 'his', 'on', "isn't", 'had', 'by', 'herself', 'once', 'same', "hasn't", "won't", 'mustn', 'out', "she's", 'against', 'a', 'hers', 'that', "it's", 'to', 'or', 'with', 'you', 'are', "wouldn't", 'under', 'not', 'will', 'shan', 'such', 'having', 'some', 'before', 'o', 'doesn', 'your', 'aren', 'when', 'them', "you'd", 'until', 'was', 'during', 'own', 't', 'up', 'didn', 'does', 'needn', 'here', 'y', 'as', "haven't", 'no', 'they', 'don', 'm', 'wouldn', 'the', 'then', 'who', 'do', 'other', 'wasn', 'hadn', 'myself', 'is', "should've", "aren't", 've', 'this', 'himself', 'themselves', 'yours', 'from', 'so', 'have', 'most', 'me', 'him', "you'll", 're', 'these', 'just', 'mightn', 'both', 'shouldn', 'each', "that'll", 'he', 'because', "you've", 'through', 'after', 'and', 'an', 'into', 'few', 'ma']
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    aws = boto3.resource('s3')
    # https://rosettacode.org/wiki/Levenshtein_distance#Iterative_2
    def Levenshtein_distance(s1,s2):
        if len(s1) > len(s2):
            s1,s2 = s2,s1
        distances = range(len(s1) + 1)
        for index2,char2 in enumerate(s2):
            newDistances = [index2+1]
            for index1,char1 in enumerate(s1):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1],
                                                 distances[index1+1],
                                                 newDistances[-1])))
            distances = newDistances
        return distances[-1]
   
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content=response["Body"].read().splitlines()
        for line in content:
            for i in line.decode('utf-8').split():
                if i in STOP_WORDS:
                    continue
                
                else:
                    list.append((i.lower()).strip().strip(",").strip("."))
        print(list)
        print(minimumEditDistance("one","chamber"))
        fname='/tmp/001.csv'
        with open(fname, 'w') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(["Current_Word", "Next_Word", "Levenshtein distance"])
            list_cycle = itertools.cycle(list)
            next(list_cycle)

            for i in range(len(list)):
                next_element = next(list_cycle)
                writer.writerow([list[i],next_element, minimumEditDistance(list[i],next_element)])

        aws.meta.client.upload_file(fname, 'traindata-b00868907', '1.csv')
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
