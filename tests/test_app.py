import pytest
import boto3
from flask import json
from app.main import app

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def s3_client():
    return boto3.client('s3', region_name='us-east-1', endpoint_url='http://localstack:4566')

def test_create_item(test_client, s3_client):
    response = test_client.post('/items', json={'id': '1', 'name': 'Item 1', 'description': 'A test item'})
    assert response.status_code == 200

    # Verify the item in S3
    s3_response = s3_client.get_object(Bucket='mybucket', Key='1')
    s3_data = json.loads(s3_response['Body'].read())
    assert s3_data['id'] == '1'
    assert s3_data['name'] == 'Item 1'
    assert s3_data['description'] == 'A test item'

def test_read_item(test_client):
    response = test_client.get('/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == '1'
    assert data['name'] == 'Item 1'
    assert data['description'] == 'A test item'

def test_update_item(test_client, s3_client):
    response = test_client.put('/items/1', json={'id': '1', 'name': 'Updated Item', 'description': 'Updated description'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == '1'
    assert data['name'] == 'Updated Item'
    assert data['description'] == 'Updated description'

    # Verify the updated item in S3
    s3_response = s3_client.get_object(Bucket='mybucket', Key='1')
    s3_data = json.loads(s3_response['Body'].read())
    assert s3_data['id'] == '1'
    assert s3_data['name'] == 'Updated Item'
    assert s3_data['description'] == 'Updated description'

def test_delete_item(test_client, s3_client):
    response = test_client.delete('/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Item deleted'

    # Verify the item is deleted from S3
    with pytest.raises(s3_client.exceptions.NoSuchKey):
        s3_client.get_object(Bucket='mybucket', Key='1')
