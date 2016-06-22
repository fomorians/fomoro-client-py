import os
import random

# import a Fomoro `Results` which represents the results from a training run
from fomoro.results import Results

# read api key from an environment variable
# (more secure than saving it in the file and version control)
FOMORO_API_KEY = os.environ.get('FOMORO_API_KEY')
PROJECT_KEY = 'rki7KxaQ'

print("\"{}\"".format(FOMORO_API_KEY))

# create a new `Results` instance, setting appropriate arguments:
# - project_key (required): your project key
# - api_key (required): your api key
# - hyperparams (optional): dictionary of hyperparameters you want to log with the results
# - metadata (optional): dictionary of additional metadata like number of model parameters
results = Results(project_key=PROJECT_KEY, api_key=FOMORO_API_KEY, hyperparams={
    "batch_size": 1
}, metadata={
    "num_parameters": 1e6
})

# optionally track the number of iterations for progress reporting and step time tracking
for i in results.iter(range(10)):
    print('step', i)

# finally, report the results:
# - loss (required): model loss
# - results (optional): dictionary of additional results like accuracy, AUC, etc.
results.report(loss=random.random(), results={
    "accuracy": random.random()
})
