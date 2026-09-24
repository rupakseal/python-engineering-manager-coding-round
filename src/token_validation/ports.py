from __future__ import annotations

from typing import Protocol

from .models import AuthorizationDecision


class AuthorizationClient(Protocol):
    async def validate(self, token: str) -> AuthorizationDecision: ...


class AuditLogger(Protocol):
    def info(self, event: str, details: str) -> None: ...
    def warning(self, event: str, details: str) -> None: ...


class MetricsRecorder(Protocol):
    def increment(self, metric_name: str) -> None: ...
    def record_duration(self, metric_name: str, seconds: float) -> None: ...
