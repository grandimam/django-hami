import unittest
from protego.client import ProtegoClient
from protego.client import ProtegoClientState

class TestCircuitBreaker(unittest.TestCase):
    def test_circuit_closes_on_success(self):
        breaker = ProtegoClient(failure_threshold=2)

        def success_func():
            return "Success"

        result = breaker.call(success_func)
        self.assertEqual(result, "Success")
        self.assertEqual(breaker.state, ProtegoClientState.CLOSED)

    def test_circuit_opens_on_failure(self):
        breaker = ProtegoClient(failure_threshold=2)

        def fail_func():
            raise Exception("Failure")

        with self.assertRaises(Exception):
            breaker.call(fail_func)
        with self.assertRaises(Exception):
            breaker.call(fail_func)

        self.assertEqual(breaker.state, ProtegoClientState.OPEN)
