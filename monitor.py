""" Script to monitor what the Rover is seeing
"""
from __future__ import print_function

import os
import time
import argparse

import boto3


BUCKET_KEY = 'RoboMakerS3Bucket'
MONITOR_PREFIX = 'detections'
SEARCH_OBJECT = 'Alien'
ALL_DETECT_KEY = os.path.join(MONITOR_PREFIX, 'objects.txt')
SEARCH_DETECT_KEY = os.path.join(MONITOR_PREFIX, '{}.txt'.format(SEARCH_OBJECT))

parser = argparse.ArgumentParser(description='Mars Rover RoboMaker Monitor')
parser.add_argument('--cloudformation-stack-name', dest='cf_stack_name', type=str, help='Full name of the workshop seeding CloudFormation stack')
args = parser.parse_args()

print("Getting info from CloudFormation stack '{}'".format(args.cf_stack_name))
cfn = boto3.client('cloudformation')

stack_info = cfn.describe_stacks(StackName=args.cf_stack_name)
outputs = stack_info['Stacks'][0]['Outputs']

# Find the bucket
bucket = None
for output in outputs:
    if output['OutputKey'] == BUCKET_KEY:
        bucket = output['OutputValue']
        break
if bucket is None:
    raise RuntimeError('{} not round in the CloudFormation output'.format(BUCKET_KEY))

s3 = boto3.client('s3')

last_detect = last_search_detect = None
last_message_time = time.time()
try:
    while True:
        try:
            # detect = s3.get_object(Bucket=bucket, Key=ALL_DETECT_KEY)['Body'].read()
            # if last_detect is None:
            #     last_detect = detect
                
            res = s3.get_object(Bucket=bucket, Key=SEARCH_DETECT_KEY)['Body'].read()
            if res != last_search_detect:
                last_search_detect = res
                print(res)
                last_message_time = time.time()
            # elif last_message_time + 1 < time.time() and detect != last_detect:
            #     print('.', end='')
            #     # print('-')
            #     last_detect = detect
            #     last_message_time = time.time()
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
        time.sleep(1)
except Exception as e:
    pass
print('Stopped')
    