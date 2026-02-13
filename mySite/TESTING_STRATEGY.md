# Testing Strategy

Test Levels:

1. Domain tests (pure unit tests)
2. Use case tests (mock repository)
3. Integration tests (Django + DB)

Rules:

- Never test ORM inside domain tests.
- Mock repositories in application tests.
- Keep business logic coverage high.
