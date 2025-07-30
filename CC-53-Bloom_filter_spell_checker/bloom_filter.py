import math
from fnv1a_hash import fnv1a_hash

class BloomFilter(object):

    def __init__(self, m: int, k: int, filter_array: list):
        self.array_size = m
        self.num_hash_fns = k
        self.filter_array = filter_array

    @classmethod
    def initialize(cls, num_of_items: int, false_pos: int):
        m, k = cls.calculate_optimal_m_k(num_of_items, false_pos)
        return BloomFilter(m, k, [0] * m)

    @classmethod
    def calculate_optimal_m_k(cls, n: int, p: int):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        k = (m / n) * math.log(2)
        return int(math.ceil(m)), int(math.ceil(k))

    def insert(self, item):
        """
        Insert items by applying the hash functions and setting the corresponding bits to 1
        """
        for hash_value in self.compute_hashes(item):
            self.filter_array[hash_value] = 1

    def query(self, item):
        for hash_value in self.compute_hashes(item):
            if self.filter_array[hash_value] == 0:
                return False
        return True

    def compute_hashes(self, data):
        hash_values = []
        for i in range(0, self.num_hash_fns):
            # Use different seeds for different hash functions
            seed = str(i + 1)
            data = "%s%s" % (seed, data)
            hash = fnv1a_hash(data)
            hash_values.append(hash % self.array_size)

        return hash_values
