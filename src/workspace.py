#!/usr/bin/env python3
# coding=UTF-8
import os
import sys
import shutil
import ConfigParser
from logger import *

def generate_workspace(config, info):    
    cwd = os.path.abspath(os.getcwd())
    ws_dir = cwd + '/' + info['contest_id'] + info['problem_id']
    sample_dir = ws_dir + '/sample'
    
    if os.path.isdir(ws_dir):
        fatal('Directory {} do exist, exit.'.format(os.path.basename(ws_dir)))

    os.mkdir(ws_dir)

    if config:
        template_file = os.path.expandvars(config.get('wtf_cf', 'template_file'))
        shutil.copy(template_file, ws_dir + '/solution.' + config.get('wtf_cf', 'template_suffix'))

    os.mkdir(sample_dir)

    for (index, sample) in enumerate(info['test_samples']):
        with open(sample_dir + '/' + str(index) + '.in', 'w') as in_file:
            in_file.write(sample['input'])

        with open(sample_dir + '/' + str(index) + '.out', 'w') as out_file:
            out_file.write(sample['output'])

    conf = info
    conf['samples'] = len(info['test_samples'])
    conf['test_samples'] = None
    conf['compile_command'] = config.get('wtf_cf', 'compile_command') if config else 'echo "There\'s no global config file." && exit -1'

    config_file = ConfigParser.ConfigParser()
    config_file.add_section('project')

    for (key, value) in conf.items():
        if value:
            config_file.set('project', key, value)
  
    config_file.set('project', 'solution', 'solution.' + (config.get('wtf_cf', 'template_suffix') if config else 'cxx'))
    
    with open(ws_dir + '/config.ini', 'w') as file:
        config_file.write(file)

