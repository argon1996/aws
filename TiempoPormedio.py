import json
import boto3
from datetime import datetime

# Cliente de DynamoDB
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
            # Verificar si el pedido tiene los campos 'tiempo_asignacion' y 'timestamp'
            if 'tiempo_asignacion' not in pedido or 'timestamp' not in pedido:
                print(f"Pedido omitido por falta de campos: {pedido}")
                continue  # Omitir este pedido si falta algún campo

            try:
                # Parsear las fechas en formato ISO
                tiempo_asignacion = datetime.fromisoformat(pedido['tiempo_asignacion'])
                timestamp_entrega = datetime.fromisoformat(pedido['timestamp'])
            except ValueError as ve:
                print(f"Error en el formato de fecha para el pedido {pedido}: {ve}")
                continue  # Omitir si hay error en el formato de fecha

            # Nombre del repartidor (manejo de casos cuando el nombre no está presente)
            repartidor = pedido.get('repartidor', {}).get('Nombre', 'Desconocido')

            # Calcular la diferencia en minutos
            tiempo_entrega = (timestamp_entrega - tiempo_asignacion).total_seconds() / 60

            # Agregar el tiempo de entrega al repartidor correspondiente
            if repartidor not in tiempos_repartidores:
                tiempos_repartidores[repartidor] = {'tiempo_total': 0, 'pedidos': 0}
            
            tiempos_repartidores[repartidor]['tiempo_total'] += tiempo_entrega
            tiempos_repartidores[repartidor]['pedidos'] += 1

            # Imprimir los valores para depuración
            print(f"Repartidor: {repartidor}, Tiempo asignación: {tiempo_asignacion}, Timestamp entrega: {timestamp_entrega}, Tiempo entrega: {tiempo_entrega}")

        # Calcular el tiempo promedio
        tiempos_promedio = {repartidor: tiempos_repartidores[repartidor]['tiempo_total'] / tiempos_repartidores[repartidor]['pedidos']
                            for repartidor in tiempos_repartidores}

        # Devolver el resultado con los encabezados CORS
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Puedes restringirlo a tu dominio si lo prefieres
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(tiempos_promedio)
        }

    except Exception as e:
        # Registrar el error en los logs
        print(f"Error al calcular tiempo promedio: {e}")

        # Devolver un error con los encabezados CORS
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Puedes restringirlo a tu dominio si lo prefieres
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'Error al calcular tiempo promedio de entrega',
                'error': str(e)
            })
        }
