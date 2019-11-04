#!/usr/bin/env python3

import boto3

import datetime
from datetime import datetime, timedelta


client = boto3.client('cloudwatch')
ec2client = boto3.client('ec2')

response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'instance-type',
            'Values': ['t*']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
)
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        iid = instance["InstanceId"]
        environment = [tag['Value'] for tag in instance["Tags"] if tag['Key'] == 'environment'][0]
        Name = [tag['Value'] for tag in instance["Tags"] if tag['Key'] == 'Name'][0]
        stats = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUCreditBalance',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': iid
            },
        ],
        StartTime=datetime.now() - timedelta(days=2),
        EndTime=datetime.now(),
        Period=3600,
        Statistics=['Minimum']
        )
        mylist=[]
        for datapoint in stats["Datapoints"]:
            mylist.append(datapoint['Minimum'])
        print (min(mylist), "%s-%s" % (environment,Name))
