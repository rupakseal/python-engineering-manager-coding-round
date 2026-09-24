from __future__ import annotations


class ConsoleAuditLogger:
    def info(self, event: str, details: str) -> None:
        print(f"INFO event={event} {details}")

    def warning(self, event: str, details: str) -> None:
        print(f"WARN event={event} {details}")


class NoOpMetricsRecorder:
    def increment(self, metric_name: str) -> None:
        pass

    def record_duration(self, metric_name: str, seconds: float) -> None:
        pass
