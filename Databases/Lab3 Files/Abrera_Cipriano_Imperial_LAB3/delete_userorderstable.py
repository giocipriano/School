#!/usr/bin/env python3
import boto3

def delete_table(name):
    dynamoo = boto3.resource('dynamodb')
    table = dynamoo.Table(name)
    table.delete()
    
if __name__ == '__main__':
    delete_table("users-orders-items")