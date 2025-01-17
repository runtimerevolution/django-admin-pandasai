from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    JsonResponse,
)
from django.utils.decorators import method_decorator
from django.views.generic import View

from .models import Chat
from .services import ChatService


class ChatView(View):
    """
    Class-based view to handle admin chat messages.
    """

    @method_decorator(staff_member_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            chat = Chat.objects.get(id=id, user=request.user)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        except ValueError:
            return HttpResponseBadRequest()

        content = request.POST.get("content")

        service = ChatService(chat)
        message = service.send_message(content)

        return JsonResponse({"output": message.content})
