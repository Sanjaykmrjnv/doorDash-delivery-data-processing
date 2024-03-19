import json
import boto3
import pandas as pd

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        json_data = json.loads(data)
        
        df = pd.DataFrame(json_data)
        
        df_delivered = df[df['status'] == 'delivered']
        
        json_filtered = df_delivered.to_json(orient='records')
        
        target_bucket = 'doordash-target-sa'
        target_key = f"{key.split('/')[-1].split('.')[0]}-filtered.json"  # Change the filename as needed
        s3.put_object(Bucket=target_bucket, Key=target_key, Body=json_filtered)
        
        # Publish a success message to SNS topic
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:767397935988:doordash-notification-service',
            Message='Data processing completed successfully.'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data processing completed successfully.')
        }
    except Exception as e:
        # Publish a failure message to SNS topic
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:767397935988:doordash-notification-service',
            Message=f'Data processing failed: {str(e)}'
        )
        
        return {
            'statusCode': 500,
            'body': json.dumps(f'Data processing failed: {str(e)}')
        }
