"""
agentmemory V3 — Approximate Nearest Neighbor Index.

Pure-Python HNSW implementation. O(log n) queries.
Thread-safe for concurrent agent access.
For >500k memories, swap in hnswlib via HNSWLibIndex.
"""

from __future__ import annotations

import hashlib
import heapq
import math
import random
import struct
import threading
from typing import Optional

from .embeddings import cosine_similarity


def _distance(a: list[float], b: list[float]) -> float:
    return 1.0 - cosine_similarity(a, b)


class HNSWIndex:
    """Thread-safe pure-Python HNSW index."""

    def __init__(self, M: int = 16, ef_construction: int = 100,
                 ef_search: int = 50):
        self.M = M
        self.M0 = M * 2
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.ml = 1.0 / math.log(M) if M > 1 else 1.0
        self._lock = threading.Lock()
        self._vectors: dict[str, list[float]] = {}
        self._layers: list[dict[str, set[str]]] = []
        self._node_level: dict[str, int] = {}
        self._entry_point: Optional[str] = None
        self._max_level: int = -1
        self._rng = random.Random(42)

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._vectors)

    def add(self, key: str, vector: list[float]):
        with self._lock:
            self._add(key, vector)

    def remove(self, key: str):
        with self._lock:
            self._remove(key)

    def query(self, vector: list[float], k: int = 10) -> list[tuple[str, float]]:
        with self._lock:
            return self._query(vector, k)

    def query_radius(self, vector: list[float], radius: float,
                     max_results: int = 100) -> list[tuple[str, float]]:
        with self._lock:
            if not self._vectors or self._entry_point is None:
                return []
            ep = self._entry_point
            for lv in range(self._max_level, 0, -1):
                ep = self._greedy(vector, ep, lv)
            cands = self._beam(vector, ep,
                               max(self.ef_search, max_results), 0)
            results = [(c, _distance(vector, self._vectors[c]))
                       for c in cands]
            results = [(k_, d) for k_, d in results if d <= radius]
            results.sort(key=lambda x: x[1])
            return results[:max_results]

    def contains(self, key: str) -> bool:
        with self._lock:
            return key in self._vectors

    def get_all_keys(self) -> list[str]:
        with self._lock:
            return list(self._vectors.keys())

    # ---- internals ----

    @staticmethod
    def _vector_random(vector: list[float]) -> float:
        """Return a deterministic pseudo-random float derived from the vector.

        Uses SHA-256 of the first 16 float values (packed as bytes) so that:
          - The same embedding always maps to the same HNSW level.
          - The result is independent of Python's PYTHONHASHSEED.
          - The result is independent of the node's UUID key.

        This eliminates insertion-order non-determinism: node levels are fixed
        by content (embedding), not by the order in which add() is called.
        """
        n = min(16, len(vector))
        data = struct.pack(f"{n}f", *vector[:n])
        digest = hashlib.sha256(data).digest()
        # Interpret first 8 bytes as a big-endian uint64 and normalise to (0, 1)
        h = int.from_bytes(digest[:8], "big") or 1  # avoid zero
        return h / 0x1_0000_0000_0000_0000

    def _add(self, key: str, vector: list[float]):
        if key in self._vectors:
            self._remove(key)
        self._vectors[key] = vector
        level = int(-math.log(self._vector_random(vector) + 1e-9) * self.ml)
        self._node_level[key] = level
        while len(self._layers) <= level:
            self._layers.append({})
        for lv in range(level + 1):
            self._layers[lv][key] = set()

        if self._entry_point is None:
            self._entry_point = key
            self._max_level = level
            return

        ep = self._entry_point
        for lv in range(self._max_level, level, -1):
            ep = self._greedy(vector, ep, lv)
        for lv in range(min(level, self._max_level), -1, -1):
            mx = self.M0 if lv == 0 else self.M
            cands = self._beam(vector, ep, self.ef_construction, lv)
            nbs = self._select(vector, cands, mx)
            self._layers[lv][key] = set(nbs)
            for nb in nbs:
                s = self._layers[lv].setdefault(nb, set())
                s.add(key)
                if len(s) > mx:
                    self._layers[lv][nb] = set(
                        self._select(self._vectors[nb], list(s), mx))
            if cands:
                ep = min(cands,
                         key=lambda k_: _distance(vector, self._vectors[k_]))
        if level > self._max_level:
            self._entry_point = key
            self._max_level = level

    def _remove(self, key: str):
        if key not in self._vectors:
            return
        level = self._node_level.get(key, 0)
        for lv in range(level + 1):
            if lv < len(self._layers) and key in self._layers[lv]:
                nbs = self._layers[lv].pop(key)
                for nb in nbs:
                    if nb in self._layers[lv]:
                        self._layers[lv][nb].discard(key)
        del self._vectors[key]
        del self._node_level[key]
        if self._entry_point == key:
            if self._vectors:
                self._entry_point = next(iter(self._vectors))
                self._max_level = self._node_level.get(
                    self._entry_point, 0)
            else:
                self._entry_point = None
                self._max_level = -1

    def _query(self, vector: list[float], k: int) -> list[tuple[str, float]]:
        if not self._vectors or self._entry_point is None:
            return []
        ep = self._entry_point
        for lv in range(self._max_level, 0, -1):
            ep = self._greedy(vector, ep, lv)
        cands = self._beam(vector, ep, max(self.ef_search, k), 0)
        results = [(c, _distance(vector, self._vectors[c])) for c in cands]
        results.sort(key=lambda x: x[1])
        return results[:k]

    def _greedy(self, q: list[float], ep: str, lv: int) -> str:
        if lv >= len(self._layers) or ep not in self._layers[lv]:
            return ep
        best, best_d = ep, _distance(q, self._vectors[ep])
        improved = True
        while improved:
            improved = False
            for nb in self._layers[lv].get(best, set()):
                if nb not in self._vectors:
                    continue
                d = _distance(q, self._vectors[nb])
                if d < best_d:
                    best, best_d = nb, d
                    improved = True
        return best

    def _beam(self, q: list[float], ep: str, ef: int,
              lv: int) -> list[str]:
        # Beam search within a single HNSW graph layer (Algorithm 2 from
        # Malkov & Yashunin 2018, "Efficient and Robust ANN Search With HNSW").
        #
        # Maintains two heaps:
        #   cands: min-heap of (distance, node_id) — candidates to expand next
        #   res:   max-heap of (-distance, node_id) — best `ef` results so far
        #            (negated because Python's heapq is a min-heap)
        #
        # The stopping condition (cd > -res[0][0]) terminates search when the
        # nearest unvisited candidate is farther than the worst result in the
        # current top-ef set — i.e., expanding further cannot improve results.
        if lv >= len(self._layers):
            return [ep] if ep in self._vectors else []
        visited = {ep}
        d0 = _distance(q, self._vectors[ep])
        cands: list[tuple[float, str]] = [(d0, ep)]
        res: list[tuple[float, str]] = [(-d0, ep)]
        while cands:
            cd, cn = heapq.heappop(cands)
            if cd > -res[0][0]:
                break
            for nb in self._layers[lv].get(cn, set()):
                if nb in visited or nb not in self._vectors:
                    continue
                visited.add(nb)
                d = _distance(q, self._vectors[nb])
                if d < -res[0][0] or len(res) < ef:
                    heapq.heappush(cands, (d, nb))
                    heapq.heappush(res, (-d, nb))
                    if len(res) > ef:
                        heapq.heappop(res)
        return [n for _, n in res]

    def _select(self, q: list[float], cands: list[str],
                m: int) -> list[str]:
        if len(cands) <= m:
            return cands
        scored = [(c, _distance(q, self._vectors[c]))
                  for c in cands if c in self._vectors]
        scored.sort(key=lambda x: x[1])
        return [c for c, _ in scored[:m]]


