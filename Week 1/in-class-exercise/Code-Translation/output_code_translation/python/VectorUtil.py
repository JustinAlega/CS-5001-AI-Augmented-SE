import math
from typing import List, Dict, Sequence, Tuple, Any


class VectorUtil:
    @staticmethod
    def _norm(vec: Sequence[float]) -> float:
        total = 0.0
        for v in vec:
            total += v * v
        return math.sqrt(total)

    @staticmethod
    def _normalize(vec: Sequence[float]) -> List[float]:
        norm_val = VectorUtil._norm(vec)
        if norm_val == 0.0:
            return [0.0 for _ in vec]
        return [v / norm_val for v in vec]

    @staticmethod
    def similarity(vector_1: Sequence[float], vector_2: Sequence[float]) -> float:
        norm_vec1 = VectorUtil._normalize(vector_1)
        norm_vec2 = VectorUtil._normalize(vector_2)
        dot_product = 0.0
        for a, b in zip(norm_vec1, norm_vec2):
            dot_product += a * b
        return dot_product

    @staticmethod
    def cosine_similarities(
        vector_1: Sequence[float],
        vectors_all: List[Sequence[float]]
    ) -> List[float]:
        similarities: List[float] = []
        norm_vec1 = VectorUtil._norm(vector_1)

        for vec in vectors_all:
            norm_vec_all = VectorUtil._norm(vec)
            if norm_vec_all == 0.0:
                similarities.append(0.0)
                continue
            dot_product = sum(a * b for a, b in zip(vec, vector_1))
            similarity = dot_product / (norm_vec1 * norm_vec_all)
            similarities.append(similarity)

        return similarities

    @staticmethod
    def n_similarity(
        vector_list_1: List[Sequence[float]],
        vector_list_2: List[Sequence[float]]
    ) -> float:
        if not vector_list_1 or not vector_list_2:
            raise ValueError("At least one of the lists is empty.")

        dim = len(vector_list_1[0])
        mean_vec1 = [0.0] * dim
        mean_vec2 = [0.0] * dim

        for vec in vector_list_1:
            for i in range(dim):
                mean_vec1[i] += vec[i]

        for vec in vector_list_2:
            for i in range(dim):
                mean_vec2[i] += vec[i]

        size1 = len(vector_list_1)
        size2 = len(vector_list_2)
        mean_vec1 = [v / size1 for v in mean_vec1]
        mean_vec2 = [v / size2 for v in mean_vec2]

        return VectorUtil.similarity(mean_vec1, mean_vec2)

    @staticmethod
    def compute_idf_weight_dict(
        total_num: int,
        number_dict: Dict[str, float]
    ) -> Dict[str, float]:
        result: Dict[str, float] = {}
        index_2_key_map: Dict[int, str] = {}
        count_list: List[float] = []

        for idx, (key, count) in enumerate(number_dict.items()):
            index_2_key_map[idx] = key
            count_list.append(count)

        a = [0.0] * len(count_list)
        for i, cnt in enumerate(count_list):
            a[i] = math.log((total_num + 1.0) / (cnt + 1.0))

        for i, value in enumerate(a):
            result[index_2_key_map[i]] = value

        return result
