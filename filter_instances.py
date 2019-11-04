#!/usr/bin/env python

# print a filtered list of ec2 instances. For a list of filters visit: http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_instances

import boto3

ec2client = boto3.client('ec2')
response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'tag:environment',
            'Values': ['qa3']
        },
        {
            'Name': 'instance-type',
            'Values': ['t3*']
        }
    ]
)
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instanceid = instance["InstanceId"]
        state = instance["State"]["Name"]
        privateip = instance["PrivateIpAddress"]
        environment = [tag['Value'] for tag in instance["Tags"] if tag['Key'] == 'environment'][0]
        Name = [tag['Value'] for tag in instance["Tags"] if tag['Key'] == 'Name'][0]
        print "%s %s-%s %s %s" % (privateip,environment,Name,instanceid,state)
