import os
import json
import random

from fomoro import Fomoro

FOMORO_ARTIFACTS = os.environ.get('FOMORO_ARTIFACTS', None)

# read api key from an environment variable
# (more secure than saving it in the file and version control)
FOMORO_API_KEY = os.environ.get('FOMORO_API_KEY')
PROJECT_KEY = 'rki7KxaQ'

# create a new `Results` instance, setting appropriate arguments:
# - project_key (required): your project key
# - api_key (required): your api key
# - hyperparams (optional): dictionary of hyperparameters you want to log with the results
# - metadata (optional): dictionary of additional metadata like number of model parameters
client = Fomoro(project_key=PROJECT_KEY, api_key=FOMORO_API_KEY, hyperparams={
    "batch_size": 1
}, metadata={
    "num_parameters": 1e6
})

# optionally track the number of iterations for progress reporting and step time tracking
for i in client.iter(range(10)):
    print('step', i)

# finally, report the results:
# - loss (required): model loss
# - results (optional): dictionary of additional results like accuracy, AUC, etc.
loss = random.random()
results = {
    "accuracy": random.random()
}
client.report(loss=loss, results=results)

if FOMORO_ARTIFACTS:
    print('Writing artifacts...')
    with open(os.path.join(FOMORO_ARTIFACTS, 'results.json'), 'w') as f:
        f.write(json.dumps(results))
