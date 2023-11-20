from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_all_airplanes, name="get_all_airplanes"),
    path("<int:id>", views.get_airplane_by_id, name="get_airplane_by_id"),
    path("add", views.add_airplane, name="add_airplane"),
    path("bulk_add", views.bulk_add_airplanes, name="bulk_add_airplanes"),
    path("update/<int:id>", views.update_airplane, name="update_airplane"),
    path("delete/<int:id>", views.delete_airplane, name="delete_airplane"),
    path("delete/all", views.delete_all_airplane, name="delete_all_airplane"),
]
