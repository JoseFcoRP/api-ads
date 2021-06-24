import boto3
import os
import uuid
from PIL import Image
from io import BytesIO
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')
bucket = os.environ.get('Bucket')
advertisements_table = boto3.resource('dynamodb').Table(os.environ.get('DDB_AD'))


def resize_image(tmp_path, des_bucket, upload_path):
    size = 50, 50
    in_mem_file = BytesIO()
    im = Image.open(tmp_path)
    im.thumbnail(size, Image.ANTIALIAS)
    # ISSUE : https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    im.save(in_mem_file, format=im.format)
    in_mem_file.seek(0)

    s3_client.put_object(
        Body=in_mem_file,
        Bucket=des_bucket,
        Key=upload_path
    )

def resize(event, context):
    record = event['Records'][0]
    key = unquote_plus(record['s3']['object']['key'])
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), key.split('/')[-1])
    upload_path = key.replace('raw', 'resized')
    s3_client.download_file(bucket, key, download_path)
    resize_image(download_path, bucket, upload_path)
    advertisements_table.update_item(Key={'title': key.split('/')[-2]},
                                        UpdateExpression="set image_resized = :r",
                                        ExpressionAttributeValues={':r': f"https://{bucket}.s3.eu-west-1.amazonaws.com/{upload_path}"}
                                    )