"""
agentmemory — Embedding implementations.

Provides the Embedder Protocol and four implementations:
  - TFIDFEmbedder: zero-dependency sparse TF-IDF vectors (default)
  - DenseEmbedder: sentence-transformers dense embeddings
  - MultiModalEmbedder: CLIP (image) + Whisper (audio) + text
  - FunctionEmbedder: wrap any callable as an embedder

Also exports cosine_similarity() and the create_embedder() factory
which auto-selects between TF-IDF and dense based on availability.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Callable, Optional, Protocol, runtime_checkable


@runtime_checkable
class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...
    @property
    def dim(self) -> int: ...


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class DenseEmbedder:
    """Dense embedder with sentence-transformers, ONNX, or TF-IDF fallback."""

    def __init__(self, model_name: str = "all-mpnet-base-v2", device: str = "cpu"):
        self._model = None
        self._dim_val = 768
        self._fallback: Optional[TFIDFEmbedder] = None
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(model_name, device=device)
            self._dim_val = self._model.get_sentence_embedding_dimension()
            self._mode = "sentence_transformers"
        except ImportError:
            self._fallback = TFIDFEmbedder(dim=512)
            self._dim_val = 512
            self._mode = "tfidf_fallback"

    @property
    def dim(self) -> int:
        return self._dim_val

    @property
    def mode(self) -> str:
        return self._mode

    def embed(self, text: str) -> list[float]:
        if self._model is not None:
            return self._model.encode(text, normalize_embeddings=True).tolist()
        return self._fallback.embed(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if self._model is not None:
            return [e.tolist() for e in self._model.encode(texts, normalize_embeddings=True)]
        return [self.embed(t) for t in texts]


# ---- Upgrade 6: Multi-modal embedder ----

class MultiModalEmbedder:
    """
    Dispatches embedding by media_type: text, image, audio.
    Falls back to text embedder for all types when CLIP/Whisper unavailable.
    """

    def __init__(self, text_embedder: Optional[Embedder] = None):
        self._text_embedder = text_embedder or TFIDFEmbedder()
        self._clip_model = None
        self._clip_processor = None
        self._whisper_model = None
        self._mode = "text_only"
        self._try_load_clip()

    def _try_load_clip(self):
        try:
            from transformers import CLIPModel, CLIPProcessor
            self._clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self._clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self._mode = "multimodal"
        except ImportError:
            pass

    @property
    def dim(self) -> int:
        return self._text_embedder.dim

    @property
    def mode(self) -> str:
        return self._mode

    def embed(self, text: str, media_type: str = "text",
              raw_data: Optional[bytes] = None) -> list[float]:
        if media_type == "image" and self._clip_model and raw_data:
            return self._embed_image(raw_data)
        if media_type == "audio" and raw_data:
            text = self._transcribe_audio(raw_data)
        return self._text_embedder.embed(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self._text_embedder.embed_batch(texts)

    def _embed_image(self, image_bytes: bytes) -> list[float]:
        import io
        from PIL import Image
        import torch
        image = Image.open(io.BytesIO(image_bytes))
        inputs = self._clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            features = self._clip_model.get_image_features(**inputs)
        emb = features[0].numpy()
        norm = (emb ** 2).sum() ** 0.5
        if norm > 0:
            emb = emb / norm
        return emb.tolist()

    def _transcribe_audio(self, audio_bytes: bytes) -> str:
        try:
            import whisper
            import tempfile, os
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio_bytes)
                tmp = f.name
            if not self._whisper_model:
                self._whisper_model = whisper.load_model("base")
            result = self._whisper_model.transcribe(tmp)
            os.unlink(tmp)
            return result.get("text", "")
        except ImportError:
            return "[audio content - whisper not installed]"


# ---- TF-IDF (zero-dep fallback) ----

_STOP = frozenset(
    "a an the is was were be been being have has had do does did will would "
    "shall should may might can could of in to for on with at by from as into "
    "through during before after above below between out off over under again "
    "further then once here there when where why how all each every both few "
    "more most other some such no nor not only own same so than too very and "
    "but if or because until while it its i me my we our you your he him his "
    "she her they them their what which who whom this that these those am are".split())
_TOKENIZE_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

def _tokenize(text: str) -> list[str]:
    return [t for t in _TOKENIZE_RE.findall(text.lower()) if t not in _STOP and len(t) > 1]


class TFIDFEmbedder:
    def __init__(self, dim: int = 512):
        self._dim = dim
        self._vocab: dict[str, int] = {}
        self._doc_freq: Counter = Counter()
        self._n_docs: int = 0

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def mode(self) -> str:
        return "tfidf"

    def _token_index(self, token: str) -> int:
        if token not in self._vocab:
            h = int.from_bytes(token.encode()[:8].ljust(8, b'\0'), 'little')
            self._vocab[token] = h % self._dim
        return self._vocab[token]

    def _update_idf(self, tokens):
        self._n_docs += 1
        for t in set(tokens):
            self._doc_freq[t] += 1

    def _idf(self, token):
        df = self._doc_freq.get(token, 0)
        return math.log(1 + self._n_docs / df) if df else 1.0

    def embed(self, text: str) -> list[float]:
        tokens = _tokenize(text)
        if not tokens:
            return [0.0] * self._dim
        self._update_idf(tokens)
        tf = Counter(tokens)
        vec = [0.0] * self._dim
        for t, count in tf.items():
            vec[self._token_index(t)] += (1 + math.log(count)) * self._idf(t)
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(t) for t in texts]


class FunctionEmbedder:
    def __init__(self, fn: Callable, dim: int, batch_fn=None):
        self._fn = fn
        self._dim = dim
        self._batch_fn = batch_fn

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def mode(self) -> str:
        return "function"

    def embed(self, text: str) -> list[float]:
        return self._fn(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self._batch_fn(texts) if self._batch_fn else [self._fn(t) for t in texts]


def create_embedder(prefer_dense=True, model_name="all-mpnet-base-v2",
                    custom_fn=None, custom_dim=None, multimodal=False) -> Embedder:
    if custom_fn and custom_dim:
        return FunctionEmbedder(custom_fn, custom_dim)
    if multimodal:
        text_emb = DenseEmbedder(model_name) if prefer_dense else TFIDFEmbedder()
        return MultiModalEmbedder(text_embedder=text_emb)
    if prefer_dense:
        return DenseEmbedder(model_name=model_name)
    return TFIDFEmbedder()
