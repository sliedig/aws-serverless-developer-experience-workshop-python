from typing import Any, List

import json
import hashlib
import uuid
import base64
import random
import time

from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent, SQSEvent


def apigw_event(http_method: str,
                resource: str,
                body: Any,
                b64encode: bool = False,
                path: str = '',
                stage: str = 'Local'
                ) -> APIGatewayProxyEvent:
    body_str = json.dumps(body)
    if b64encode:
        body_str = base64.b64encode(body_str.encode('utf-8'))

    return APIGatewayProxyEvent({
        "body": body_str,
        "resource": resource,
        "path": f'/{path}',
        "httpMethod": http_method,
        "isBase64Encoded": b64encode,
        "queryStringParameters": {
            "foo": "bar"
        },
        "multiValueQueryStringParameters": {
            "foo": [
                "bar"
            ]
        },
        "pathParameters": {
            "proxy": f"/{path}"
        },
        "stageVariables": {
            "baz": "qux"
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Custom User Agent String",
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "multiValueHeaders": {
            "Accept": [ "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" ],
            "Accept-Encoding": [ "gzip, deflate, sdch" ],
            "Accept-Language": [ "en-US,en;q=0.8" ],
            "Cache-Control": [ "max-age=0" ],
            "CloudFront-Forwarded-Proto": [ "https" ],
            "CloudFront-Is-Desktop-Viewer": [ "true" ],
            "CloudFront-Is-Mobile-Viewer": [ "false" ],
            "CloudFront-Is-SmartTV-Viewer": [ "false" ],
            "CloudFront-Is-Tablet-Viewer": [ "false" ],
            "CloudFront-Viewer-Country": [ "US" ],
            "Host": [ "0123456789.execute-api.us-east-1.amazonaws.com" ],
            "Upgrade-Insecure-Requests": [ "1" ],
            "User-Agent": [ "Custom User Agent String" ],
            "Via": [ "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)" ],
            "X-Amz-Cf-Id": [ "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==" ],
            "X-Forwarded-For": [ "127.0.0.1, 127.0.0.2" ],
            "X-Forwarded-Port": [ "443" ],
            "X-Forwarded-Proto": [ "https" ],
        },
        "requestContext": {
            "accountId": "123456789012",
            "resourceId": "123456",
            "stage": stage,
            "requestId": str(uuid.uuid4()),
            "requestTime": time.strftime("%d/%b/%Y:%H:%M:%S %z", time.gmtime()),
            "requestTimeEpoch": int(time.time()),
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "accessKey": None,
                "sourceIp": "127.0.0.1",
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "Custom User Agent String",
                "user": None,
            },
            "path": f"/{stage}/{path}",
            "resourcePath": resource,
            "httpMethod": http_method,
            "apiId": "1234567890",
            "protocol": "HTTP/1.1"
        }
    })


def sqs_event(messages: List[dict],
              queue_name: str = 'MyQueue',
              account_id: int = random.randint(100000000000,999999999999),
              aws_region: str = 'us-east-1'
              ) -> SQSEvent:

    records = []
    for message in messages:
        body = json.dumps(message.get('body', ''))
        md5ofbody = hashlib.md5(body.encode('utf-8')).hexdigest()
        rcv_timestamp = int(time.time() + (random.randint(0, 500)/1000))    # Random delay of 0-500ms
        
        records.append({
            "messageId": str(uuid.uuid4()),
            "receiptHandle": "MessageReceiptHandle",
            "body": body,
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": f"{int(time.time())}",
                "SenderId": f"{account_id}",
                "ApproximateFirstReceiveTimestamp": str(rcv_timestamp),
            },
            "messageAttributes": message.get('attributes', dict()),
            "md5OfBody": md5ofbody,
            "eventSource": "aws:sqs",
            "eventSourceARN": f"arn:aws:sqs:{aws_region}:{account_id}:{queue_name}",
            "awsRegion": aws_region,
        })

    return SQSEvent({ "Records": records })



# def sqs_event(messages: List[dict],
#               queue_name: str = 'MyQueue',
#               account_id: int = 0,
#               aws_region: str = 'us-east-1'
#               ) -> dict:
#     try:
#         return {
#             "Records": [
#                 sqs_record(m.get('body'), m.get('attributes', dict()),
#                         queue_name=queue_name,
#                         account_id=account_id,
#                         aws_region=aws_region)
#                 for m in messages
#             ]
#         }
#     except KeyError as e:
#         raise Exception(f'Each message should contain at least a `body` key: {messages}') from e


# def sqs_record(body: Any,
#                attributes: dict[str,Any] = dict(),
#                queue_name: str = 'MyQueue',
#                account_id: int = 0,
#                aws_region: str = 'us-east-1'
#                ) -> dict:
#     body = json.dumps(body)
#     if account_id == 0:
#         account_id = random.randint(100000000000,999999999999)
    
#     return {
#         "messageId": str(uuid.uuid4()),
#         "receiptHandle": "MessageReceiptHandle",
#         "body": body,
#         "attributes": {
#             "ApproximateReceiveCount": "1",
#             "SentTimestamp": int(time.time()),
#             "SenderId": f"{account_id}",
#             "ApproximateFirstReceiveTimestamp": str(int(time.time() + (random.randint(0, 500)/1000))),  # Random delay of 0-500ms
#         },
#         "messageAttributes": attributes,
#         "md5OfBody": hashlib.md5(body).hexdigest(),
#         "eventSource": "aws:sqs",
#         "eventSourceARN": f"arn:aws:sqs:{aws_region}:{account_id}:{queue_name}",
#         "awsRegion": aws_region,
#     }