class ExactKNNIndex:
    """Exact brute-force KNN index using cosine similarity.

    Zero randomness — insertion order does not affect results.
    Every query scans all stored vectors and returns the true top-k.
    O(n) per query; suitable for benchmark/evaluation where n < 50k.

    Uses numpy for fast batch dot-product when available (auto-detected),
    otherwise falls back to pure Python with pre-normalized vectors.
    """

    def __init__(self):
        self._vectors: dict[str, list[float]] = {}
        self._lock = threading.Lock()
        try:
            import numpy as np
            self._np = np
        except ImportError:
            self._np = None

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._vectors)

    def add(self, key: str, vector: list[float]):
        with self._lock:
            self._vectors[key] = vector

    def remove(self, key: str):
        with self._lock:
            self._vectors.pop(key, None)

    def contains(self, key: str) -> bool:
        with self._lock:
            return key in self._vectors

    def get_all_keys(self) -> list[str]:
        with self._lock:
            return list(self._vectors.keys())

    def query(self, vector: list[float], k: int = 10) -> list[tuple[str, float]]:
        with self._lock:
            if not self._vectors:
                return []
            keys = list(self._vectors.keys())
            distances = self._batch_distances(vector, keys)
            # Partial sort: only need top-k
            k = min(k, len(keys))
            # Use heapq.nsmallest for efficiency when k << n
            import heapq
            top = heapq.nsmallest(k, zip(distances, keys), key=lambda x: x[0])
            return [(key, dist) for dist, key in top]

    def query_radius(self, vector: list[float], radius: float,
                     max_results: int = 100) -> list[tuple[str, float]]:
        with self._lock:
            if not self._vectors:
                return []
            keys = list(self._vectors.keys())
            distances = self._batch_distances(vector, keys)
            results = [(key, dist) for key, dist in zip(keys, distances) if dist <= radius]
            results.sort(key=lambda x: x[1])
            return results[:max_results]

    def _batch_distances(self, query: list[float], keys: list[str]) -> list[float]:
        """Compute cosine distances (1 - similarity) for all keys. Uses numpy if available."""
        if self._np is not None:
            np = self._np
            q = np.array(query, dtype=np.float32)
            q_norm = np.linalg.norm(q)
            if q_norm == 0:
                return [1.0] * len(keys)
            q = q / q_norm
            # Stack all stored vectors into a matrix
            mat = np.array([self._vectors[k] for k in keys], dtype=np.float32)
            # Row-normalize
            norms = np.linalg.norm(mat, axis=1, keepdims=True)
            norms = np.where(norms == 0, 1.0, norms)
            mat = mat / norms
            # Cosine similarity = dot product of normalized vectors
            sims = mat @ q
            return (1.0 - sims).tolist()
        else:
            return [_distance(query, self._vectors[k]) for k in keys]


