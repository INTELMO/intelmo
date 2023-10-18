from intelmo import create_server, Compatible

from collections import Counter
from heapq import nlargest
from string import punctuation
from typing import List

import spacy
from spacy.lang.en.stop_words import STOP_WORDS


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
        )
    )
    server.run()
