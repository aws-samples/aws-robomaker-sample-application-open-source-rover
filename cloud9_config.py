""" Script to simplify the Cloud9 IDE configuration. 
This works together with the CloudFormation template used to seed the workshop and a `roboMakerSettings.json` configuration file supplied
as part of this project. Any changes to those will require reviewing this script
"""

import os
import json
import argparse
import re
import shutil

import boto3

# LAUNCH_FILE_PATH = 'robot_ws/src/martian_detector/launch/martian_detector.launch'
CONFIG_FILE_NAME = 'roboMakerSettings.json'
SIM_CONFIG_ID = 'sim-robot-with-simple-world'
BUCKET_KEY = 'RoboMakerS3Bucket'
REGION_KEY = 'REGION'
CFN_CONFIG_KEYS = {
    BUCKET_KEY: ['cfg.simulation.outputLocation', 'cfg.robotApp.s3Bucket', 'cfg.simulationApp.s3Bucket', 'cfg.robotApp.launchConfig.environmentVariables.S3_BUCKET'],
    'SimulationRole': ['cfg.simulation.iamRole'],
    'DefaultSecurityGroupID': ['cfg.simulation.vpcConfig.securityGroups'],
    'PublicSubnet1': ['cfg.simulation.vpcConfig.subnets'],
    'PublicSubnet2': ['cfg.simulation.vpcConfig.subnets']
}

EXTRA_CONFIG_KEYS = {
    REGION_KEY: ['cfg.robotApp.launchConfig.environmentVariables.REGION']
}

def set_value(obj, target_keys, val):
    for target_keys in target_keys:
        cfg = obj
        key_parts = target_keys.split('.')
        
        # Move down the config hierarcy until before the last, creating missing elements. 
        for k in key_parts[:-1]:
            if k not in cfg:
                cfg[k] = {}
            cfg = cfg[k]

        if isinstance(cfg[key_parts[-1]], list):
            cfg[key_parts[-1]].append(val)
        else:
            cfg[key_parts[-1]] = val
            
parser = argparse.ArgumentParser(description='Mars Rover RoboMaker Config')
parser.add_argument('--cloudformation-stack-name', dest='cf_stack_name', type=str, help='Full name of the workshop seeding CloudFormation stack')
parser.add_argument('--project-root-dir', type=str, default='aws-robomaker-sample-application-open-source-rover', 
                    help="Path to the Mars Rover root directory, absolute or relative to the directory from which this script is executed")
parser.add_argument('--config-target-dir', type=str, default='./', help="Path to a directory to save the configured '{}' file".format(CONFIG_FILE_NAME))
args = parser.parse_args()

print("Getting info from CloudFormation stack '{}'".format(args.cf_stack_name))
cfn = boto3.client('cloudformation')

stack_info = cfn.describe_stacks(StackName=args.cf_stack_name)
outputs = stack_info['Stacks'][0]['Outputs']

print('Configuring the RoboMaker menu')

template_config_file = os.path.join(args.project_root_dir, CONFIG_FILE_NAME)
print('- loading config template: {}'.format(template_config_file))
with open(template_config_file) as fin:
    config = json.loads(fin.read())

sim_config = None    
for c in config['runConfigurations']:
    if c['id'] == SIM_CONFIG_ID:
        sim_config = c
        break
if sim_config is None:
    raise RuntimeError('{} not round in the template config'.format(SIM_CONFIG_ID))

# Set values from CloudFormation 
for key in CFN_CONFIG_KEYS:
    
    # Find the value in the CFN outputs
    val = None
    for output in outputs:
        if output['OutputKey'] == key:
            val = output['OutputValue']
            break
    if val is None:
        raise RuntimeError('{} not round in the CloudFormation output'.format(key))
        
    set_value(sim_config, CFN_CONFIG_KEYS[key], val)

# Set the other config values
for key in EXTRA_CONFIG_KEYS:
    if key == REGION_KEY:
        set_value(sim_config, EXTRA_CONFIG_KEYS[key], cfn.meta.region_name)
        
out_config_file = os.path.join(args.config_target_dir, CONFIG_FILE_NAME)
print('- saving config to {}'.format(out_config_file))
with open(out_config_file, 'w') as fout:
    fout.write(json.dumps(config, indent=2))
 
# launch_file = os.path.join(args.project_root_dir, LAUNCH_FILE_PATH)
# print('Configuring Martian detector: {}'.format(launch_file))

# backup_launch_file = launch_file + '_original'
# if not os.path.exists(backup_launch_file):
#     print('- back up launch file to {}'.format(backup_launch_file))
#     shutil.copy(launch_file, backup_launch_file)
    
# with open(launch_file) as fin:
#     launch = fin.read()

# param_name = 'auto_capture'
# matches = re.findall('(<arg[^>]*name\s*=\s*"{}"[^>]*>)'.format(param_name), launch)
# if len(matches) > 1:
#     raise RuntimeError('Found more that one {} arg'.format(param_name))
# elif len(matches) == 1:
#     print('- enable {}'.format(param_name))
#     launch = launch.replace(matches[0], '<arg name="{}" default="true" />'.format(param_name))

# param_name = 'aws_region'
# matches = re.findall('(<arg[^>]*name\s*=\s*"{}"[^>]*>)'.format(param_name), launch)
# if not matches:
#     raise RuntimeError('{} argument not found'.format(param_name))
# elif len(matches) == 1:
#     print('- set {}'.format(param_name))
#     launch = launch.replace(matches[0], '<arg name="{}" default="{}" />'.format(param_name, cfn.meta.region_name))

# param_name = 's3_bucket_name'
# matches = re.findall('(<param[^>]*name\s*=\s*"{}"[^>]*>)'.format(param_name), launch)
# if not matches:
#     raise RuntimeError('{} parameter not found'.format(param_name))
# elif len(matches) == 1:
#     print('- set {}'.format(param_name))
#     launch = launch.replace(matches[0], '<param name="{}" value="{}" />'.format(param_name, bucket))
    
# print('- saving')
# with open(launch_file, 'w') as fout:
#     fout.write(launch)   
    
print('SUCCEEDED')