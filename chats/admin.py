from django.contrib import admin
from django.contrib.admin.utils import quote
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Chat
from .services import UserService


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at"]
    change_form_template = "admin/chat/chat_form.html"

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(user=request.user)
        return qs.prefetch_related("messages")

    def add_view(self, request, form_url="", extra_context=None):
        service = UserService(request.user)
        chat = service.get_latest_or_create_chat()

        obj_url = reverse(
            "admin:%s_%s_change" % (self.opts.app_label, self.opts.model_name),
            args=(quote(chat.pk),),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(obj_url)
