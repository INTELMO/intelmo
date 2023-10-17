from spacy.lang.en.stop_words import STOP_WORDS
import spacy
from typing import List
from string import punctuation
from heapq import nlargest
from collections import Counter
from typing import Union
from nicegui import ui
from ui import rss_page, reader_page
from models.task import InteractiveTaskConfiguration, TaskModelConfiguration, Composition, Compatible


class Server:
    def __init__(self, configuration: TaskModelConfiguration):
        self.configuration = configuration

    def create_routes(self):
        @ui.page('/')
        def rss_page_index():
            return rss_page.content()

        @ui.page('/{rss_source_id}')
        def rss_page_feed(rss_source_id: str):
            return rss_page.detail_content(rss_source_id)

        @ui.page('/reader/article')
        def reader_article(url: str):
            functions = self.configuration.task_tree.get_leaves()
            return reader_page.content(url, functions, self.configuration)

    def run(self):
        self.create_routes()
        ui.run(
            title=self.configuration.name if self.configuration.name else "INTELMO",
        )


def create_server(name: str, description: str,
                  tasks: Union[InteractiveTaskConfiguration, Composition]):
    return Server(TaskModelConfiguration(name, description, tasks))

###
# Example below
###


# Note: a class is not required by packages, but it is recommended to use one for better organization
class SpaCySummarizer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.stopwords = list(STOP_WORDS)

    # classical summarization algorithm using spacy
    def summarize_count(self, text: str, config: dict) -> List[str]:
        if "count" not in config:
            count = 7
        else:
            count = int(config["count"])

        keywords = []
        doc = self.nlp(text)
        for token in doc:
            if token.text in self.stopwords or token.text in punctuation:
                continue
            if token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ']:
                keywords.append(token.text)
        freq_word = Counter(keywords)
        max_freq = Counter(keywords).most_common(1)[0][1]
        for word in keywords:
            freq_word[word] = freq_word[word] / max_freq

        sent_strength = {}
        for sent in doc.sents:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent] += freq_word[word.text]
                    else:
                        sent_strength[sent] = freq_word[word.text]

        summarized_sentences = nlargest(
            count, sent_strength, key=sent_strength.get)
        final_sentences = [w.text for w in summarized_sentences]
        return final_sentences

    def summarize(self, text: str) -> List[str]:
        return self.summarize_count(text, {
            "count": 7
        })


if __name__ in {"__main__", "__mp_main__"}:
    server = create_server(
        name='INTELMO New UI',
        description='INTELMO New UI',
        tasks=Compatible(
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
                "name": "Summarize2",
                "description": "Summarize the text",
                "task_type": "modification",
                "task": SpaCySummarizer().summarize,


            }
        )
    )
    server.run()
