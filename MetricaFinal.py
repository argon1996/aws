import json
import boto3
from datetime import datetime

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PedidosEntregados')

def lambda_handler(event, context):
    try:
        # Escanear la tabla de pedidos
        response = table.scan()
        pedidos = response['Items']

        # Diccionario para almacenar los tiempos totales y conteos de repartidores
        tiempos_repartidores = {}

        # Calcular el tiempo promedio de entrega por repartidor
        for pedido in pedidos:
            if 'tiempo_asignacion' not in pedido or 'timestamp' not in pedido:
                continue  # Omitir si falta algún campo

            try:
                tiempo_asignacion = datetime.fromisoformat(pedido['tiempo_asignacion'])
                timestamp_entrega = datetime.fromisoformat(pedido['timestamp'])
            except ValueError:
                continue  # Omitir si hay un error en el formato de fecha

            repartidor = pedido['repartidor'].get('Nombre', 'Desconocido')
            tiempo_entrega = (timestamp_entrega - tiempo_asignacion).total_seconds() / 60

            if repartidor not in tiempos_repartidores:
                tiempos_repartidores[repartidor] = {'tiempo_total': 0, 'pedidos': 0}

            tiempos_repartidores[repartidor]['tiempo_total'] += tiempo_entrega
            tiempos_repartidores[repartidor]['pedidos'] += 1

        # Calcular el tiempo promedio por repartidor
        tiempos_promedio = {
            repartidor: tiempos_repartidores[repartidor]['tiempo_total'] / tiempos_repartidores[repartidor]['pedidos']
            for repartidor in tiempos_repartidores
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(tiempos_promedio)
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
                'message': 'Error al calcular tiempo promedio de entrega',
                'error': str(e)
            })
        }
