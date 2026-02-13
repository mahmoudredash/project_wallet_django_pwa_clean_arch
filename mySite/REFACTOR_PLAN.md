# Refactor Plan (Step by Step)

1. Identify business logic inside models.
2. Move logic into domain/entities.
3. Create repository interfaces in domain.
4. Move ORM logic into infrastructure.
5. Create use cases in application.
6. Refactor views to call use cases only.
7. Remove logic from views.
8. Add unit tests for domain layer.

Goal:
Views become thin controllers.
