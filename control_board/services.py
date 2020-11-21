
from __future__ import annotations

from .models import BatchORM, OrderLineORM
from .entities import OrderLine
from .entities import allocate as entity_allocate
from .repository import AbstractRepository, ORMRepository

class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in [b.sku for b in batches]

def allocate(line, repo):
    batches = repo.list()
    
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')

    if isinstance(repo,ORMRepository):
        ORMRepository.add(batch)
    
    return batches