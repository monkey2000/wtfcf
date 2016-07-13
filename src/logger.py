#!/usr/bin/env python2
# coding=UTF-8
import colorama
import sys

def fatal(info):
    print(colorama.Style.RESET_ALL + colorama.Fore.RED + '[FATAL] ' + info)
    sys.exit(-1)


def warning(info):
    print(colorama.Style.RESET_ALL + colorama.Fore.YELLOW + '[WARN] ' + info)


def info(info):
    print(colorama.Style.RESET_ALL + colorama.Fore.WHITE + '[INFO] ' + info)

