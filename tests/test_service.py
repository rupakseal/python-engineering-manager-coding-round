from __future__ import annotations

import unittest
from collections import Counter

from token_validation import (
    AuthorizationDecision,
    TokenValidationService,
    ValidationStatus,
)


class FakeAuditLogger:
    def __init__(self) -> None:
        self.entries: list[str] = []

    def info(self, event: str, details: str) -> None:
        self.entries.append(f"INFO {event} {details}")

    def warning(self, event: str, details: str) -> None:
        self.entries.append(f"WARN {event} {details}")


class FakeMetrics:
    def __init__(self) -> None:
        self.counters: Counter[str] = Counter()
        self.durations: list[tuple[str, float]] = []

    def increment(self, metric_name: str) -> None:
        self.counters[metric_name] += 1

    def record_duration(self, metric_name: str, seconds: float) -> None:
        self.durations.append((metric_name, seconds))


class StaticClient:
    def __init__(self, decision: AuthorizationDecision) -> None:
        self.decision = decision
        self.calls = 0

    async def validate(self, token: str) -> AuthorizationDecision:
        self.calls += 1
        return self.decision


class EventuallySuccessfulClient:
    def __init__(self) -> None:
        self.calls = 0

    async def validate(self, token: str) -> AuthorizationDecision:
        self.calls += 1
        if self.calls < 3:
            raise ConnectionError("temporary failure")
        return AuthorizationDecision.allowed("subject-123")


class TokenValidationServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_valid_decision(self) -> None:
        client = StaticClient(AuthorizationDecision.allowed("subject-123"))
        metrics = FakeMetrics()
        service = TokenValidationService(client, FakeAuditLogger(), metrics)

        result = await service.validate("header.payload.signature", "customer-456")

        self.assertEqual(ValidationStatus.VALID, result.status)
        self.assertEqual("subject-123", result.subject)
        self.assertEqual(1, metrics.counters["validation.success"])

    async def test_rejects_missing_token(self) -> None:
        client = StaticClient(AuthorizationDecision.allowed("never-used"))
        service = TokenValidationService(client, FakeAuditLogger(), FakeMetrics())

        result = await service.validate(" ", "customer-456")

        self.assertEqual(ValidationStatus.INVALID, result.status)
        self.assertEqual(0, client.calls)

    async def test_retries_downstream_failure(self) -> None:
        client = EventuallySuccessfulClient()
        service = TokenValidationService(client, FakeAuditLogger(), FakeMetrics())

        result = await service.validate("header.payload.signature", "customer-456")

        self.assertEqual(ValidationStatus.VALID, result.status)
        self.assertEqual(3, client.calls)


if __name__ == "__main__":
    unittest.main()
