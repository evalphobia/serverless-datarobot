import json
import pandas
import model


def predict(event, context):
    """Run prediction."""
    # print "Received event: " + json.dumps(event, indent=2)
    data = event
    if 'body' in event:
        data = json.loads(event['body'])

    key = None
    if 'queryStringParameters' in event and event['queryStringParameters'] and 'key' in event['queryStringParameters']:
        key = event['queryStringParameters']['key']
        if key not in data:
            return response_error400('Cannot find the key: %s' % key)

    params = _to_list(data)
    ds = pandas.DataFrame.from_dict(params)
    ds = model.rename_columns(ds)
    ds = model.convert_bool(ds)
    model.validate_columns(ds.columns)
    ds = model.parse_numeric_types(ds)
    ds = model.add_missing_indicators(ds)
    ds = model.impute_values(ds)
    ds = model.combine_small_levels(ds)
    predicts = model.predict_dataframe(ds)

    if key:
        result = [{key: params[i][key], 'predict': predicts[i]} for i in range(predicts.size)]
        return response_success({'data': result})
    else:
        return response_success({'predicts': predicts.tolist()})


def _to_list(val):
    """Return the variable converted to list type."""
    if isinstance(val, list):
        return val
    else:
        return [val]


def response_success(data):
    """Return success response."""
    body = {
        "error": None,
        "code": 200,
    }
    data.update(body)
    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }


def response_error400(err):
    """Return error response."""
    return {
        "statusCode": 400,
        "body": {
            "code": 400,
            "error": err
        }
    }
