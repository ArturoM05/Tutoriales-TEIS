from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Inventario, Libro
from tienda_app.services import CompraService

from .serializers import LibroSerializer, OrdenInputSerializer


class InventarioAPIView(APIView):
    """
    GET /api/v1/inventario/
    La otra 'puerta': devuelve el mismo stock que ve la vista HTML.
    """

    def get(self, request):
        libros = Libro.objects.prefetch_related('inventario').all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)


class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/v1/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}
    """

    def post(self, request):
        # 1. Validacion de datos de entrada ( Adapter )
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            # 2. Inyeccion de Dependencias ( Factory )
            gateway = PaymentFactory.get_processor()
            # 3. Ejecucion de Logica de Negocio ( Service Layer )
            servicio = CompraService(procesador_pago=gateway)
            usuario = request.user if request.user.is_authenticated else None
            # Noten como el servicio NO cambia , solo cambia quien lo llama 
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                cantidad=datos.get('cantidad', 1),
                direccion=datos['direccion_envio'],
                usuario=usuario, 
            )

            return Response(
                {
                    'estado': 'exito',
                    'mensaje': f'Orden creada. Total: {resultado}',
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            # Errores de negocio ( ej : Sin stock )
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception:
            # Errores inesperados
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
