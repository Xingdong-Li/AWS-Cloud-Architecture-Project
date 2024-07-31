# app/main.py
from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localstack:4566')
s3 = boto3.client('s3', region_name='us-east-1', endpoint_url='http://localstack:4566')

table = dynamodb.Table('Items')
bucket_name = 'mybucket'

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200

@app.route("/items/<item_id>", methods=['GET'])
def read_item(item_id):
    try:
        response = table.get_item(Key={'id': item_id})
        item = response.get('Item')
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/items", methods=['POST'])
def create_item():
    item = request.json
    try:
        table.put_item(Item=item)
        s3.put_object(Bucket=bucket_name, Key=item['id'], Body=str(item))
        return jsonify(item)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/items/<item_id>", methods=['PUT'])
def update_item(item_id):
    item = request.json
    try:
        table.update_item(
            Key={'id': item_id},
            UpdateExpression="set #name=:name, description=:description",
            ExpressionAttributeValues={
                ':name': item['name'],
                ':description': item['description']
            },
            ExpressionAttributeNames={
                "#name": "name"
            }
        )
        s3.put_object(Bucket=bucket_name, Key=item_id, Body=str(item))
        return jsonify(item)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/items/<item_id>", methods=['DELETE'])
def delete_item(item_id):
    try:
        table.delete_item(Key={'id': item_id})
        s3.delete_object(Bucket=bucket_name, Key=item_id)
        return jsonify({"message": "Item deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
