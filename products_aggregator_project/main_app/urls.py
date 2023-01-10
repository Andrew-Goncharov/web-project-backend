from django.urls import path, re_path
from .views import GetAllView, GetView, ImportView, DeleteView

urlpatterns = [
    path("nodes/", GetAllView.as_view(), name="get_all_node_view"),
    path("imports/", ImportView.as_view(), name="import_nodes_view"),
    path("delete/<str:node_id>", DeleteView.as_view(), name="delete_node_view"),
    re_path(r"^nodes/(?P<node_id>\d+)/$", GetView.as_view(), name="get_node_view")
]
# re_path(r"^delete/(?P<node_id>\d+)/$", DeleteView.as_view(), name="delete_node_view"),