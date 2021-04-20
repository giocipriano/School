#!/usr/bin/evn python3
import boto3 
import csv 

ddb = boto3.resource('dynamodb')

def batch_write(tablename, rows):
    tbl = ddb.Table(tablename)
    
    with tbl.batch_writer() as batch:
        for row in rows:
            batch.put_item(Item=row)
        return True

def scanfile(csvfile, list):
    rows = csv.DictReader(open(csvfile))
    
    for row in rows:
        list.append(row)
        
if __name__ == '__main__':
    tablename = 'Infections'
    csvfile = 'InfectionsData.csv'
    items = []
    
    scanfile(csvfile, items)
    status = batch_write(tablename, items)
    
    if (status):
        print('CSV file has been imported')
    else:
        print('Import failed')