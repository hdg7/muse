from collections import Counter
from heapq import nlargest
from string import punctuation

import spacy
import spacy.cli
from spacy.lang.en.stop_words import STOP_WORDS

from muse.summarizer.summarizer import Summarizer
from muse.utils.decorators import with_valid_options


class Spacy(Summarizer):
    @with_valid_options(
        language_spacy={
            "type": str,
            "default": "en_core_web_sm",
            "help": "The language model to use",
        },
    )
    def __init__(self, options: dict[str, any]):
        if options is None:
            options = {}

        ln = options.get("language_spacy", "en_core_web_sm")
        try:
            self.nlp = spacy.load(ln)
        except:
            spacy.cli.download(ln)
            self.nlp = spacy.load(ln)

    def summarize(self, texts) -> list[str]:
        if isinstance(texts, list):
            return self._summary_multi(texts)
        return [self._summarize_single(texts[0])]

    def _summarize_single(self, text):
        doc = self.nlp(str(text))
        keyword = []
        stopwords = list(STOP_WORDS)
        pos_tag = ["PROPN", "ADJ", "NOUN", "VERB"]
        for token in doc:
            if token.text in stopwords or token.text in punctuation:
                continue
            if token.pos_ in pos_tag:
                keyword.append(token.text)
        word_freq = Counter(keyword)
        for word in word_freq.keys():
            word_freq[word] = word_freq[word] / max(word_freq.values())
        sent_strength = {}
        for sent in doc.sents:
            for word in sent:
                if word.text in word_freq.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent] += word_freq[word.text]
                    else:
                        sent_strength[sent] = word_freq[word.text]
        summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
        final_sentences = [w.text for w in summarized_sentences]
        summary = " ".join(final_sentences)
        return summary

    def _summary_multi(self, texts):
        return [self._summarize_single(text) for text in texts]
