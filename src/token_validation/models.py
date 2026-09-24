from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    active: bool
    subject: str | None
    reason: str

    @classmethod
    def allowed(cls, subject: str) -> AuthorizationDecision:
        return cls(True, subject, "active")

    @classmethod
    def denied(cls, reason: str) -> AuthorizationDecision:
        return cls(False, None, reason)


class ValidationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    TEMPORARILY_UNAVAILABLE = "temporarily_unavailable"


@dataclass(frozen=True, slots=True)
class ValidationResult:
    status: ValidationStatus
    subject: str | None
    message: str

    @classmethod
    def valid(cls, subject: str) -> ValidationResult:
        return cls(ValidationStatus.VALID, subject, "token active")

    @classmethod
    def invalid(cls, reason: str) -> ValidationResult:
        return cls(ValidationStatus.INVALID, None, reason)

    @classmethod
    def unavailable(cls) -> ValidationResult:
        return cls(
            ValidationStatus.TEMPORARILY_UNAVAILABLE,
            None,
            "authorization dependency unavailable",
        )
