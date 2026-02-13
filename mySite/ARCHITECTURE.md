# Project Architecture - Django PWA (Clean Architecture)

## Overview

This project follows Clean Architecture principles.

Layers:

- Domain → Pure business logic (no Django imports)
- Application → Use cases and orchestration
- Infrastructure → Django ORM, DB, external services
- Interface → Django Views / DRF / PWA endpoints

## Dependency Rule

Outer layers depend on inner layers.

Domain ← Application ← Infrastructure ← Interface

Domain must never depend on Django.

## PWA Context

- Service workers live in interface layer
- API endpoints serve JSON only
- No business logic inside views

## Folder Structure

app/
  domain/
  application/
  infrastructure/
  interfaces/
