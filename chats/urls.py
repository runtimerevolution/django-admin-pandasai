from django.urls import path

from .views import ChatView

urlpatterns = [
    path("chat/<int:id>/", ChatView.as_view(), name="chat"),
]
