#!/usr/bin/env python3

import boto3

import datetime
from datetime import datetime, timedelta


client = boto3.client('cloudwatch')
ec2client = boto3.client('ec2')

response = ec2client.describe_volumes()
for volume in response["Volumes"]:
    vid = volume["VolumeId"]
    environment = [tag['Value'] for tag in volume["Tags"] if tag['Key'] == 'environment'][0]
    Name = [tag['Value'] for tag in volume["Tags"] if tag['Key'] == 'Name'][0]
    stats=client.get_metric_statistics(
        Namespace='AWS/EBS',
        MetricName='BurstBalance',
        Dimensions=[
            {
                'Name': 'VolumeId',
                'Value': vid
            },
        ],
        StartTime=datetime.now() - timedelta(days=2),
        EndTime=datetime.now(),
        Period=3600,
        Statistics=['Minimum']
    )
    if not stats["Datapoints"]:
        print ("no_stats %s-%s %s" % (environment,Name,vid))
    else:
        mylist=[]
        for datapoint in stats["Datapoints"]:
            mylist.append(datapoint['Minimum'])
        print (min(mylist), "%s-%s %s" % (environment,Name,vid))
