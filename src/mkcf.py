#!/usr/bin/env python2
# coding=UTF-8

import sys
import os
import re
import colorama
import ConfigParser
import urllib3
from workspace import generate_workspace
from logger import *
from bs4 import BeautifulSoup

CONFIG_PATH = os.path.abspath(os.path.expanduser('~')) + '/.wtfcf.ini'
PID_PATTERN = [
    re.compile('/contest/(\d*)/problem/(.*)'),
    re.compile('/problem/(\d*)/(.*)')
]

http = urllib3.PoolManager()
config = ConfigParser.ConfigParser()

def init_config():
    global config
    if not os.path.isfile(CONFIG_PATH):
        warning('Your ~/.wtfcf.ini do not exist.')
        warning('This may cause strange behavior.')
        config = None
    else:
        config.read(CONFIG_PATH)

def init_proxy():
    if config.has_option('proxy', 'type') and \
            config.has_option('proxy', 'url'):
        url = config.get('proxy', 'url')
        if config.get('proxy', 'type') == 'http':
            http = urllib3.ProxyManager(url)
            info('HTTP Proxy on ' + url + ' attached. ')
        elif config.get('proxy', 'type') == 'socks':
            from urllib3.contrib.socks import SOCKSProxyManager
            http = SOCKSProxyManager(config.get('proxy', 'url'))
            info('Socks Proxy on ' + url + ' attached. ') 

TIME_LIMIT_PATTERN = [
    (re.compile('(\d*) second'), lambda mat: int(mat[0]) * 1000)
]

def parse_time_limit(time):
    for regex, func in TIME_LIMIT_PATTERN:
        result = regex.findall(time)
        if len(result) == 1:
            return func(result)


def get_info(url):
    req = http.request('GET', url)
   
    if req.status != 200:
        fatal('Bad request: ' + str((url, req.status,)))

    contest_id = -1
    problem_id = 'Z'
    for regex in PID_PATTERN:
        result = regex.findall(url)
        if len(result) == 1 and len(result[0]) == 2:
            contest_id = result[0][0]
            problem_id = result[0][1]

    html = BeautifulSoup(req.data, "html.parser")
    title = html.select('.header > .title')[0].get_text()

    tmp = html.select('.header > .time-limit > .property-title')[0].get_text()
    time_limit = html.select('.header > .time-limit')[0].get_text()[len(tmp):]
    time_limit = parse_time_limit(time_limit)

    samples = html.select('.sample-test')[0]
    children = list(samples.children)

    if len(children) % 2:
        fatal('Bad length of samples: ' + repr(samples.children))

    test_samples = []
    for (input_dom, output_dom) in zip(children[::2], children[1::2]):
        test_samples.append({
            'input': '\n'.join(list(input_dom.find('pre').stripped_strings)),
            'output': '\n'.join(list(output_dom.find('pre').stripped_strings))
        })

    return {
        'problem_id': problem_id,
        'contest_id': contest_id,
        'title': title,
        'time_limit': time_limit,
        'test_samples': test_samples
    }


def print_info(info):
    print(colorama.Fore.BLUE + 'Problem ID: {}{}'.format(info['contest_id'], info['problem_id']))
    print(colorama.Fore.MAGENTA + 'Time Limit for each test: {}ms'.format(info['time_limit']))
    print(colorama.Fore.MAGENTA + 'Number of samples: {}'.format(len(info['test_samples'])))


def main():
    colorama.init()
    init_config()
    init_proxy()

    if len(sys.argv) <= 1:
        fatal('Missing wtf parameter, should be a problem url on CF.')

    target = sys.argv[1]

    info('Start crawling ' + target)

    data = get_info(target)

    info('Crawl metadata successfully.')
    print_info(data)

    generate_workspace(config, data)
    info('Generate worksapce successfully.')
    info('Enjoy! :D')

if __name__ == '__main__':
    main()
