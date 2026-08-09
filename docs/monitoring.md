# Monitoring

Technical:
- latency p50/p95/p99;
- camera / edge availability;
- ANN search latency;
- turnstile integration errors;
- cache age and sync lag.

ML:
- false reject rate;
- manual review rate;
- quality reject rate;
- liveness failures;
- drift по illumination / pose / quality.

Business:
- среднее и p95 время прохода;
- доля автоматических проходов;
- нагрузка на охрану;
- очередь в пик.

Alerts:
- p95 >1 сек 15 минут;
- FRR >3%;
- manual review >8%;
- cache age выше TTL;
- всплеск quality failures по конкретной камере.

Каждое решение расследуется по `event_id` через audit trail.
