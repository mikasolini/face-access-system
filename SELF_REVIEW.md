# SELF_REVIEW

Самая слабая часть — PoC без реальной CV-модели и фактического FAR/FRR. Предполагается, что edge GPU обеспечивает sub-second pipeline и локальный ANN. Не закрыты юридические детали биометрии, advanced spoofing и production enrollment.

За два дополнительных дня я бы добавил реальный baseline на готовых моделях, demo validation set, latency benchmark и контейнер. Перед production нужны threat model, penetration test, юридическая проверка и калибровка порогов.

Нельзя полностью автоматизировать low liveness/quality, weak margin, stale policy и security-инциденты.

Проект следует остановить при подтверждённом false accept, при невозможности получить приемлемый FAR без неприемлемого FRR/очередей или если manual review остаётся настолько высоким, что экономический эффект исчезает.
