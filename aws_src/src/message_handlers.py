import json
import os
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler_put(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON"})}

    message = body.get("message")
    source = body.get("source", "unknown")
    if not message or not isinstance(message, str):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing or invalid 'message' field"}),
        }

    item = {
        "MessageId": str(uuid.uuid4()),
        "message": message,
        "source": source,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"MessageId": item["MessageId"], "timestamp": item["timestamp"]}
        ),
    }


def lambda_handler_get(event, context):
    query_params = event.get("queryStringParameters") or {}
    source = query_params.get("source")
    if not source or not isinstance(source, str):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "Missing or invalid 'source' query parameter"}
            ),
        }

    response = table.query(
        KeyConditionExpression=Key("source").eq(source),
        ScanIndexForward=False,  # Sort by timestamp in descending order
        Limit=1,
    )
    latest_message = response.get("Items", [])[0] if response.get("Items") else None
    body = (
        json.dumps(latest_message)
        if latest_message
        else json.dumps({"message": "No messages found for the given source"})
    )

    return {
        "statusCode": 200,
        "body": body,
    }
