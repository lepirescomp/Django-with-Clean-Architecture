from django.views.generic import CreateView
from django.http.response import HttpResponse

from .repository import ORMRepository
from .entities import OrderLine, allocate

class AllocateViewSet(CreateView):

    def post(self, request, *args, **kwargs):
        batches = ORMRepository.list()
        kwargs = request.environ["kwargs"]

        lines = OrderLine(
                kwargs["reference"],
                kwargs["sku"],
                kwargs["qty"]
            )
            
        allocate(lines, batches)
        return HttpResponse(status=201)

