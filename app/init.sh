#!/bin/bash

# Create an S3 bucket
awslocal s3 mb s3://mybucket --endpoint-url=http://localstack:4566
# Create a DynamoDB table
awslocal dynamodb create-table \
    --table-name Items \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --endpoint-url=http://localstack:4566