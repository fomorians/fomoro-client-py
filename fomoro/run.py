from __future__ import division

import os
import json
import pytz
import time
import datetime
import requests
import subprocess

from tzlocal import get_localzone

FOMORO_ENV = os.environ.get('FOMORO_ENV', 'production')
FOMORO_RUN_ID = os.environ.get('FOMORO_RUN_ID', None)

if FOMORO_ENV == 'production':
    API_HOST = 'https://api.fomoro.com' 
elif FOMORO_ENV == 'staging':
    API_HOST = 'http://dev.api.fomoro.com'
else:
    API_HOST = 'http://localhost:3000'

def get_git_log():
    format_str = '''
        {
            "commit_hash": "%H",
            "author_name": "%an",
            "author_email": "%ae",
            "author_date": "%at",
            "subject": "%s",
            "body": "%b"
        }
        '''

    # flatten json format
    format_str = json.loads(format_str)
    format_str = json.dumps(format_str)

    output = subprocess.check_output("git log --max-count=1 --format='{}'".format(format_str), \
        shell=True, \
        stderr=subprocess.STDOUT)

    output = json.loads(output)
    return output

def get_git_branch():
    branch = subprocess.check_output([ 'git', 'rev-parse', '--abbrev-ref', 'HEAD' ], stderr=subprocess.STDOUT)
    branch = branch.strip()
    return branch

def get_git_dirty():
    try:
        subprocess.check_output([ 'git', 'diff', '--quiet', 'HEAD' ], stderr=subprocess.STDOUT)
        return False
    except subprocess.CalledProcessError as e:
        return True

class Run(object):
    def __init__(self, project_key, api_key, hyperparams=None, metadata=None):
        self.project_key = project_key
        self.api_key = api_key
        self.hyperparams = hyperparams
        self.metadata = metadata

        try:
            self.git_log = get_git_log()
            self.dirty = get_git_dirty()
            self.branch = get_git_branch()

            if self.dirty:
                print('WARNING: You have uncommitted changes. (fomoro)')

        except subprocess.CalledProcessError as e:
            print('Failed to retrieve git information.')
            print('Make sure you are running inside of a git repo and committed.')

        self.reset()
        self.begin()

    def reset(self):
        self.steps = 1
        self.start_time = None
        self.end_time = None
        self.total_time = None
        self.average_step_time = None
        self.loss = None

    def begin(self):
        self.start_time = datetime.datetime.utcnow()

    def end(self):
        self.end_time = datetime.datetime.utcnow()
        self.total_time = self.end_time - self.start_time
        self.average_step_time = self.total_time // self.steps

    def iter(self, iterable, steps=None):
        if steps is None:
            try:
                steps = len(iterable)
            except TypeError:
                steps = None
        self.steps = steps

        for obj in iterable:
            yield obj

    def report(self, loss, results=None):
        self.end()

        tz = get_localzone()

        author_date = float(self.git_log['author_date'])
        author_date = datetime.datetime.fromtimestamp(author_date, tz) \
            .astimezone(tz=pytz.utc) \
            .isoformat()

        data = {
            "commit_hash": self.git_log['commit_hash'],
            "commit_subject": self.git_log['subject'],
            "commit_body": self.git_log['body'],
            "author_name": self.git_log['author_name'],
            "author_email": self.git_log['author_email'],
            "author_date": author_date,
            "training_start_time": self.start_time.isoformat(),
            "training_end_time": self.end_time.isoformat(),
            "training_total_time": self.total_time.total_seconds(),
            "training_average_step_time": self.average_step_time.total_seconds(),
            "training_steps": self.steps,
            "dirty": self.dirty,
            "branch": self.branch,
            "loss": loss,
            "hyperparams": json.dumps(self.hyperparams),
            "metadata": json.dumps(self.metadata),
            "results": json.dumps(results),
        }

        headers = {
            'Authorization': 'Bearer {}'.format(self.api_key)
        }

        if FOMORO_RUN_ID:
            api_url = API_HOST + '/projects/{}/runs/{}'.format(self.project_key, FOMORO_RUN_ID)
            r = requests.put(api_url, json=data, headers=headers)
        else:
            api_url = API_HOST + '/projects/{}/runs'.format(self.project_key)
            r = requests.post(api_url, json=data, headers=headers)

        if r.status_code != 200:
            print(r.text)
