#! /usr/bin/env python3

import json


def read_credentials():
    with open('passwords.txt', 'r') as f:
        parsed_json = json.load(f)
        credentials = parsed_json['GOBI']
    return credentials["user"], credentials["password"]
