# ML design

Pipeline: face detection → quality estimation → alignment → liveness → embedding → one-to-many ANN search → decision rules.

На проходной нужна identification: система ищет человека среди базы разрешённых сотрудников.

Baseline: готовые предобученные модели для detection/liveness/embeddings, ANN — FAISS/HNSW-like индекс. В PoC эти части упрощены mock-эмбеддингами и полным перебором маленькой базы.

Три исхода:
- `allow`: высокий match, достаточный margin, quality/liveness OK;
- `manual_review`: низкое качество, borderline liveness, слабый margin, degraded mode;
- `deny`: spoof / отсутствие разрешения / низкий match.

Цена false accept выше false reject, поэтому allow threshold выбирается консервативно.

Метрики: FAR, FRR, EER, ROC/PR, manual review rate, latency.

Validation: split по личностям, разные камеры, дни, освещение, маски/очки и ракурсы. Delayed labels: ручные проверки охраны, проход по карте после отказа, жалобы сотрудников.

LLM не нужен в hot path `allow/deny`: решение должно быть детерминированным, быстрым и аудируемым.
