import json
import os
from tuya_connector import TuyaOpenAPI

ACCESS_ID = os.environ['ACCESS_ID']
ACCESS_KEY = os.environ['ACCESS_KEY']
ENDPOINT = os.environ['ENDPOINT']

def lambda_handler(event, context):
    try:
        message = event if isinstance(event, dict) else json.loads(event['body'])
    except (json.JSONDecodeError, KeyError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input'})
        }

    id_value = message.get('id')
    desired_status = message.get('status').lower()

    if str(id_value) == "1":
        DEVICE_ID = os.environ['DEVICE_ID1']
    elif str(id_value) == "2":
        DEVICE_ID = os.environ['DEVICE_ID2']
    elif str(id_value) == "3":
        DEVICE_ID = os.environ['DEVICE_ID3']
    elif str(id_value) == "4":
        DEVICE_ID = os.environ['DEVICE_ID4']
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Unsupported id value'})
        }
    
    openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
    openapi.connect()

    def get_device_status(device_id):
        response = openapi.get(f'/v1.0/devices/{device_id}/status')
        if response['success']:
            for status in response['result']:
                if status['code'] == 'switch_1':
                    return status['value']
        return None

    def control_smart_plug(device_id, status):
        commands = [{'code': 'switch_1', 'value': status}]
        response = openapi.post(f'/v1.0/devices/{device_id}/commands', {'commands': commands})
        return response

    current_status = get_device_status(DEVICE_ID)
    
    if current_status is not None:
        if (current_status and desired_status == 'on') or (not current_status and desired_status == 'off'):
            final_status = 'on' if current_status else 'off'
        else:
            new_status = (desired_status == 'on')
            control_smart_plug(DEVICE_ID, new_status)
            final_status = 'on' if new_status else 'off'
        return {
            'id': id_value,
            'status': final_status
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to get the current status of the device'})
        }
