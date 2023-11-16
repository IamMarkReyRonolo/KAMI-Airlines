from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_all_airplanes),
    path("<int:id>", views.get_airplane_by_id),
    path("add", views.add_airplane),
    path("bulk_add", views.bulk_add_airplanes),
    path("update/<int:id>", views.update_airplane),
    path("delete/<int:id>", views.delete_airplane),
    path("delete/all", views.delete_all_airplane),
]
