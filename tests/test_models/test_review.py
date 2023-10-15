#!/usr/bin/python3
import unittest
from models.review import Review


class TestReview(unittest.TestCase):
    def test_initialization(self):
        review = Review()
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")

    def test_attribute_assignment(self):
        review = Review()
        review.place_id = "12345"
        review.user_id = "67890"
        review.text = "A great place to stay!"

        self.assertEqual(review.place_id, "12345")
        self.assertEqual(review.user_id, "67890")
        self.assertEqual(review.text, "A great place to stay!")


if __name__ == '__main__':
    unittest.main()
