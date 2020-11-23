
from __future__ import annotations

from .models import BatchORM, OrderLineORM
from .entities import OrderLine
from .entities import allocate as entity_allocate
from .repository import AbstractRepository, ORMRepository, FakeRepository

class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in [b.sku for b in batches]


def add_batch(ref, sku, qty, eta=None, repo):
    repo.add(Batch(ref, sku, qty, eta))


def allocate(id, sku, qty, repo):
    batches = repo.list()
    line = OrderLine(id,sku,qty)  
      
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')

    batch = entity_allocate(line,batches)

    repo.add(batch)

    return [batch]