# Architecture

Гибридная архитектура: hot path на edge, управление идентичностями, enrollment, версии моделей, аудит и аналитика — в центре.

```mermaid
flowchart LR
    C[Camera] --> E[Edge inference]
    E --> Q[Quality + Liveness]
    Q --> M[Embedding + ANN]
    M --> D[Decision engine]
    D -->|allow| T[Turnstile]
    D -->|manual_review| G[Guard UI]
    D --> A[Local audit buffer]
    A --> CA[Central audit log]
    CS[Central employee service] -->|templates + policy updates| E
```

## Hot path
Camera → face detect → quality → alignment → liveness → embedding → ANN search → policy decision → turnstile.

## Async
- обновление шаблонов и access policy;
- централизованный audit log;
- monitoring;
- model rollout;
- аналитика качества.

## Offline
Свежий кеш допускает ограниченную работу. Старый кеш, недоступность модели/ANN или сомнительный кейс → `manual_review` / card fallback, но не auto-allow.
