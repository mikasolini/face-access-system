# Risks and Operations

## Low-latency, надёжность и деградация
1. Детекция, quality, liveness, embedding и ANN — на edge; цель p95 <1 сек.
2. На edge — шифрованный кеш активных templates и policy с TTL; отзыв доступа синхронизируется приоритетно.
3. При потере сети или stale cache сомнительный кейс не получает auto-allow: карта/manual review.
4. `event_id` — idempotency key; повтор не открывает турникет второй раз. Offline audit синхронизируется после восстановления связи.

## Privacy, safety и governance
1. Эмбеддинги считаются чувствительными биометрическими шаблонами; шифрование at rest/in transit.
2. Исходные кадры по умолчанию не сохраняются; инциденты — только краткосрочно по отдельной политике.
3. RBAC к шаблонам, audit log всех enrollment/change/access решений.
4. При увольнении/отзыве согласия шаблон удаляется в центре и отзывается на edge; старый policy cache не должен давать auto-allow.
