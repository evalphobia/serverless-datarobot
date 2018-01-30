import json

BODY = {
    'error': None,
    'code': 200,
    'status': 'ok',
}

RESPONSE = {
    'statusCode': 200,
    'body': json.dumps(BODY)
}


def status(event, context):
    """Return status."""
    return RESPONSE
