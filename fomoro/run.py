import os
import json
import pytz
import time
import datetime
import dateutil.parser
import requests
import subprocess

ENV = os.environ.get('ENV', 'production')

if ENV == 'production':
    API_URL = 'https://api.fomoro.com/projects/{}/runs'
else:
    API_URL = 'http://dev.api.fomoro.com/projects/{}/runs'
    # API_URL = 'http://localhost:3000/projects/{}/runs'

def get_git_log():
    format_str = '''
        {
            "commit_hash": "%H",
            "author_name": "%an",
            "author_email": "%ae",
            "author_date": "%aI",
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

    def reset(self):
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
        self.average_step_time = self.total_time / self.steps

    def iter(self, iterable, steps=None):
        self.begin()

        if steps is None:
            try:
                steps = len(iterable)
            except TypeError:
                steps = None
        self.steps = steps

        for obj in iterable:
            yield obj

        self.end()

    def report(self, loss, results=None):
        api_url = API_URL.format(self.project_key)

        author_date = self.git_log['author_date']
        author_date = dateutil.parser.parse(author_date) \
            .astimezone(tz=pytz.utc) \
            .replace(tzinfo=None) \
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

        r = requests.post(api_url, json=data, headers=headers)
        if r.status_code != 200:
            print(r.text)
