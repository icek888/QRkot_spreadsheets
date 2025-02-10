from datetime import datetime

from app.models.base import InvestmentBase


def invest(
    target: InvestmentBase,
    sources: list[InvestmentBase]
) -> list[InvestmentBase]:
    '''Процесс инвестирования без асинхронных операций и работы с сессией.'''
    updated = []
    close_date = datetime.now()
    for source in sources:
        source_remaining = source.full_amount - source.invested_amount
        if source_remaining <= 0:
            continue
        target_remaining = target.full_amount - target.invested_amount
        transfer = min(target_remaining, source_remaining)
        for obj in (source, target):
            obj.invested_amount += transfer
            if obj.invested_amount >= obj.full_amount:
                obj.fully_invested = True
                obj.close_date = close_date
        updated.append(source)
        if target.fully_invested:
            break
    return updated
