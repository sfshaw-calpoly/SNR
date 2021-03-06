import threading
import time

from snr import *

SLEEP_TIME_S = 0.000050
CATCH_UP_TIME_S = SLEEP_TIME_S * 4


class TestConsumer(SNRTestCase):

    def test_increment(self):
        self.num: int = 0

        def increment(n: int) -> None:
            self.num += n

        self.assertEqual(0, self.num)
        increment(0)
        self.assertEqual(0, self.num)
        increment(1)
        self.assertEqual(1, self.num)
        increment(2)
        self.assertEqual(3, self.num)

    def test_consumer_start_join(self):
        consumer = Consumer[int]("test_start_join",
                                 lambda _: None,
                                 SLEEP_TIME_S)

        time.sleep(CATCH_UP_TIME_S)
        self.assertTrue(consumer.is_alive())

        time.sleep(CATCH_UP_TIME_S)
        self.assertTrue(consumer.is_alive())

        consumer.join_from("test complete")
        self.assertFalse(consumer.is_alive())
        time.sleep(CATCH_UP_TIME_S)
        self.assertFalse(consumer.is_alive())

    def test_consumer_put(self):

        self.lock = threading.Lock()
        self.num: int = 0

        def increment(n: int) -> None:
            with self.lock:
                self.num += n

        def check(value: int) -> None:
            with self.lock:
                self.assertEqual(value, self.num)
        consumer = Consumer("test_put",
                            increment,
                            SLEEP_TIME_S)

        def flush() -> None:
            if consumer.is_alive():
                time.sleep(CATCH_UP_TIME_S)
                consumer.flush()
                time.sleep(CATCH_UP_TIME_S)
                consumer.flush()

        try:

            flush()
            self.assertTrue(consumer.is_alive())
            check(0)

            consumer.put(0)
            flush()
            check(0)

            consumer.put(1)
            flush()
            check(1)

            self.assertTrue(consumer.is_alive())
            consumer.put(2)
            flush()
            check(3)
            self.assertTrue(consumer.is_alive())

            consumer.join_from("test complete")
            flush()
            self.assertFalse(consumer.is_alive())
            check(3)
        finally:
            if consumer.is_alive():
                consumer.join_from("test complete")
