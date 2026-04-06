from django.urls import path
from .api.views import CompraAPIView, InventarioAPIView
from .views import CompraView, CompraRapidaView, InventarioView

urlpatterns = [
    # Puerta HTML
    path('inventario/', InventarioView.as_view(), name='inventario'),
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    path('compra_rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='finalizar_compra_rapida'),
    # Puerta API
    path('api/v1/inventario/', InventarioAPIView.as_view(), name='api_inventario'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]