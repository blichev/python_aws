#!/usr/bin/env python

# print a list of all instances in the region with ip and environmen-name tags from AWS

import boto3

ec2client = boto3.client('ec2')
response = ec2client.describe_instances()
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instanceid = instance["InstanceId"]
        state = instance["State"]["Name"]
        privateip = instance["PrivateIpAddress"]
        environment = [tag['Value'] for tag in instance["Tags"] if tag['Key'] == 'environment'][0]
        Name = [tag['Value'] for tag in instance["Tags"] if tag['Key'] == 'Name'][0]
        print "%s %s-%s %s %s" % (privateip,environment,Name,instanceid,state)
