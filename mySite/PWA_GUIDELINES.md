# Django PWA Guidelines

- Service worker logic stays in interface layer.
- No business logic inside JavaScript.
- API responses must be JSON only.
- Offline logic handled in frontend only.
- Backend remains stateless.

API rules:
- Always return structured JSON
- No HTML rendering inside API views
