import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from muse.summarizer.summarizer import Summarizer

class mT5(Summarizer):
    def __init__(self, params):
        super().__init__(params)
        if(params['model_name'] == None):
            self.model_name = "csebuetnlp/mT5_multilingual_XLSum"
        else:
            self.model_name = params['model_name']
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

            
    def summarize(self, texts) -> list[str]:
        if isinstance(texts[0], list):
            return self._summary_multi(texts)
        return [self._summarize_single(texts[0])]

    def _summarize_single(self,text):
        WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
        input_ids = tokenizer(
            [WHITESPACE_HANDLER(article_text)],
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512
        )["input_ids"]

        output_ids = model.generate(
            input_ids=input_ids,
            max_length=84,
            no_repeat_ngram_size=2,
            num_beams=4
        )[0]

        summary = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )
        return summary
        

