import os
import random

from lab.experiment import Experiment

FOMORO_API_KEY = os.environ.get('FOMORO_API_KEY')

def main():
    experiment = Experiment(FOMORO_API_KEY, '6CAc248f')
    for i in experiment.iter(range(10)):
        print('step', i)
    experiment.report(random.random(), random.random())

if __name__ == '__main__':
    main()
