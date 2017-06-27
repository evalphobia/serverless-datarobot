serverless-datarobot
====

DataRobot Prime Web API on AWS Lambda.


# Usage

## Single function

This is template for single AWS Lambda function.

- 1. update `model.py` to your DataRobot Prime python code.
- 2. Install serverless plugins `npm install`
- 3. Install python modules `sls requirements install`
- 4. Deploy function `AWS_ACCESS_KEY_ID=<your access key> AWS_SECRET_ACCESS_KEY=<your secret key> sls deploy`


## Multiple function

This is template for multiple AWS Lambda function.

- 1. update `model.py` to your DataRobot Prime python code.
- 2. Install serverless plugins `npm install`
- 3. Deploy function `AWS_ACCESS_KEY_ID=<your access key> AWS_SECRET_ACCESS_KEY=<your secret key> sls deploy`


## HTTP API

### POST /predict

Get prediction results by given parameters.
Response is number array style and prediction results are shown in the `"predicts"` key of response.

- exmaple

```bash
# Single prediction

$ curl -XPOST https://<your api domain>/predict \
   -H 'Content-Type: application/json' \
   -d '{ "user_id": 100, "age": 20 }'

{"error": null, "code": 200, "predicts": [0.3727827380524341]}
```

```bash
# Multiple prediction

$ curl -XPOST https://<your api domain>/predict \
   -H 'Content-Type: application/json' \
   -d '[{ "user_id": 100, "age": 20 }, { "user_id": 200, "age": 35 }]'

{"error": null, "code": 200, "predicts": [0.3727827380524341, 0.26119423557818366]}
```

### POST /predict?key=<_key_>

Get prediction results by given parameters.
Response is object array style which is created by the `<key>`.

- exmaple

```bash
# Single prediction

$ curl -XPOST https://<your api domain>/predict?key=user_id \
   -H 'Content-Type: application/json' \
   -d '{ "user_id": 100, "age": 20 }'

{"error": null, "code": 200, "data": [{"user_id": 100, "predict": 0.3727827380524341}]}
```

```bash
# Multiple prediction

$ curl -XPOST https://<your api domain>/predict?key=user_id \
   -H 'Content-Type: application/json' \
   -d '[{ "user_id": 100, "age": 20 }, { "user_id": 200, "age": 35 }]'

{"error": null, "code": 200, "data": [{"user_id": 100, "predict": 0.3727827380524341}, {"user_id": 200, "predict": 0.26119423557818366}]}
```

## Local Test

Modify `"body"` in `event.json` file.
Then hit command below,

```bash
$ sls invoke local -f datarobot --path event.json
```
