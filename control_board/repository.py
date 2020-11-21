import abc
from .models import BatchORM, OrderLineORM, AllocationsORM
from .entities import Batch, OrderLine

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError


class ORMRepository(AbstractRepository):
    @staticmethod
    def add(batch):
        if len(batch._allocated) == 0:            
            batch_orm = BatchORM.objects.create(
                reference = batch.reference,
                sku = batch.sku,
                qty = batch.qty,
                eta = batch.eta,
            )
                         
        for orderline in batch._allocated:
            if orderline is not None:
                orderline_orm = OrderLineORM.objects.create(
                    reference=orderline.reference,
                    sku=orderline.sku,
                    qty=orderline.qty)

                batch_orm = BatchORM.objects.create(
                    reference = batch.reference,
                    sku = batch.sku,
                    qty = batch.qty,
                    eta = batch.eta,
                    
                )

                AllocationsORM.objects.create(
                    order_line=orderline_orm,
                    batch=batch_orm
                )


    @staticmethod
    def get(reference):
        orderline_id = None

        batch_orm = BatchORM.objects.get(reference=reference)
        orderline_id = AllocationsORM.objects.get(batch_id=batch_orm.id)

        if orderline_id is not None:
            orderline_orm = OrderLineORM.objects.filter(id=orderline_id.id)

        for ol in orderline_orm:

            batch =Batch(
                reference=batch_orm.reference,
                sku = batch_orm.sku,
                qty= batch_orm.qty,
                eta = batch_orm.eta,
                )
            
            batch.batch_allocate(OrderLine(
                reference=ol.reference,
                sku=ol.sku,
                qty=ol.qty
                ))

        return batch

    @staticmethod
    def list():
        batches_return_list = []

        batches = BatchORM.objects.all()
        
        for batch_orm in batches:
            batches_return_list.append(Batch(
                reference=batch_orm.reference,
                sku = batch_orm.sku,
                qty= batch_orm.qty,
                eta = batch_orm.eta,
            ))

        return batches_return_list