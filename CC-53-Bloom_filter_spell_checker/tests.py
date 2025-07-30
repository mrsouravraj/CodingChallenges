from unittest import TestCase
from bloom_filter import BloomFilter

class TestBloomFilter(TestCase):

    def test_optimal_parameters_for_bloom_filter(self):
        # Test case: For 10 million elements and a false positive probability of 0.1% (1 in 1,000)
        m, k = BloomFilter.calculate_optimal_m_k(10 ** 7, 0.001)
        self.assertEqual(143775876, m)
        self.assertEqual(10, k)

        # Test case: For 1 million elements and a false positive probability of 0.01% (1 in 10,000)
        m, k = BloomFilter.calculate_optimal_m_k(10 ** 6, 0.0001)
        self.assertEqual(19170117, m)
        self.assertEqual(14, k)

        # Test case: For 100 million elements and a very low false positive rate of 1 in 1 billion
        m, k = BloomFilter.calculate_optimal_m_k(100_000_000, 1e-9)
        self.assertEqual(4313276270, m)
        self.assertEqual(30, k)

        # Edge case: Very small n and high FPP
        m, k = BloomFilter.calculate_optimal_m_k(10, 0.5)  # 50% FPP
        self.assertTrue(m > 0)
        self.assertTrue(k > 0)

    def test_bloom_filter_basic_insert_and_query(self):
        # Test insertion and successful lookup
        bf = BloomFilter.initialize(100, 0.01)
        bf.insert("hello")
        self.assertTrue(bf.query("hello"))

        # Test lookup of a non-inserted element (may be false positive, but unlikely)
        self.assertFalse(bf.query("world"))

    def test_bloom_filter_multiple_insertions(self):
        # Insert multiple elements and verify they can be queried
        items = ["apple", "banana", "cherry", "date", "fig", "grape"]
        bf = BloomFilter.initialize(1000, 0.01)
        for item in items:
            bf.insert(item)

        for item in items:
            self.assertTrue(bf.query(item))

        # Non-inserted item (low chance of false positive)
        self.assertFalse(bf.query("orange"))

    def test_bloom_filter_false_positive_rate(self):
        # Rough statistical test for false positives
        bf = BloomFilter.initialize(1000, 0.01)
        inserted = [f"item{i}" for i in range(1000)]
        for item in inserted:
            bf.insert(item)

        false_queries = [f"not_inserted_{i}" for i in range(1000)]
        false_positives = sum(1 for item in false_queries if bf.query(item))

        # Allowing margin based on expected false positive rate (~1%)
        self.assertLessEqual(false_positives, 30)  # Slightly lenient threshold

    def test_bloom_filter_empty_query(self):
        # Querying without any insertions should return false
        bf = BloomFilter.initialize(100, 0.01)
        self.assertFalse(bf.query("ghost"))
