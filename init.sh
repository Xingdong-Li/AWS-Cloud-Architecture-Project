# init.sh
#!/bin/bash

awslocal --endpoint-url=http://localstack:4566 s3 mb s3://mybucket
awslocal --endpoint-url=http://localstack:4566 dynamodb create-table --table-name Items --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
