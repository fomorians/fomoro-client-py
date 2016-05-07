import os
import random

from lab.experiment import Experiment

API_KEY = os.environ.get('API_KEY')

def main():
    experiment = Experiment(API_KEY, 1)
    for i in experiment.iter(range(10)):
        print('step', i)
    experiment.report(random.random(), random.random())

if __name__ == '__main__':
    main()
