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
				# any function that takes article text and returns a string
                "task": ...
			}
		],
    )

	server.run()
```

Then you can start the server with:

```bash
python example.py
```

A development server will be started at `http://localhost:5000`.
