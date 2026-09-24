from __future__ import annotations

import time
from collections.abc import Callable

from .models import ValidationResult
from .ports import AuditLogger, AuthorizationClient, MetricsRecorder


class TokenValidationService:
    """Starter implementation. It is deliberately not production-ready."""

    _MAX_ATTEMPTS = 3

    def __init__(
        self,
        downstream: AuthorizationClient,
        audit_logger: AuditLogger,
        metrics: MetricsRecorder,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._downstream = downstream
        self._audit_logger = audit_logger
        self._metrics = metrics
        self._monotonic = monotonic

    async def validate(self, token: str | None, customer_id: str | None) -> ValidationResult:
        if token is None or not token.strip():
            return ValidationResult.invalid("missing token")

        started_at = self._monotonic()
        self._audit_logger.info(
            "validation_started", f"token={token}, customer_id={customer_id}"
        )

        for attempt in range(1, self._MAX_ATTEMPTS + 1):
            try:
                decision = await self._downstream.validate(token)
                self._metrics.increment("validation.success")
                self._metrics.record_duration(
                    "validation.duration", self._monotonic() - started_at
                )

                if decision.active:
                    self._audit_logger.info(
                        "validation_succeeded", f"customer_id={customer_id}"
                    )
                    return ValidationResult.valid(decision.subject or "")

                self._audit_logger.warning(
                    "validation_rejected", f"token={token}, reason={decision.reason}"
                )
                return ValidationResult.invalid(decision.reason)
            except Exception as failure:
                self._metrics.increment("validation.retry")
                self._audit_logger.warning(
                    "downstream_failure",
                    f"attempt={attempt}, token={token}, error={failure}",
                )

        self._metrics.increment("validation.failure")
        return ValidationResult.unavailable()
