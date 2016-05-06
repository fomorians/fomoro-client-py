import os
import time
import requests
import subprocess

ENV = os.environ.get('ENV', 'development')
API_KEY = os.environ.get('API_KEY')

if ENV == 'production':
    API_URL = 'https://api.fomoro.com/api/v0.1/experiments/{}/results'
else:
    API_URL = 'http://dev.api.fomoro.com/api/0.1/experiments/{}/results'

def get_git_describe():
    return subprocess.check_output(['git', 'describe', '--always', '--dirty', '--abbrev=0'], stderr=subprocess.STDOUT)

class Experiment(object):
    def __init__(self, api_key, experiment_id):
        self.api_key = api_key
        self.experiment_id = experiment_id

        try:
            self.hash = get_git_describe()
        except subprocess.CalledProcessError as e:
            print('Failed to retrieve current git commit hash.')
            print('Make sure you are running inside of git repo and committed.')

        self.reset()

    def reset(self):
        self.start_time = None
        self.end_time = None
        self.loss = None

    def begin(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def iter(self, iterable, total=None):
        self.begin()

        if total is None:
            try:
                total = len(iterable)
            except TypeError:
                total = None

        for obj in iterable:
            yield obj

        self.end()

    def report(self, loss, accuracy=None):
        api_url = API_URL.format(self.experiment_id)
        requests.post(api_url, json={
            "hash": self.hash,
            "loss": loss,
        })

def main():
    experiment = Experiment(API_KEY, 141)
    for i in experiment.iter(range(10)):
        print('step', i)
    experiment.report(1.24, accuracy=0.13)
    # experiment.reset()

if __name__ == '__main__':
    main()
