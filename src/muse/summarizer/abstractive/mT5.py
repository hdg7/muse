import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from muse.summarizer.summarizer import Summarizer


class MT5(Summarizer):
    def __init__(self, params):
        super().__init__(params)
        if params is None:
            params = {}

        self.model_name = params.get("model_name", "csebuetnlp/mT5_multilingual_XLSum")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.device = params.get(
            "device", "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model.to(self.device)

    def summarize(self, texts) -> list[str]:
        if isinstance(texts, list):
            return self._summary_multi(texts)
        return [self._summarize_single(texts[0])]

    def _summarize_single(self, text):
        WHITESPACE_HANDLER = lambda k: re.sub("\s+", " ", re.sub("\n+", " ", k.strip()))
        input_ids = self.tokenizer(
            [WHITESPACE_HANDLER(text.text)],
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512,
        )["input_ids"].to(self.device)

        output_ids = self.model.generate(
            input_ids=input_ids, max_length=84, no_repeat_ngram_size=2, num_beams=4
        )[0]

        summary = self.tokenizer.decode(
            output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        return summary

    def _summary_multi(self, texts):
        return [self._summarize_single(text) for text in texts]
