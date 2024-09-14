import json
import boto3
import datetime
import uuid
from decimal import Decimal
import logging

# Configurar el logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PedidosEntregados')

def lambda_handler(event, context):
    try:
        # Registrar el evento completo para depuración
        logger.info(f"Evento recibido completo: {json.dumps(event)}")
        
        # Verificar si el cuerpo de la solicitud está presente y forzar el parseo
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({"message": "Cuerpo de la solicitud no proporcionado"})
            }
        
        # Parsear el cuerpo de la solicitud, asumiendo que es un JSON
        body = json.loads(event['body'])
        
        # Generar un UUID para el pedido
        pedido_id = str(uuid.uuid4())
        
        # Obtener datos del repartidor y productos
        repartidor = body['repartidor']
        productos = body['productos']

        # Convertir precios a Decimal
        for producto in productos:
            producto['Precio'] = Decimal(str(producto['Precio']))

        # Obtener el timestamp actual
        timestamp = str(datetime.datetime.now())
        
        # Guardar los datos en DynamoDB
        table.put_item(
            Item={
                'pedido_id': pedido_id,
                'repartidor': repartidor,
                'productos': productos,
                'timestamp': timestamp
            }
        )

        # Registro de éxito
        logger.info(f"Pedido registrado exitosamente: {pedido_id}")
        
        # Respuesta de éxito con los encabezados CORS
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'Pedido registrado exitosamente',
                'pedido_id': pedido_id
            })
        }
    except Exception as e:
        # Manejo de errores con encabezados CORS
        logger.error(f"Error al registrar el pedido: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'Error al registrar el pedido',
                'error': str(e)
            })
        }
