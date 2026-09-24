# Candidate Instructions

## Scenario

Your team owns a high-volume OAuth token-validation service.

- Peak traffic: 10,000 requests per second
- Availability objective: 99.99%
- Normal downstream authorization latency: approximately 100 ms
- Incident behavior: downstream calls occasionally take longer than 10 seconds
- Last incident: pending coroutines and downstream connections accumulated until the service became unavailable
- Security requirement: raw tokens and customer identifiers must never appear in logs

The supplied asynchronous Python implementation passes its small baseline suite, but it is not production-ready.

## Assignment

Improve the service so that it fails safely and predictably when its downstream dependency is slow or unavailable.

Address as much as you reasonably can within 60 minutes:

1. Bound downstream latency with an appropriate async timeout.
2. Add concurrency-safe circuit-breaker behavior without a third-party library.
3. Decide whether retries are appropriate, and implement a safe policy if they are.
4. Ensure logs do not expose tokens, customer identifiers or sensitive exception text.
5. Add or improve tests for normal and failure behavior.
6. Add useful operational metrics through the supplied recorder protocol.
7. Document incomplete work and production tradeoffs in `ARCHITECTURE_NOTES.md`.

You may refactor any starter code and add new files. Do not call a real network service.

## AI policy

You may use an AI coding assistant. You remain responsible for every change. Be prepared to explain the context you supplied, output you rejected, how you verified the result, and what you would require before production approval.

Do not place confidential data, credentials or proprietary source code in an external AI tool.

## Discussion topics

- `asyncio.timeout` or `asyncio.wait_for` and cancellation semantics;
- retry amplification, backoff and jitter;
- task-safe circuit-breaker transitions;
- event-loop blocking and connection-pool exhaustion;
- fail-open versus fail-closed behavior;
- metrics, alerts, canary deployment and rollback;
- delegation and delivery ownership.

## Definition of done

- The code runs on Python 3.11 or newer.
- `run-tests.sh` or `run-tests.ps1` succeeds.
- New behavior is covered by tests.
- Sensitive values are not logged.
- Key decisions are recorded in `ARCHITECTURE_NOTES.md`.
