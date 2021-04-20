#!/usr/bin/env python3
import boto3
from boto3.dynamodb.conditions import Key
import hashlib
import random
from decimal import Decimal
from pprint import pprint

def add_item(order_id, product_name, quantity, price, date): 
    
    item_id = hashlib.sha256(product_name.encode()).hexdigest()[:8]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    item = {
        'pk'           : '#ITEM#{0}'.format(item_id), 
        'sk'           : '#ORDER#{0}'.format(order_id),
        'product_name' : product_name,
        'quantity'     : quantity,
        'price'        : price,
        'statusDate'   : "Pending#{0}".format(date),
        'status'       : 'Pending'
    }
    table.put_item(Item=item)
    print("Added {0} to order {1}".format(product_name, order_id))
    
def checkout(username, address, items, date): 

    order_id = hashlib.sha256(str(random.random()).encode()).hexdigest()[:random.randrange(1, 20)]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    item = {
        'pk'            : '#USER#{0}'.format(username), 
        'sk'            : '#ORDER#{0}'.format(order_id),
        'address'       : address,
        'statusDate'    : "Shipping#{0}".format(date),
        'status'        : 'Shipping',
        'orderAdddress' : '{0}#ORDER#{1}'.format(address, order_id)
    }
    table.put_item(Item=item)
    
    for item in items:
        add_item(order_id, 
                 item['product_name'], 
                 item['quantity'], 
                 item['price'],
                 item['orderDate']
                 )

def query_user_orders(username):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('sk').begins_with('#ORDER#')
    )
    return response['Items']
    
def query_order_items(order_id):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        IndexName='inverted-index',
        KeyConditionExpression=Key('sk').eq('#ORDER#{0}'.format(order_id)) & 
                               Key('pk').begins_with('#ITEM#')
    )
    return response['Items']
    
def query_pending_orders(username):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    response = table.query(
        IndexName= 'user-filter-order-index',
        KeyConditionExpression = Key('pk').eq('#USER#{0}'.format(username)) & 
                                  Key('statusDate').begins_with('Pending#'))
    return response['Items']
    
def query_shipping_orders(username):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    response = table.query(
        IndexName= 'user-filter-order-index',
        KeyConditionExpression = Key('pk').eq('#USER#{0}'.format(username)) & 
                                 Key('statusDate').begins_with('Shipping#'))
    return response['Items']
    
def query_allpending():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    response = table.query(
        IndexName= 'pending-index',
        KeyConditionExpression = Key('status').eq('Pending') & 
                                 Key('sk').begins_with('#ORDER#'))
    return response['Items']
    
def query_allshipping():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    response = table.query(
        IndexName= 'pending-index',
        KeyConditionExpression = Key('status').eq('Shipping') & 
                                 Key('sk').begins_with('#ORDER#'))
    return response['Items']
    
if __name__ == '__main__':
    pprint(query_shipping_orders('tgrimes1'))