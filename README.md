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

## AWS IAM Setting

Here is example IAM setting,

```js
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:DescribeLogStreams",
                "logs:DescribeLogGroups",
                "logs:FilterLogEvents"
            ],
            "Resource": "arn:aws:logs:ap-northeast-1:*:*",
            "Effect": "Allow"
        },
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DeleteLogGroup"
            ],
            "Resource": "arn:aws:logs:ap-northeast-1:<your AWS account number>:log-group:/aws/lambda/serverless-datarobot-*",
            "Effect": "Allow"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:GetRole",
                "iam:PassRole",
                "iam:PutRolePolicy",
                "iam:DeleteRolePolicy"
            ],
            "Resource": [
                "arn:aws:iam::<your AWS account number>:role/serverless-datarobot-*-lambdaRole"
            ]
        },
        {
            "Action": [
                "lambda:GetFunction",
                "lambda:GetFunctionConfiguration",
                "lambda:ListVersionsByFunction",
                "lambda:CreateFunction",
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "lambda:PublishVersion",
                "lambda:AddPermission",
                "lambda:InvokeFunction",
                "lambda:DeleteFunction"
            ],
            "Resource": "arn:aws:lambda:ap-northeast-1:<your AWS account number>:function:serverless-datarobot-*",
            "Effect": "Allow"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:Describe*"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:ValidateTemplate"
            ],
            "Resource": [
                "arn:aws:cloudformation:ap-northeast-1:<your AWS account number>:stack/serverless-datarobot-*/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:PutObject",
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": [
                "arn:aws:s3:::serverless-datarobot",
                "arn:aws:s3:::serverless-datarobot/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "SNS:Subscribe"
            ],
            "Resource": [
                "arn:aws:sns:ap-northeast-1:<your AWS account number>:serverless-datarobot*"
            ]
        }
    ]
}
```

Change your own setting,

- `<your AWS account number>` (e.g. 0123456789)
- `ap-northeast-1` for your `region`
- `serverless-datarobot` for your service name in `serverless.yml`
