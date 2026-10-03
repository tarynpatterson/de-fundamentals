import logging

import pytest

from dekit.retry import retry


class CallTracker:
    def __init__(self):
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        return "success"


def test_retry_succeeds_first_try():
    tracker = CallTracker()
    decorated = retry()(tracker)

    result = decorated()

    assert result == "success"
    assert tracker.call_count == 1


class FlakyTracker:
    def __init__(self, fail_times):
        self.call_count = 0
        self.fail_times = fail_times

    def __call__(self):
        self.call_count += 1
        if self.call_count <= self.fail_times:
            raise ValueError(f"failing on call {self.call_count}")
        return "success"


def test_retry_succeeds_after_failures(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda seconds: None)

    tracker = FlakyTracker(fail_times=2)
    decorated = retry(max_attempts=5, base_delay=1.0)(tracker)

    result = decorated()

    assert result == "success"
    assert tracker.call_count == 3


def test_retry_raises_after_max_attempts(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda seconds: None)

    tracker = FlakyTracker(fail_times=10)
    decorated = retry(max_attempts=3, base_delay=1.0)(tracker)

    with pytest.raises(ValueError, match="failing on call 3"):
        decorated()

    assert tracker.call_count == 3


class WrongExceptionTracker:
    def __init__(self):
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        raise TypeError("this should not be retried")


def test_retry_does_not_retry_unlisted_exceptions(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda seconds: None)

    tracker = WrongExceptionTracker()
    decorated = retry(max_attempts=5, exceptions=(ValueError,))(tracker)

    with pytest.raises(TypeError):
        decorated()

    assert tracker.call_count == 1


def test_retry_delays_follow_backoff(monkeypatch):
    recorded_delays = []
    monkeypatch.setattr("time.sleep", lambda seconds: recorded_delays.append(seconds))

    tracker = FlakyTracker(fail_times=3)
    decorated = retry(max_attempts=5, base_delay=1.0, backoff_multiplier=2.0)(tracker)

    decorated()

    assert recorded_delays == [1.0, 2.0, 4.0]


def test_retry_preserves_metadata():
    @retry()
    def my_function(x):
        """My docstring."""
        return x

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "My docstring."


def test_retry_logs_warning_on_retry(monkeypatch, caplog):
    monkeypatch.setattr("time.sleep", lambda seconds: None)

    tracker = FlakyTracker(fail_times=1)
    decorated = retry(max_attempts=3, base_delay=1.0)(tracker)

    with caplog.at_level(logging.WARNING):
        decorated()

    assert "Attempt 1/3" in caplog.text
    assert "Retrying" in caplog.text
