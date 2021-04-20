#!/usr/bin/evn python3
import boto3 
import csv 

ddb = boto3.resource('dynamodb')

def updateitem(tablename, patientID, city, patienturl):
    
    inftable = ddb.Table('Infections')
    
    response = inftable.update_item(
        Key={
            'PatientId': patientID,
            'City': city
        },
        UpdateExpression = 'SET patient_url = :patrrl',
        ExpressionAttributeValues = {':patrrl' : patienturl},
        ReturnValues = "UPDATED_NEW")
    return response
    
if __name__ == '__main__':
    pat1 = {'patientID': '1', 'city':'Salem','patrl': 'https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord1.txt'}
    pat2 = {'patientID': '2', 'city':'Gallup','patrl': 'https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord2.txt'}
    pat3 = {'patientID': '3', 'city':'Reno','patrl': 'https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord3.txt'}
    tablename = 'Infections'
    
    updateitem(tablename, pat1['patientID'], pat1['city'], pat1['patrl'])
    updateitem(tablename, pat2['patientID'], pat2['city'], pat2['patrl'])
    updateitem(tablename, pat3['patientID'], pat3['city'], pat3['patrl'])