#!/usr/bin/env python2
# coding=UTF-8

import sys
import os
import re
import colorama
import ConfigParser
import urllib3
import subprocess32 as subprocess
import shutil
import time
from logger import *

CWD_PATH = os.path.abspath(os.getcwd())
SAMPLE_PATH = CWD_PATH + '/sample'
TEMP_PATH = CWD_PATH + '/tmp'
CONFIG_PATH = CWD_PATH + '/config.ini'
BINARY_PATH = CWD_PATH + '/binary'

DEVNULL = open(os.devnull, 'wb')

config = ConfigParser.ConfigParser()

def compile():
    if os.path.isfile(BINARY_PATH):
        info('Compiled binary found, delete.')
        os.remove(BINARY_PATH)
    
    ret = subprocess.call(config.get('project', 'compile_command').format(
        CWD_PATH + '/' + config.get('project', 'solution'), BINARY_PATH
    ), shell=True)

    if ret is not 0:
        fatal('Compiling failed')

def run_test():
    if os.path.isdir(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)

    os.mkdir(TEMP_PATH)

    sleep_time = int(config.get('project', 'time_limit')) / 1000.0
    
    for i in range(int(config.get('project', 'samples'))):
        status = 'UNKNOWN'
        with open(SAMPLE_PATH + '/' + str(i) + '.in', 'r') as input_file, \
             open(TEMP_PATH + '/' + str(i) + '.ans', 'w') as answer_file:
            ret = None

            try:
                ret = subprocess.call(BINARY_PATH, shell=True,
                        stdin=input_file, stdout=answer_file, timeout=sleep_time)
            except subprocess.TimeoutExpired:
                pass
            
            if ret == None:
                status = 'TLE'
            elif ret == 0:
                ret = subprocess.call('diff --brief -w -B {0} {1}'.format(
                    TEMP_PATH + '/' + str(i) + '.ans',
                    SAMPLE_PATH + '/' + str(i) + '.out'
                ), shell=True, stdout=DEVNULL)
                if ret == 0:
                    status = 'AC'
                elif ret == 1:
                    status = 'WA'
                else:
                    status = 'RE'
            else:
                status = 'RE'

            print colorama.Style.RESET_ALL + \
                (colorama.Fore.RED if status != 'AC' else colorama.Fore.GREEN) + \
                'Test Case #{}: [{}]'.format(i, status)

def main():
    if not os.path.isfile(CONFIG_PATH):
        fatal('There\'s no config file!')

    config.read(CONFIG_PATH)

    info('Compile the code')
    compile()
    info('Compile successfully')

    info('Run test cases: ')
    run_test()

if __name__ == '__main__':
    main()
