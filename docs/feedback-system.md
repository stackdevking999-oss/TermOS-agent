# Feedback System

TermOS agent uses a shared feedback contract for every meaningful run:

- environment collection
- task planning
- task execution
- test execution
- repair attempts
- release validation

## Goal

The system should always know:

1. what it was trying to do
2. what happened
3. what changed after the fix
4. whether the outcome should be stored as a reusable lesson

## Shared object

The canonical object is `RunFeedback`.

It carries:
- kind
- name
- status
- environment
- command
- stdout
- stderr
- exit code
- runtime
- artifacts
- notes
- metadata

## Storage

All feedback events are written to `feedback_events` in SQLite. Existing task, environment, and test tables remain as compatibility layers.

## Why this matters

A self-improving agent needs evidence. Feedback is the evidence.
