from django.urls import path

from orders.views import OrderCreateView, CanceledTemplateView, SuccessTemplateView, OrderListView, OrderDetailView

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="orders_list"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order"),
    path("order-create/", OrderCreateView.as_view(), name="order_create"),
    path("order-canceled/", CanceledTemplateView.as_view(), name="order_canceled"),
    path("order-success/", SuccessTemplateView.as_view(), name="order_success"),
    path("order-success/", SuccessTemplateView.as_view(), name="order_success"),
]
