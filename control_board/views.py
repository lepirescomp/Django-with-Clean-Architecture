from django.views.generic import CreateView
from django.http.response import HttpResponse

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

