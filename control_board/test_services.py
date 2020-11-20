import pytest

from .entities import Batch, OrderLine
from .repository import AbstractRepository
from .services import allocate, InvalidSku


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = batches

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return self._batches


def test_returns_allocation():
    line = OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])

    result = allocate(line, repo)
    assert result.reference == "b1"


def test_error_for_invalid_sku():
    line = OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate(line, repo)
