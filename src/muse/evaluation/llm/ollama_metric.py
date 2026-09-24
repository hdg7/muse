import ollama
import numpy as np
import re
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

from muse.evaluation.evaluation import Evaluation
from muse.utils.decorators import with_valid_options

similarity_languages = {
    "sentence-transformers/distiluse-base-multilingual-cased-v1": [
        "Arabic",
        "Chinese",
        "Dutch",
        "English",
        "French",
        "German",
        "Italian",
        "Korean",
        "Polish",
        "Portuguese",
        "Russian",
        "Spanish",
        "Turkish",
    ]
}


class OllamaMetric(Evaluation):
    """
    Class to evaluate the OLLAMA metric
    """

    @with_valid_options(
        key_facts_model={
            "type": str,
            "default": "mistral-small",
            "help": "The model to use for key facts",
        },
        similarity_model={
            "type": str,
            "default": "sentence-transformers/distiluse-base-multilingual-cased-v1",
            "help": "The model to use for similarity",
        },
        reference_free={
            "type": bool,
            "default": True,
            "help": "Whether to use reference text for key facts",
        },
        similarity_threshold={
            "type": float,
            "default": 0.5,
            "help": "The similarity threshold",
        },
        similarity_pair_method={
            "type": str,
            "default": "max",
            "help": "The similarity pair method",
        },
        language_source={"type": str, "default": "en", "help": "The source language"},
        language_target={"type": str, "default": "en", "help": "The target language"},
    )
    def __init__(self, options):
        if not options:
            options = {}

        self.score_method = np.mean

        self.key_fact_model = options.get("key_facts_model", "tinyllama")
        self.similarity_model = options.get(
            "similarity_model",
            "sentence-transformers/distiluse-base-multilingual-cased-v1",
        )

        self.reference_free = options.get("reference_free", True)
        self.similarity_threshold = options.get("similarity_threshold", 0.5)

        self.similarity_pair_method = options.get("similarity_pair_method", "max")

        self.language_source = options.get("language_source", "en")
        self.language_target = options.get("language_target", "en")

        if self.similarity_model in similarity_languages.keys():
            if not any(
                [
                    x.lower().startswith(self.language_source.lower())
                    for x in similarity_languages[self.similarity_model]
                ]
            ):
                old_model = self.similarity_model
                self.similarity_model = (
                    "sentence-transformers/distiluse-base-multilingual-cased-v2"
                )
                print(
                    f"Warning: The language {self.language_source} is not supported by the model {old_model}. Switching to {self.similarity_model}"
                )
            if not any(
                [
                    x.lower().startswith(self.language_target.lower())
                    for x in similarity_languages[self.similarity_model]
                ]
            ):
                old_model = self.similarity_model
                self.similarity_model = (
                    "sentence-transformers/distiluse-base-multilingual-cased-v2"
                )
                print(
                    f"Warning: The language {self.language_target} is not supported by the model {old_model}. Switching to {self.similarity_model}"
                )

        self.model = SentenceTransformer(self.similarity_model)

        self._pull_models([self.key_fact_model])

    def evaluate(
        self, summary, reference_text=None, reference_summary=None
    ) -> dict[str, any]:
        """
        Method to evaluate the summary

        :param summary: The summary to be evaluated
        :param reference_text: The reference text is not used in ROUGE evaluation
        :param reference_summary: The reference summary to compare the summary to (optional)
        :return: The evaluation results
        """

        if not summary:
            raise ValueError("The summary should not be empty")

        if isinstance(summary, str):
            summary = [summary]
        if reference_text and isinstance(reference_text, str):
            reference_text = [reference_text]
        if reference_summary and isinstance(reference_summary, str):
            reference_summary = [reference_summary]

        if summary and (
            (reference_summary and len(summary) != len(reference_summary))
            or (reference_text and len(summary) != len(reference_text))
        ):
            raise ValueError(
                "The number of summaries and reference summaries should be the same"
            )

        return {
            "ollama": self._evaluate_multi(summary, reference_text, reference_summary)
        }

    def _evaluate_single(self, summary, reference_text, reference_summary):
        summary = str(summary)
        reference_text = str(reference_text) if reference_text else None
        reference_summary = str(reference_summary) if reference_summary else None

        if self.reference_free:
            reference_key_facts = self.get_key_facts(reference_text)
        else:
            reference_key_facts = self.get_key_facts(reference_summary)

        summary_key_facts = self.get_key_facts(summary)

        key_fact_correspondence = self.get_key_fact_correspondence(
            reference_key_facts, summary_key_facts
        )

        factuality = self.calculate_factuality(key_fact_correspondence)
        completeness = self.calculate_completeness(key_fact_correspondence)
        density = self.calculate_density(key_fact_correspondence)

        return {
            "score": self.score_method([float(factuality), float(completeness), float(density)]),
            "factuality": float(factuality),
            "completeness": float(completeness),
            "density": float(density),
            "key_fact_correspondence": key_fact_correspondence,
            "reference_key_facts": reference_key_facts,
            "summary_key_facts": summary_key_facts,
        }

    def _evaluate_multi(self, summary, reference_text, reference_summary):
        return [
            self._evaluate_single(
                summary[i],
                reference_text=None if not reference_text else reference_text[i],
                reference_summary=(
                    None if not reference_summary else reference_summary[i]
                ),
            )
            for i in range(len(summary))
        ]

    def get_key_facts(self, text: str) -> list:
        if text is None or not str(text).strip():
            return []

        prompt = (
            "Extract the key factual information from the following text.\n"
            "Return one concise fact per line.\n"
            "Do not use bullets, numbering, headings, XML tags, explanations, "
            "or additional commentary.\n"
            "Write the facts in the same language as the input text.\n\n"
            f"{text}"
        )

        model_response = self._query_model(self.key_fact_model, prompt)

        if isinstance(model_response, dict):
            response = model_response.get("response", "")
        else:
            response = getattr(model_response, "response", "")

        if not response or not str(response).strip():
            return []

        response = str(response)

        # Remove DeepSeek-style reasoning blocks.
        response = re.sub(
            r"<think>.*?</think>",
            "",
            response,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove other paired XML-like blocks.
        response = re.sub(
            r"<(\w+)>.*?</\1>",
            "",
            response,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove common Markdown list prefixes.
        response = re.sub(
            r"^\s*(?:[-*•]|\d+[\.)])\s*",
            "",
            response,
            flags=re.MULTILINE,
        )

        facts = []

        for line in response.splitlines():
            fact = line.strip()

            if not fact:
                continue

            # Remove a possible introductory heading.
            if not facts and ":" in fact:
                prefix, content = fact.split(":", 1)

                common_headings = {
                    "key facts",
                    "facts",
                    "key factual information",
                    "الحقائق الرئيسية",
                    "الحقائق",
                    "المعلومات الرئيسية",
                }

                if prefix.strip().lower() in common_headings:
                    fact = content.strip()

            if fact:
                facts.append(fact)

        return facts


    def get_key_fact_correspondence(
            self,
            f: list[str],
            g: list[str],
    ) -> list:
        source_facts = [
            str(fact).strip()
            for fact in (f or [])
            if fact is not None and str(fact).strip()
        ]

        target_facts = [
            str(fact).strip()
            for fact in (g or [])
            if fact is not None and str(fact).strip()
        ]

        # No reference facts means there is nothing to compare.
        if not source_facts:
            return []

        # Reference facts exist, but the evaluated summary yielded no facts.
        # Record every reference fact as unmatched.
        if not target_facts:
            return [
                (source_fact, None, None)
                for source_fact in source_facts
            ]

        if self.similarity_pair_method != "max":
            raise ValueError(
                f"Invalid similarity pair method: "
                f"{self.similarity_pair_method!r}"
            )

        correspondence = []

        for source_fact in source_facts:
            candidates = []

            for target_fact in target_facts:
                similarity = float(
                    self.get_similarity(source_fact, target_fact)
                )

                # Prevent NaN values from interfering with max().
                if np.isfinite(similarity):
                    candidates.append(
                        (source_fact, target_fact, similarity)
                    )

            if not candidates:
                correspondence.append(
                    (source_fact, None, None)
                )
                continue

            best_pair = max(
                candidates,
                key=lambda pair: pair[2],
            )

            if best_pair[2] < self.similarity_threshold:
                correspondence.append(
                    (source_fact, None, None)
                )
            else:
                correspondence.append(best_pair)

        return correspondence



    def get_similarity(self, f: str, g: str) -> float:
        embeddings = self.model.encode([f, g])
        return 1 - cosine(embeddings[0], embeddings[1])

    @staticmethod
    def _query_model(model, text: str):
        response = ollama.generate(
            model=model,
            prompt=text,
            think=False,
            stream=False,
            options={
                "temperature": 0.2,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.35,
                "repeat_last_n": 128,
                "num_predict": 512,
            },
        )
        return response

    @staticmethod
    def _pull_models(models):

        for model in models:
            ollama.pull(model)

    @staticmethod
    def calculate_factuality(p: list[tuple]) -> float:
        p = [pair[2] for pair in p if pair[2] is not None]
        if len(p) == 0:
            return 0
        return sum([x for x in p]) / len(p)

    @staticmethod
    def calculate_completeness(p: list[tuple]) -> float:
        p = [pair[2] for pair in p]
        if len(p) == 0:
            return 0
        return len([x for x in p if x is not None]) / len(p)

    @staticmethod
    def calculate_comprehension(p: list[tuple]) -> float:
        pass

    def calculate_density(self, p: list[tuple]) -> float:
        return (0.5 * self.calculate_completeness(p)) + (
            0.5 * self.calculate_factuality(p)
        )

    @staticmethod
    def calculate_coherence(source: str):
        pass
