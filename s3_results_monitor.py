""" This can be used to check the results by watching the location in Amazon S3 where
the Alien Detector stores the results.
"""
import os
import time
import argparse

import boto3


BUCKET_KEY = 'RoboMakerS3Bucket'
MONITOR_PREFIX = 'detections'
SEARCH_OBJECT = 'Alien'
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

last_detect = None
try:
    while True:
        try:
            res = s3.get_object(Bucket=bucket, Key=SEARCH_DETECT_KEY)['Body'].read()
            if res != last_detect:
                last_detect = res
                print(res)
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e
        time.sleep(1)
except Exception as e:
    pass
print('Stopped')
    