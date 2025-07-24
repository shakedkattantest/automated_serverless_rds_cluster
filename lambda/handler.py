import json
import os
import boto3

def lambda_handler(event, context):
    print("Incoming Event:")
    print(json.dumps(event))

    # Extract body
    body = event.get("body")
    if body:
        try:
            payload = json.loads(body)
        except:
            return {"statusCode": 400, "body": "Invalid JSON"}
    else:
        return {"statusCode": 400, "body": "Missing request body"}

    # Publish to SNS
    sns = boto3.client("sns")
    topic_arn = os.environ["SNS_TOPIC_ARN"]

    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(payload),
        Subject="New RDS Provisioning Request"
    )

    return {
        "statusCode": 200,
        "body": "Request received. Processing..."
    }
