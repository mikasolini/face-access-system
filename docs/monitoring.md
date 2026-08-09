# Monitoring

Technical: latency p50/p95/p99, camera/edge availability, ANN latency, turnstile errors, cache age.

ML: FRR, manual review rate, quality rejects, liveness failures, drift по illumination/pose/quality.

Business: время прохода, доля автоматических проходов, нагрузка на охрану, очередь в пик.

Alerts: p95 >1 сек 15 минут; FRR >3%; manual review >8%; stale cache; всплеск quality failures по камере.

Расследование по `event_id` и `decision_id` через audit trail.
