#! python3

from __future__ import print_function

import os
import sys
import subprocess
import re
import time

ENV_NAME_DOMAIN = 'DOMAIN'
ENV_NAME_EMAIL = 'EMAIL'

WAIT_DNS_UP = 1


def main():
    certbot_args = [
        'certbot',
        'certonly',
        '--preferred-challenge',
        'dns',
        '--manual',
        '--agree-tos',
    ] + sys.argv[1:] # extra args

    domain = os.environ.get(ENV_NAME_DOMAIN)
    if domain:
        certbot_args.append('--domain')
        certbot_args.append(domain)
    else:
        print('environment variable [{name}] is not defined'.format(name=ENV_NAME_DOMAIN))
        print('exit now')
        exit(1)

    email = os.environ.get(ENV_NAME_EMAIL)
    if email:
        certbot_args.append('--email')
        certbot_args.append(email)
    else:
        print('environment variable [{name}] is not defined'.format(name=ENV_NAME_DOMAIN))
        print('use argument "--register-unsafely-without-email"')
        certbot_args.append('--register-unsafely-without-email')

    print('running certbot with args')
    print(certbot_args)
    print('-----')

    process = subprocess.Popen(
        certbot_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    record_names = set()

    while process.poll() is None: # while subprocess still running
        line = readline_and_print(process.stdout)
        stripped_line = line.strip()
        
        if stripped_line == 'Are you OK with your IP being logged?':
            process.stdin.write('Y\n'.encode())
            process.stdin.flush()

        if stripped_line == 'Please deploy a DNS TXT record under the name':
            name_line = readline_and_print(process.stdout)
            readline_and_print(process.stdout)
            record_data = readline_and_print(process.stdout).strip()

            name = get_name_from_line(name_line)
            record_names.add(name)

            dns_up_args = [
                './dns-up.sh',
                name,
                record_data
            ]
            print('starting running dns up script with', dns_up_args)
            dns_up_process = subprocess.Popen(dns_up_args)

            dns_up_return_code = dns_up_process.wait()
            if dns_up_return_code != 0:
                print_remaining_stdout(process)
                
                print('return code != 0')
                print('exit now')
                exit(1)
            
            time.sleep(WAIT_DNS_UP)

            process.stdin.write('\n'.encode())
            process.stdin.flush()
        
        if stripped_line == '1: Keep the existing certificate for now':
            process.stdin.write('1\n'.encode())
            process.stdin.flush()
            process.terminate()

            print_remaining_stdout(process)

            exit()

    for name in record_names:
        dns_down_args = [
            './dns-down.sh',
            name
        ]
        dns_down_process = subprocess.Popen(dns_down_args)
        dns_down_process.wait()


def readline_and_print(stream):
    line = stream.readline()
    if isinstance(line, bytes):
        line = line.decode()
    print(line, end='')
    return line


def get_name_from_line(line):
    if isinstance(line, bytes):
        line = line.decode()
    return re.search(r'^(.*) with the following value', line.strip()).group(1)


def print_remaining_stdout(process):
    while process.poll() is None:
        line = process.stdout.readline()
        print(line, end='')


if __name__ == "__main__":
    main()
