from generation.translationExample import custom_translate
from highlight.spacyExample import SpaCySummarizer
from intelmo import create_server

if __name__ == "__main__":
    server = create_server(
        name="Example Server",
        description="An example server",
        composition="pipeline",
        tasks=[
            {
                "name": "Summarize",
                "description": "Summarize the text",
                "task_type": "highlight",
                "task": SpaCySummarizer().summarize_count,
                "form": [
                    {
                        "name": "count",
                        "type": "number",
                        "label": "Sentences Count",
                        "defaultValue": 7,
                        "min": 1,
                        "max": 10,
                        "step": 1,
                    }
                ]
            },
            {
                "name": "Translate",
                "description": "Translate the text to Chinese",
                "task_type": "custom",
                "task": custom_translate
            },

        ]
    )
    server.run()
