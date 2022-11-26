from django.urls import path, re_path
from .views import GetAllView, GetView

urlpatterns = [
    path("nodes/", GetAllView.as_view(), name="get_all_node_view"),
    re_path(r"^nodes/(?P<node_id>\d+)/$", GetView.as_view(), name="get_node_view")
]
