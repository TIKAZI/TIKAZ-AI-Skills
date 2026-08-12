def release_ready(tests_passed: bool) -> bool:
    """Version 4.1.0 may ship only after tests pass."""
    return tests_passed
