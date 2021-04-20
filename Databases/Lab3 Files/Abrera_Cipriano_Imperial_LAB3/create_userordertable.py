#!/usr/bin/env python3
import boto3

def create_invert_table(
    ddb_table_name,
    partition_key,
    sort_key,
    lsi):
        
    dynamoo = boto3.resource('dynamodb')
    tablename = ddb_table_name
    
    attribute_definitions = [
        {'AttributeName': partition_key, 'AttributeType': 'S'},
        {'AttributeName': sort_key, 'AttributeType': 'S'},
        {'AttributeName': 'status', 'AttributeType': 'S'},
        {'AttributeName': 'statusDate', 'AttributeType': 'S'}]
        
    key_schema = [
        {'AttributeName': partition_key, 'KeyType': 'HASH'},
        {'AttributeName': sort_key, 'KeyType': 'RANGE'}]
        
    provision_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}

    global_secondary_indexes = [{
            'IndexName': 'inverted-index',
            'KeySchema': [
                {'AttributeName': sort_key, 'KeyType': 'HASH'},
                {'AttributeName': partition_key, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'INCLUDE',
                           'NonKeyAttributes': ['quantity',	'price', 'statusDate', 'product_name', 'date']
            },
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    }, 
    {
            'IndexName': 'pending-index',
            'KeySchema': [
                {'AttributeName': 'status', 'KeyType': 'HASH'},
                {'AttributeName': sort_key, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'INCLUDE',
                           'NonKeyAttributes': ['quantity',	'price', 'product_name', 'date']
            },
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    }]
    
    local_secondary_indexes = [{
            'IndexName': 'user-filter-order-index',
            'KeySchema': [
                {'AttributeName': sort_key, 'KeyType': 'HASH'},
                {'AttributeName': 'statusDate', 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'INCLUDE',
                           'NonKeyAttributes': ['quantity',	'price', 'product_name', 'date']
            }
    }]
    
    try:
        table = dynamoo.create_table(
            TableName=tablename,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provision_throughput,
            GlobalSecondaryIndexes=global_secondary_indexes,
            LocalSecondaryIndexes=local_secondary_indexes)
        return table
    except Exception as err:
        print("{0} table could not be created.".format(tablename))
        print("Error message: {0}".format(err))

def delete_table(name):
    dynamoo = boto3.resource('dynamodb')
    table = dynamoo.Table(name)
    table.delete()

if __name__ == '__main__':
    table = create_invert_table("users-orders-items", "pk", "sk", "orderAddress")