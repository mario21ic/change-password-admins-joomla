#!/usr/bin/env python

import ConfigParser
import pwd
import string
from random import choice
import os
import subprocess
from subprocess import PIPE,Popen
import csv
import ConfigParser
import simplejson


config = ConfigParser.ConfigParser()
config.read("config.ini")
uid_start = config.getint("settings", "uid_start")
uid_end = config.getint("settings", "uid_end")
pass_length = config.getint("settings", "pass_length")


def list_users():
    users = []
    for p in pwd.getpwall():
        if (p.pw_uid in range(uid_start, uid_end)) \
                and "/home/" in p.pw_dir:
            users.append(p.pw_name)
    return users

def generate_password(length):
    return ''.join(choice(string.letters + string.digits + '_-.$') for _ in range(length))

def read_configuration(directory):
    if os.path.isfile(directory + "/configuration.php"):
        php_process = Popen(["php", "access.php", directory], stdout=PIPE)
        values = simplejson.loads(php_process.communicate()[0])
        php_process.stdout.close()
        return values
    return False

def change_pass(user, password):
    pass

def write_csv(data):
    with open('report.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)


def main():
    data = []
    for user in list_users():
        configuration = read_configuration('/home/' + user + "/public_html/")
        #configuration = read_configuration(os.getcwd())
        if configuration:
            password = generate_password(pass_length)
            print configuration['db']
            print configuration['dbprefix']
            print configuration['user']
            print configuration['password']
            data.append([user, password])
            #if change_pass(user, password):
            #    data.append([user, password])
    write_csv(data)

if __name__ == "__main__":
    main()
