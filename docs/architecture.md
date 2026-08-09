# Architecture

Гибрид: hot path на edge, управление идентичностями, enrollment, model rollout и аудит — в центре.

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
    CS[Central employee service] -->|templates/policy updates| E
```

Hot path: camera → detect → quality → alignment → liveness → embedding → ANN → policy decision → turnstile.
Async: шаблоны/policy, аудит, мониторинг, model rollout, аналитика.
