# Quick Start with INTELMO

## Installation

INTELMO is available on PyPI and can be installed with pip:

```bash
pip install intelmo
```

## Basic Configuration

You can use `intelmo.create_server()` to create a server.

```python
# example.py
from intelmo import create_server

if __name__ == "__main__":
    server = create_server(
		name="Example Server",
		description="This is an example server.",
		tasks=[
			{
				"name": "Sentiment",
                "description": "Show the sentiment of the text",
                "task_type": "generation",
                "task": analyse_sentiment  # a function that takes article text and returns a string
			}
		],
    )

	server.run()
```

Then you can start the server with:

```bash
python example.py
```
