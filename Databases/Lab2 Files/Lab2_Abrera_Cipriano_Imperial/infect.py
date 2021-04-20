#!/usr/bin/evn python3
import boto3 

ddb = boto3.resource('dynamodb')

def create_table(ddbtablename, partkey, sortkey, lsi):
    Infections = ddbtablename
    attribute_definitions = [
        {'AttributeName': partkey, 'AttributeType': 'S'},
        {'AttributeName': sortkey, 'AttributeType': 'S'}]
        
    key_schema = [
        {'AttributeName': partkey, 'KeyType': 'HASH'},
        {'AttributeName': sortkey, 'KeyType': 'RANGE'}]
        
    provision_thruput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    
    try: 
        infect = ddb.create_table(
            TableName = Infections,
            KeySchema = key_schema,
            AttributeDefinitions = attribute_definitions,
            ProvisionedThroughput = provision_thruput)
        return infect
    except Exception as err:
        print("Table cannot be created. Error Message: {0}".format(err))
            
if __name__ == '__main__':
    infect_table = create_table("Infections", "PatientId", "City", "Date")
    inftable = ddb.Table('Infections')
