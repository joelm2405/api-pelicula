import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Inicialización de recursos
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["TABLE_NAME"])
    
    # Intento de proceso principal
    try:
        # Extracción de datos del evento
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        uuidv4 = str(uuid.uuid4())

        # Creación del item de la película
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        # Inserción en DynamoDB
        response = table.put_item(Item=pelicula)

        # Log INFO para ejecución exitosa
        log_info = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada exitosamente",
                "pelicula": pelicula,
                "response": response
            }
        }
        print(json.dumps(log_info))

        # Respuesta exitosa
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log ERROR para errores
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear película",
                "error": str(e),
                "event": event
            }
        }
        print(json.dumps(log_error))
        
        # Respuesta de error
        return {
            'statusCode': 500,
            'error': str(e)
        }
