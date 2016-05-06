import os

from lab.experiment import Experiment

API_KEY = os.environ.get('API_KEY')

def main():
    experiment = Experiment(API_KEY, 141)
    for i in experiment.iter(range(10)):
        print('step', i)
    experiment.report(1.24, accuracy=0.13)
    # experiment.reset()

if __name__ == '__main__':
    main()
