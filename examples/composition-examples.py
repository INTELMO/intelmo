from intelmo import create_server
from modification.spacyExample import SpaCySummarizer
from custom.customExample import SpaCyAnnotator
from generation.globalExample import analyse_sentiment
from generation.translationExample import translate_to_zh, custom_translate
from intelmo.models.composition import Exclusive, Compatible, Pipelined

if __name__ == "__main__":
    server = create_server(
        name="Example Server",
        description="An example server",
        tasks=Compatible(
            Pipelined(
                {
                    "name": "Summarize",
                    "description": "Summarize the text",
                    "task_type": "modification",
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
                    "name": "Sentiment",
                    "description": "Show the sentiment of the text",
                    "task_type": "generation",
                    "task": analyse_sentiment
                },
                {
                    "name": "Comment",
                    "description": "Leave your comments of this paragraph!",
                    "task_type": "custom",
                    "task": custom_translate
                },
            ),
            {
                "name": "Translate",
                "description": "Translate the text to Chinese",
                "task_type": "insertion",
                "task": translate_to_zh,
                "form": [
                    {
                        "name": "to_lang",
                        "type": "select",
                        "label": "To Language",
                        "defaultValue": "zh-CN",
                        "options": [
                            {
                                "label": "Chinese",
                                "value": "zh-CN"
                            },
                            {
                                "label": "Spanish",
                                "value": "es"
                            },
                            {
                                "label": "French",
                                "value": "fr"
                            },
                        ]
                    }
                ]
            },
            {
                "name": "Custom",
                "description": "Customized task",
                "task_type": "custom",
                "task": SpaCyAnnotator().annotate
            }
        )
    )
    server.run()
