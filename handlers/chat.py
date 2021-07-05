import os, json, boto3, base64
from jsonschema import validate
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone


chats_table = boto3.resource('dynamodb').Table(os.environ.get('DDB_CHATS'))
advertisements_table = boto3.resource('dynamodb').Table(os.environ.get('DDB_AD'))

with open('schemas/message_post.json','r') as file:
    schema_post = json.load(file)

def get_chat(event, context):
    try:
        title = event['pathParameters']['title'].replace('%20', ' ')
    except KeyError:
        return {"statusCode": 400, "body": "No se ha indicado anuncio"}
    
    ann = advertisements_table.query(KeyConditionExpression=Key('title').eq(title)).get("Items")[0]
    if not ann:
        return {"statusCode": 404, "body": f"No se ha encontrado el anuncio {title}"}


    if 'user' in event['pathParameters']:
        owner = ann['owner']
        user = event['requestContext']['authorizer']['claims']['email']
        chat_id = title+'/'+event['pathParameters']['user']
        if not (user == owner or user == event['pathParameters']['user']):
            return {"statusCode": 403, "body": f"Usuario no autorizado en el chat"}
    else:
        chat_id = title
    

    chat = chats_table.query(KeyConditionExpression=Key('chat_id').eq(chat_id))
    messages = [{'fecha_hora': x['fecha_hora'], 'user_id': x['user_id'], 'message': x['message']} for x in chat.get("Items", [])]
    if not messages:
        return {"statusCode": 404, "body": "No messages found"}
    else:
        return {"statusCode": 200, "body": json.dumps(messages)}


def send_message(event, context):

    user = event['requestContext']['authorizer']['claims']['email']
    try:
        title = event['pathParameters']['title'].replace('%20', ' ')
    except KeyError:
        return {"statusCode": 400, "body": "No se ha indicado anuncio"}
    
    ann = advertisements_table.query(KeyConditionExpression=Key('title').eq(title)).get("Items")[0]
    if not ann:
        return {"statusCode": 404, "body": f"No se ha encontrado el anuncio {title}"}

    owner = ann['owner']

    if 'user' in event['pathParameters']:
        chat_id = title+'/'+event['pathParameters']['user']
        if not (user == owner or user == event['pathParameters']['user']):
            return {"statusCode": 403, "body": f"Usuario no autorizado en el chat"}
    else:
        chat_id = title

    message = json.loads(event.get('body', '{}'))
    if not message:
        return {"statusCode": 400, "body": "No se ha indicado body"}

    validate(instance=message, schema=schema_post)

    item = {
            'chat_id': chat_id,
            'fecha_hora': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            'user_id': user,
            'message': message['message'],
        }
    chats_table.put_item(Item=item)
    return {"statusCode": 201, "body": f"Posted in {chat_id}" }
