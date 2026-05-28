from django.urls import path

from .views import CartDetailView, CartAddView, CartRemoveView, CartUpdateAjaxView

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    # add / remove برای همه مدل‌ها
    path(
        "add/<str:app_label>/<str:model_name>/<int:object_id>/",
        CartAddView.as_view(),
        name="add",
    ),
    path(
        "remove/<str:app_label>/<str:model_name>/<int:object_id>/",
        CartRemoveView.as_view(),
        name="remove",
    ),
    path(
        "ajax/<str:app_label>/<str:model_name>/<int:object_id>/",
        CartUpdateAjaxView.as_view(),
        name="ajax_update",
    ),
]
