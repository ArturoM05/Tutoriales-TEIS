from django.shortcuts import render
from django.views import View
from .infra.factories import PaymentFactory
from .models import Inventario
from .services import CompraService, CompraRapidaService


class CompraView(View):
    """
    CBV: Vista Basada en Clases.
    Actúa como un "Portero": recibe la petición y delega al servicio.
    """

    template_name = 'tienda_app/compra.html'

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(
                request,
                self.template_name,
                {
                    'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                    'total': total,
                },
            )
        except (ValueError, Exception) as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)


class CompraRapidaView ( View ) :
 template_name = 'tienda_app/compra_rapida.html'

 def setup_service(self):
     gateway = PaymentFactory.get_processor()
     return CompraRapidaService(procesador_pago=gateway)

 def get ( self , request , libro_id ) :
    servicio = self.setup_service()
    contexto = servicio.obtener_detalle_producto(libro_id)
    return render ( request , self.template_name , contexto )

 def post ( self , request , libro_id ) :
    servicio = self.setup_service()
    try:
        total = servicio.ejecutar_compra_rapida(libro_id)
        if total is not None:
            return render(
                request,
                self.template_name,
                {
                    'mensaje_exito': f"¡Gracias por su compra rápida! Total: ${total}",
                    'total': total,
                },
            )
        else:
            return render(request, self.template_name, {'error': "La transacción fue rechazada por el banco."}, status=400)
    except (ValueError, Exception) as e:
        return render(request, self.template_name, {'error': str(e)}, status=400)


class InventarioView(View):
    """
    Vista HTML del inventario.
    Una de las dos 'puertas' que muestran el estado del stock.
    """
    template_name = 'tienda_app/inventario.html'

    def get(self, request):
        inventario = Inventario.objects.select_related('libro').all()
        return render(request, self.template_name, {'inventario': inventario})