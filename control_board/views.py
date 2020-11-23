from django.views.generic import CreateView
from django.http.response import HttpResponse
import datetime

from .repository import ORMRepository
from .entities import OrderLine, OutOfStock
from .services import allocate as service_allocate, InvalidSku

class AllocateViewSet(CreateView):

    def post(self, request, *args, **kwargs):
        batches = ORMRepository
        kwargs = request.environ["kwargs"]

        lines = OrderLine(
                kwargs["reference"],
                kwargs["sku"],
                kwargs["qty"]
            )
        try:  
            service_allocate(lines, batches)
        except(OutOfStock, InvalidSku) as e:
            return HttpResponse(status=400)

        return HttpResponse(status=201)

class AddBatchViewSet(CreateView):

    def post(self, request, *args, **kwargs):
        repo = ORMRepository
        kwargs = request.environ["kwargs"]
        
        eta = kwargs['eta']
        if eta is not None:
            eta = datetime.fromisoformat(eta).date()
        services.add_batch(
            kwargs['ref'], kwargs['sku'], kwargs['qty'], eta,
            repo
        )
        return HttpResponse(status=201)