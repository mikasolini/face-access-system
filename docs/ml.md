# ML design

Pipeline: face detection → quality → alignment → liveness → embedding → one-to-many ANN → decision rules.

На проходной нужна identification, а не только verification: поиск сотрудника среди разрешённой базы.

Baseline: готовые предобученные модели + FAISS/HNSW-like ANN. В PoC эти части mock.

Исходы:
- `allow`: quality/liveness OK, высокий match и достаточный margin;
- `manual_review`: low quality, borderline liveness, weak margin, degraded mode;
- `deny`: spoof / policy deny / match ниже порога.

Метрики: FAR, FRR, EER, ROC/PR, manual review rate, latency.

Validation: split по личностям, а не по кадрам; разные камеры, дни, освещение и ракурсы. LLM не нужен в hot path allow/deny: решение должно быть быстрым, детерминированным и аудируемым.
