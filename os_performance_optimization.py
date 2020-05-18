#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************#
# ScriptName: os_performance_optimization.py
# Create Date: 2020-02-22 09:00
# Modify Date: 2020-02-22 09:00
# ***************************************************************#

from __future__ import print_function
import os
import sys
import datetime

suggested_sysctl_params_basic = {
    'net.ipv4.tcp_syncookies': "1",
    'net.core.somaxconn': "4096",
    'net.netfilter.nf_conntrack_max': "655350",
    'net.ipv4.tcp_max_syn_backlog': "8192",
    'net.ipv4.ip_local_port_range': "1024 65000",
    'net.ipv4.tcp_max_tw_buckets': "50000",
    'net.netfilter.nf_conntrack_tcp_timeout_established': '1200',
    'net.ipv4.tcp_timestamps': "1",
    'net.ipv4.tcp_tw_recycle': "0",
    'net.ipv4.tcp_tw_reuse': "1",
    'net.ipv4.tcp_fin_timeout': "30",
}

suggested_limits = '''
root soft nofile 655350
root hard nofile 655350
root soft nproc 655350
root hard nproc 655350
* soft nofile 655350
* hard nofile 655350
* soft nproc 655350
* hard nproc 655350
'''

def save_sysctl():
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    sysctl = open('/etc/sysctl.conf', 'r')

    print("Backing up sysctl.conf as /etc/sysctl.conf.%s" % now)
    os.system('cp /etc/sysctl.conf /etc/sysctl.conf.%s' % now)

    sysctl_new = open('/tmp/sysctl.conf', 'w')
    for line in sysctl.readlines():
        line = line.strip()
        for k, v in suggested_sysctl_params_basic.items():
            if str(k) in line:
                break
        else:
            line = line + '\n'
            sysctl_new.write(line)

    for k, v in suggested_sysctl_params_basic.items():
        line_new = k + ' = ' + v + '\n'
        sysctl_new.write(line_new)

    sysctl.close()
    sysctl_new.close()
    os.system('rm -f /etc/sysctl.conf')
    os.system('mv /tmp/sysctl.conf /etc/sysctl.conf')

def save_limits():
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    limits = open('/etc/security/limits.conf', 'r')

    print("Backing up limits.conf as /etc/security/limits.conf.%s" % now)
    os.system('cp /etc/security/limits.conf /etc/security/limits.conf.%s' % now)
    limits_new = open('/tmp/limits.conf', 'w')
    for line in limits.readlines():
        line = line.strip()
        if ("root" in line or "*" in line) and ("soft" in line or "hard" in line) and ("nofile" in line or "nproc" in line) and not line.startswith('#'):
            continue
        else:
            line = line + '\n'
            limits_new.write(line)
    for line in suggested_limits.splitlines():
        limits_new.write(line)
        limits_new.write('\n')

    limits.close()
    limits_new.close()
    os.system('rm -f /etc/security/limits.conf')
    os.system('mv /tmp/limits.conf /etc/security/limits.conf')
    
def get_sysctl(param):
    r = os.popen("sysctl -a 2>&1 | grep " + str(param)).read()
    r = r.strip()
    return r if '=' not in r else r.split('=')[1]

def set_sysctl(param, value):
    return os.system('sysctl -w "%s=%s" 2>&1' % (str(param), str(value)))

def save():
    print("Saving sysctl configs...")
    save_sysctl()
    print("Saving sysctl configs...[finished]")

    print("Saving limits configs...")
    save_limits()
    print("Saving limits configs...[finished]")

def optimization():
    # 优化网络参数
    print("Optimizing basic networking params...")
    for k, v in suggested_sysctl_params_basic.items():
        set_sysctl(k, v)
    print("Optimizing basic networking params...[finished]")
    
    # 优化最大文件打开数
    print("\nOptimizing max open files...")
    if not os.system('ulimit -SHn 655350'):
        print("max open files: 655350")
        print("Optimizing max open files...[finished]")

    # 优化最大进程数
    print("\nOptimizing max user processes...")
    if not os.system('ulimit -SHu 655350'):
        print("max user processes: 655350")
        print("Optimizing max user processes...[finished]")


if __name__ == '__main__':
    print("******GTS-GOC os performance optimization script******")
    good_choice = False
    while(True):
        choice = raw_input("\n(1) show current configs (2) optimize current configs (3) optimize current configs and persist: ")
        if choice == '1':
            for k in suggested_sysctl_params_basic.keys():
                print(k, '=', get_sysctl(k))
            print("max open files: ", os.popen('ulimit -n').read().strip())
            print("max user processes: ", os.popen('ulimit -u').read().strip())
        elif choice == '2':
            optimization()
        elif choice == '3':
            optimization()
            save()
            break
            

    print("\n******GTS-GOC provides******\n")
