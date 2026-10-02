import unittest

from light_malib.utils.metric import Metrics, SlidingMetric


class TestSlidingMetric(unittest.TestCase):
    def test_retains_latest_values_after_wraparound(self):
        for initial in ([], [1], [1, 2, 3]):
            with self.subTest(initial=initial):
                metric = SlidingMetric(window_size=3, init_list=initial)
                history = list(initial)
                for value in range(len(initial) + 1, 11):
                    history.append(value)
                    metric.update(value)
                    recent = history[-3:]
                    self.assertAlmostEqual(metric.mean(), sum(recent) / len(recent))

    def test_rollout_metrics_replace_oldest_score(self):
        metrics = Metrics({"score": {"type": "sliding", "window_size": 3}})
        for score in [1, 2, 3, 10]:
            metrics.update({"score": score})
        self.assertEqual(metrics.get_means(), {"score": 5})

    def test_single_value_window(self):
        metric = SlidingMetric(window_size=1)
        self.assertIsNone(metric.mean())
        for value in [2, 5, -1]:
            metric.update(value)
            self.assertEqual(metric.mean(), value)
