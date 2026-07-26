# Testing Phase

The testing phase is a first-class part of TermOS agent. It is responsible for proving that the environment, skills, executor, verifier, and memory layers work before the system is used for real tasks.

## Modes

- **dev mode**: build and experiment
- **test mode**: run checks, collect evidence, and avoid destructive actions
- **release mode**: execute only approved and verified workflows

## Testing layers

### Unit tests
Validate one component at a time:
- environment inventory
- planner rules
- skill registry
- command executor
- verifier
- memory store

### Integration tests
Validate component combinations:
- inventory + planner
- planner + executor
- executor + verifier
- verifier + memory

### Workflow tests
Validate real jobs end to end:
- APK decode
- APK build
- APK sign
- file search
- shell command execution

### Regression tests
Prevent old failures from returning:
- missing dependencies
- permission problems
- path issues
- shell quoting issues
- Android/Termux quirks

## Readiness criteria

The repo is ready for testing when:
- the environment profiler works
- the executor can run a safe command reliably
- the verifier checks success correctly
- the memory layer stores test runs
- at least one workflow passes end to end
- the test machine returns structured feedback

## Feedback requirements

The test machine should return:
- test name
- status
- environment snapshot
- command run
- stdout
- stderr
- exit code
- runtime
- artifacts
- notes

## Output expectation

Testing should not just say "failed" or "passed". It should explain what happened, what was expected, and what the machine observed.
