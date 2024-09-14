import boto3
import json
from decimal import Decimal

# Cliente DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PedidosEntregados')

# Función personalizada para convertir Decimal a float
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convierte Decimal a float para JSON
    raise TypeError

def lambda_handler(event, context):
    try:
        # Obtener todas las entregas de la tabla
        response = table.scan()
        items = response['Items']

        # Inicializar el diccionario para contar productos
        productos_mas_vendidos = {}

        # Iterar sobre cada pedido
        for item in items:
            productos = item.get('productos', [])
            for producto in productos:
                # Verificar si el nombre del producto está en 'Producto' o 'producto'
                nombre_producto = producto.get('Producto') or producto.get('producto')
                cantidad = producto.get('Cantidad', 1)  # Asumimos 1 si no hay campo de cantidad

                if not nombre_producto:
                    print("Producto no encontrado en el pedido:", producto)
                    continue  # Saltar si no se encuentra un nombre de producto

                if nombre_producto not in productos_mas_vendidos:
                    productos_mas_vendidos[nombre_producto] = 0

                productos_mas_vendidos[nombre_producto] += cantidad

        # Devolver el resultado con los valores Decimales convertidos
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(productos_mas_vendidos, default=decimal_default)  # Aquí usamos la función para manejar Decimals
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'Error al calcular productos más vendidos',
                'error': str(e)
            })
        }
