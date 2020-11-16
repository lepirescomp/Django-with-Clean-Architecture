import abc
from .models import BatchORM, OrderLineORM
from .entities import Batch, OrderLine

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

class ORMRepository(AbstractRepository):
    @staticmethod
    def add(batch):
        for orderline in batch._allocated:
            if orderline is not None:
                orderline = OrderLineORM.objects.create(
                    reference=orderline.reference,
                    sku=orderline.sku,
                    qty=orderline.qty)

                BatchORM.objects.create(
                    reference = batch.reference,
                    sku = batch.sku,
                    qty = batch.qty,
                    eta = batch.eta,
                    allocated = orderline
                )
    @staticmethod
    def get(reference):
        batch_orm = BatchORM.objects.get(reference=reference)
        orderline_id = batch_orm.allocated_id
        orderline_orm = OrderLineORM.objects.filter(id=orderline_id)
        for ol in orderline_orm:

            batch =Batch(
                reference=batch_orm.reference,
                sku = batch_orm.sku,
                qty= batch_orm.qty,
                eta = batch_orm.eta,
                )
            
            batch.allocate(OrderLine(
                reference=ol.reference,
                sku=ol.sku,
                qty=ol.qty
                ))