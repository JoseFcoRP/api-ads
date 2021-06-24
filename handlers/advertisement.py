import os, json, boto3, base64
from jsonschema import validate
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone


advertisements_table = boto3.resource('dynamodb').Table(os.environ.get('DDB_AD'))
s3 = boto3.resource('s3')
bucket = os.environ.get('Bucket')

with open('schemas/advertisement_post.json','r') as file:
    schema_post = json.load(file)

def list(event, context):
    ann = advertisements_table.scan(Select='SPECIFIC_ATTRIBUTES', AttributesToGet=['title'])
    advertisements = [x['title'] for x in ann.get("Items", [])]
    if not advertisements:
        return {"statusCode": 404, "body": "No advertisements found"}
    else:
        return {"statusCode": 200, "body": json.dumps(advertisements)}

def get(event, context):
    try:
        title = event['pathParameters']['title'].replace('%20', ' ')
    except KeyError:
        return {"statusCode": 400, "body": "Advertisement title not indicated"}

    ann = advertisements_table.query(KeyConditionExpression=Key('title').eq(title))
    advertisements = [{"title":x['title'], "description":x['description'],  "image_url":x['image_url']} for x in ann.get("Items", [])]
    if not advertisements:
        return {"statusCode": 404, "body": f"Advertisement {title} not found"}
    else:
        return {"statusCode": 200, "body": json.dumps(advertisements[0])}

def publish(event, context):
    user = event['requestContext']['authorizer']['claims']['email']
    body = json.loads(event['body'])
    if not body:
        return {"statusCode": 400, "body": "No se ha indicado body"}
    validate(instance=body, schema=schema_post)
    
    path = f"advertisements/image_raw/{body['title']}/raw.{body['image_ext']}"
    image_url = f"https://{bucket}.s3.eu-west-1.amazonaws.com/{path}"
    image_decoded = base64.b64decode(body['image'])
    obj = s3.Object(bucket,path)
    obj.put(Body=image_decoded, ContentType=body['mimetype'])
    payload = {
                'title': body['title'],
                'description': body['description'],
                'image_url': image_url,
                'creation_date': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                'owner': user
              }
    advertisements_table.put_item(Item=payload)
    return {"statusCode": 201, "body": f"Advertisement {body['title']} created"}