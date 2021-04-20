import boto3
import pandas as pd #to import csv files into this python file 
import json
import os
import csv



def create_table( #!def to create keyword
    ddb_table_name,
    partition_key,
    sort_key,
    lsi,
    ):
        
    dynamodb = boto3.resource('dynamodb')
    infections = ddb_table_name
        
        
        
    attribute_definitions = [
            {'AttributeName': partition_key, 'AttributeType': 'S'},
            {'AttributeName': sort_key, 'AttributeType': 'S'},
            ]
        
    key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}, #partition key used to partition table in diff segments
                  {'AttributeName': sort_key, 'KeyType': 'RANGE'}] #used to sort records in that specific partition; you should always 
                  #define partition as HASH and sort as RANGE 
                  
        
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10} #how many units per seconds (5 and 10)
         

    #create table function
    
    try:
            # Create a DynamoDB table with the parameters provided
        table = dynamodb.create_table(TableName=infections,
                                     KeySchema=key_schema,
                                     AttributeDefinitions=attribute_definitions,
                                     ProvisionedThroughput=provisioned_throughput,
                                     )
        return table
    except Exception as err:
        print("{0} Table could not be created".format(infections))
        print("Error message {0}".format(err))
        
def delete_table(name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(name)
    table.delete()

if __name__ == '__main__':
    infections_table = create_table("infections", "PatientId", "City", "Date")

    
    
if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    infections = dynamodb.Table('infections')
    
    
with open('InfectionsData.csv') as InfectionsData:
    data = csv.DictReader(InfectionsData)
    for row in data:
        infections.put_item(Item=row)