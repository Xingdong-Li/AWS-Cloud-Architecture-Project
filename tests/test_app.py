import pytest
import boto3
from flask import json
from app.main import app

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        yield client

def test_create_item(test_client):
    response = test_client.post('/items', json={'id': '1', 'name': 'Item 1', 'description': 'A test item'})
    assert response.status_code == 200

def test_read_item(test_client):
    response = test_client.get('/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == '1'
    assert data['name'] == 'Item 1'
    assert data['description'] == 'A test item'

def test_update_item(test_client):
    response = test_client.put('/items/1', json={'id': '1', 'name': 'Updated Item', 'description': 'Updated description'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == '1'
    assert data['name'] == 'Updated Item'
    assert data['description'] == 'Updated description'

def test_delete_item(test_client):
    response = test_client.delete('/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Item deleted'
