import boto3
import pandas  as pd

def lambda_handler(event, context):
    print("Event -> ",event)
    print("Context -> ",context)

    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    df = pd.read_json(obj['Body'])

    delivered_records = df[df['status'] == 'delivered']

    target_bucket = 'doordash-target-sa'
    target_key = s3_key.replace('landing', 'target')  # Adjust key to target bucket
    target_obj = {'Bucket': target_bucket, 'Key': target_key}
    s3.put_object(Body=delivered_records.to_json(), **target_obj)

    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:767397935988:doordash-notification-service'  # Specify your SNS topic ARN
    sns.publish(TopicArn=topic_arn, Message='Delivery data processing completed successfully.')

    return {
        'statusCode': 200,
        'body': 'Processing completed.'
    }