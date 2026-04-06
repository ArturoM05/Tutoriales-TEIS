from decimal import Decimal
from tienda_app.models import Orden
 
class OrdenBuilder :
    def __init__ ( self ) :
        self . reset ()

    def reset ( self ) :
        self._usuario = None
        self._items = []
        self._direccion = " "
        self._cantidad = 1
    
    def con_usuario ( self , usuario ) :
        self._usuario = usuario
        return self # Permite Fluent Interface

    def con_productos ( self , productos ) :
        self._items = productos
        return self
    def para_envio ( self , direccion ) :
        self._direccion = direccion
        return self
    def con_cantidad ( self , cantidad ) :
        self._cantidad = cantidad
        return self
    
    def build ( self ) -> Orden :
        # if not self._usuario or not self._items :
        if not self._items :
            raise ValueError ( " Datos insuficientes para crear la orden . " )
        # Encapsulamos la logica de calculo
        subtotal = sum ( p . precio for p in self._items ) * self._cantidad
        total_con_iva = subtotal * Decimal("1.19")

        orden = Orden.objects.create(
            usuario = self._usuario ,
            libro = self._items[0] ,
            total = total_con_iva ,
            direccion_envio = self._direccion
        )
        self.reset()
        return orden