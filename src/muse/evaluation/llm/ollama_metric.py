import ollama
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

        self.key_fact_model = options.get("key_facts_model", "mistral-small")
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

    def get_key_facts(self, text: str) -> list[str]:
        prompt = f"From the following text, generate a list of keyfacts, in bullet points, each should only be around a single sentence, and concise. \n\n{text}"
        response = self._query_model(self.key_fact_model, prompt)["response"]
        return [
            x.strip().lstrip("•").lstrip("1234567890").strip()
            for x in response.split("\n")
            if x
        ]

    def get_key_fact_correspondence(self, f: list[str], g: list[str]) -> list[tuple]:
        # Combine by the threshold
        # If we have the following:
        # f = ["ae", "b", "c", "d", "e", "f"]
        # g = ["a", "d", "e", "z"]
        # and the threshold is 0.5
        # We would get the following:
        # a -> ae = 0.5
        # a -> b, a -> c, a -> d, a -> e, a -> f = 0
        # d -> ae, d -> b, d -> c, d -> e, d -> f = 0
        # d -> d = 1
        # e -> ae = 0.5
        # e -> b, e -> c, e -> d, e -> f = 0
        # e -> e = 1
        # z -> ae, z -> b, z -> c, z -> d, z -> e, z -> f = 0
        # So we take the f -> g of the max at the moment
        # So we would get the following:
        # [ ("ae", "a", sim("ae", "a"),
        #   ("b", None, None),
        #   ("c", None, None),
        #   ("d", "d", sim("d", "d")),
        #   ("e", "e", sim("e", "e")),
        #   ("f", None, None),
        #   (None, "z", None)
        # ]

        pairs = [(x, y, float(self.get_similarity(x, y))) for x in f for y in g]

        if self.similarity_pair_method == "max":
            for source_fact in f:
                max_sim = max([pair[2] for pair in pairs if pair[0] == source_fact])
                max_pair = [
                    pair
                    for pair in pairs
                    if pair[0] == source_fact and pair[2] == max_sim
                ][0]
                pairs = [pair for pair in pairs if pair[0] != source_fact]
                pairs.append(max_pair)
            pairs = [
                (
                    pair[0],
                    (
                        None
                        if pair[2] is not None and pair[2] < self.similarity_threshold
                        else pair[1]
                    ),
                    (
                        None
                        if pair[2] is not None and pair[2] < self.similarity_threshold
                        else pair[2]
                    ),
                )
                for pair in pairs
            ]
        else:
            raise ValueError("The similarity pair method is not valid")

        return pairs

    def get_similarity(self, f: str, g: str) -> float:
        embeddings = self.model.encode([f, g])
        return 1 - cosine(embeddings[0], embeddings[1])

    @staticmethod
    def _query_model(model, text: str):
        response = ollama.generate(model, text)
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
