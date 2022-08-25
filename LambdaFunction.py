import json
import random
import boto3
import tweepy
from datetime import datetime, timedelta, timezone
JST = timezone(timedelta(hours=+9), 'JST')

def lambda_handler(event, context):
    text = random_choice_text()
    tweet(text)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def tweet(text: str):
    auth = tweepy.OAuthHandler('API Key', 'API Secret Key')
    auth.set_access_token('Access Token', 'Access Token Secret')
    api = tweepy.API(auth)
    api.update_status(text)


def random_choice_text() -> str:
    db = boto3.resource('dynamodb')
    table = db.Table('TableName')
    res = table.scan()
    items = res['Items']
    
    now = datetime.now(JST).strftime('%Y/%m/%d %H:%M:%S')
    texts = []
    weights = []
    for item in items:
        texts.append(item['text']+'\n'+'\n'+'('+now+')')
        weights.append(int(item['weight']))
    return random.choices(texts, k = 1, weights=weights)[0]