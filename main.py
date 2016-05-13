import os
import random

# import a Fomoro `Run` which represents a training run
from fomoro.run import Run

# read api key from an environment variable
# (more secure than saving it in the file and version control)
FOMORO_API_KEY = os.environ.get('FOMORO_API_KEY')

# create a new `Run` instance, setting appropriate arguments:
# - project_key (required): your project key
# - api_key (required): your api key
# - hyperparams (optional): dictionary of hyperparameters you want to log with the results
# - metadata (optional): dictionary of additional metadata like number of model parameters
run = Run(project_key='rJbwGJNf', api_key=FOMORO_API_KEY, hyperparams={
    "batch_size": 1
}, metadata={
    "num_parameters": 1e6
})

# optionally track the number of iterations for progress reporting and step time tracking
for i in run.iter(range(10)):
    print('step', i)

# finally, report the results:
# - loss (required): model loss
# - results (optional): dictionary of additional results like accuracy, AUC, etc.
run.report(loss=random.random(), results={
    "accuracy": random.random()
})
