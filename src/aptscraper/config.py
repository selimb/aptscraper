import json
from jsonschema import validate
import os
import sys


CONFIG_FNAME = 'conf.json'
number_fields = ['min_price', 'max_price']
string_fields = ['fromaddr', 'toaddr', 'passwd']
hood = {
    'type': 'object',
    'properties': {
        'label': {'type': 'string'},
        'polygon': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': [
                    {'type': 'number'},
                    {'type': 'number'},
                ],
            },
        },
    },
}
properties = {
    'hoods': {
        'type': 'array',
        'items': hood,
    },
    'laundry': {
        'type': 'boolean',
    },
    'dry_run': {
        'type': 'boolean',
    },
}
required = number_fields + string_fields + ['hoods', 'laundry']
for field in number_fields:
    properties[field] = {'type': ['number', 'null']}
for field in string_fields:
    properties[field] = {'type': ['string']}

SCHEMA = {
    'type': 'object',
    'properties': properties,
    'required': required
}


def load_conf(d):
    fpath = os.path.join(d, CONFIG_FNAME)
    if not os.path.exists(fpath):
        print('No config found at ' + fpath)
        sys.exit(1)
    with open(fpath) as f:
        conf = json.load(f)

    validate(conf, SCHEMA)
    return conf
