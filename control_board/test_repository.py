from django.db import connection
import pytest

from .entities import Batch, OrderLine
from .repository import ORMRepository
from .models import BatchORM, OrderLineORM, AllocationsORM

@pytest.mark.django_db
def test_repository_can_save_a_batch():
    batch = Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    ORMRepository.add(batch)

    rows = list(BatchORM.objects.raw(
        'SELECT * FROM "control_board_batchorm"'
    ))

    assert rows[0].reference == batch.reference
    assert rows[0].sku == batch.sku
    assert rows[0].qty == batch.qty

@pytest.mark.django_db
def insert_order_line():
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO control_board_orderlineorm (reference, sku, qty)'
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = cursor.execute(
        'SELECT id FROM control_board_orderlineorm WHERE reference="order1" AND sku="GENERIC-SOFA"',
    )
    return orderline_id

@pytest.mark.django_db
def insert_batch(batch_id):
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO control_board_batchorm (reference, sku, qty, eta) VALUES ("{batch_id}", "GENERIC-SOFA", 100, null)',
    )
    [[batch_id]] = cursor.execute(
        f'SELECT id FROM control_board_batchorm WHERE reference="{batch_id}" AND sku="GENERIC-SOFA"',
    )
    return batch_id

@pytest.mark.django_db
def insert_allocation(orderline_id, batch_id):
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO control_board_allocationsorm (batch_id, order_line_id) VALUES ("{batch_id}","{orderline_id}")',
    )

@pytest.mark.django_db
def test_repository_can_retrieve_a_batch_with_allocations():
    orderline_id = insert_order_line()
    batch1_id = insert_batch("batch1")
    insert_batch("batch2")
    insert_allocation(orderline_id, batch1_id)

    retrieved = ORMRepository.get("batch1")

    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference
    assert retrieved.sku == expected.sku
    assert retrieved.qty == expected.qty
    assert retrieved._allocated == {
        OrderLine("order1", "GENERIC-SOFA", 12),
    }