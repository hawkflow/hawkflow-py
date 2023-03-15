![HawkFLow.ai](https://hawkflow.ai/static/images/emails/bars.png)

# HawkFlow.ai

## Monitoring for anyone that writes code

1. Install the pip package `pip install hawkflow`
2. Usage:
```python
import time

from hawkflowclient.hawkflow_api import *

# authenticate with your API key
hf = HawkflowAPI("YOUR_API_KEY")

# start timing your code - pass through process (required) and meta (optional) parameters
print("sending timing start data to hawkflow")
hf.start("your_process_name", "your_meta_data")

# do some work
print("sleeping for 5 seconds...")
time.sleep(5)

# end timing this piece of code - process (required) and meta (optional) parameters should match the start
print("sending timing end data to hawkflow")
hf.end("your_process_name", "your_meta_data")
``` 


More examples: [HawkFlow.ai Python examples](https://github.com/hawkflow/hawkflow-examples/tree/master/python)

Read the docs: [HawkFlow.ai documentation](https://docs.hawkflow.ai/)

## What is HawkFlow.ai?

HawkFlow.ai is a new monitoring platform that makes it easier than ever to make monitoring part of your development process. Whether you are an Engineer, a Data Scientist, an Analyst, or anyone else that writes code, HawkFlow.ai helps you and your team take ownership of monitoring.