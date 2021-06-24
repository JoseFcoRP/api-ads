import os, boto3
from datetime import datetime, timezone


advertisements_table = boto3.resource('dynamodb').Table(os.environ.get('DDB_AD'))


def delete_ads(event, context):
    fecha_actual = datetime.utcnow().replace(tzinfo=timezone.utc)
    THRESHOLD = int(os.environ.get('THRESHOLD'))
    ann = advertisements_table.scan(Select='SPECIFIC_ATTRIBUTES', AttributesToGet=['title', 'creation_date'])
    for ad in ann.get("Items", []):
        fecha = datetime.fromisoformat(ad['creation_date'])
        if (fecha_actual-fecha).days > THRESHOLD:
            advertisements_table.delete_item(Key={'title': ad['title']})
