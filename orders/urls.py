from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create_view, name="order_create"),
    path("<int:order_id>/", views.order_detail_view, name="order_detail"),
    path("history/", views.order_history_view, name="order_history"),
    path("reorder/<int:order_id>/", views.order_reorder_view, name="reorder"),
    path("return/<int:order_id>/", views.return_products, name="order_return"),
    path(
        "return/submit/<int:order_id>/",
        views.submit_return_request,
        name="order_return_submit",
    ),
]