class HNSWLibIndex:
    """Adapter wrapping hnswlib. pip install hnswlib"""

    def __init__(self, dim: int, max_elements: int = 100_000,
                 M: int = 16, ef_construction: int = 200):
        try:
            import hnswlib
        except ImportError:
            raise ImportError("pip install hnswlib")
        self._idx = hnswlib.Index(space="cosine", dim=dim)
        self._idx.init_index(max_elements=max_elements, M=M,
                             ef_construction=ef_construction)
        self._idx.set_ef(50)
        self._k2l: dict[str, int] = {}
        self._l2k: dict[int, str] = {}
        self._next = 0

    @property
    def size(self) -> int:
        return len(self._k2l)

    def add(self, key: str, vector: list[float]):
        if key in self._k2l:
            lbl = self._k2l[key]
        else:
            lbl = self._next
            self._next += 1
            self._k2l[key] = lbl
            self._l2k[lbl] = key
        self._idx.add_items([vector], [lbl])

    def remove(self, key: str):
        if key in self._k2l:
            lbl = self._k2l.pop(key)
            self._l2k.pop(lbl, None)
            self._idx.mark_deleted(lbl)

    def contains(self, key: str) -> bool:
        return key in self._k2l

    def get_all_keys(self) -> list[str]:
        return list(self._k2l.keys())

    def query(self, vector: list[float], k: int = 10) -> list[tuple[str, float]]:
        if not self.size:
            return []
        lbls, dists = self._idx.knn_query([vector], k=min(k, self.size))
        return [(self._l2k[int(l)], float(d))
                for l, d in zip(lbls[0], dists[0]) if int(l) in self._l2k]

    def query_radius(self, vector: list[float], radius: float,
                     max_results: int = 100) -> list[tuple[str, float]]:
        return [(k, d) for k, d in self.query(vector, max_results)
                if d <= radius]
