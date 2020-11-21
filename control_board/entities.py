from dataclasses import dataclass

class OutOfStock(Exception):
    pass

def allocate(orderline, batches):
    if type(batches) != list:
        batches=[batches]
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(orderline))
        batch.batch_allocate(orderline)
        return batch
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {orderline.sku}')


class Batch:

    def __init__(self, reference, sku, qty, eta, ):
        self.reference = reference
        self.sku = sku
        self.qty = qty
        self.eta = eta
        self._allocated = set()

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return False
        return self.eta > other.eta

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    @property
    def alocatted_quantity(self):
        return sum(order_line.qty for order_line in self._allocated)

    @property
    def available_quantity(self):
        return self.qty - self.alocatted_quantity

    def can_allocate(self, orderline):
        return self.sku == orderline.sku and orderline.qty <= self.available_quantity

    def deallocate(self, orderline):
        if orderline in self._allocated:
            self._allocated.remove(orderline)
    
    def batch_allocate(self, line):
        if self.can_allocate(line):
            self._allocated.add(line)

@dataclass(unsafe_hash=True)
class OrderLine:
        reference: str
        sku: str
        qty: int