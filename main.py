import os
import random

from fomoro.run import Run

FOMORO_API_KEY = os.environ.get('FOMORO_API_KEY')

def main():
    run = Run('6CAc248f', FOMORO_API_KEY)
    for i in run.iter(range(10)):
        print('step', i)
    run.report(random.random(), random.random())

if __name__ == '__main__':
    main()
