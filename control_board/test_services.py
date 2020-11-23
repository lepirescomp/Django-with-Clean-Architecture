import pytest

from .entities import Batch, OrderLine
from .repository import AbstractRepository, FakeRepository
from .services import allocate, InvalidSku

pytest.fixture
def for_batch(ref, sku, qty, eta=None):
    return FakeRepository([
        Batch(ref, sku, qty, eta),
    ])


def test_returns_allocation():
    repo = for_batch("b1", "COMPLICATED-LAMP", 100, eta=None)

    result = allocate("o1", "COMPLICATED-LAMP", 10, repo)
    assert result[0].reference == "b1"


def test_error_for_invalid_sku():
    repo = for_batch("b1", "AREALSKU", 100, eta=None)

    with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate("o1", "NONEXISTENTSKU", 10, repo)
