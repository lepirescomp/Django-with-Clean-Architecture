import pytest

from .entities import Batch, OrderLine
from .repository import AbstractRepository, FakeRepository
from .services import allocate, InvalidSku

def test_returns_allocation():
    line = OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])

    result = allocate(line, repo)
    assert result[0].reference == "b1"


def test_error_for_invalid_sku():
    line = OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate(line, repo)
