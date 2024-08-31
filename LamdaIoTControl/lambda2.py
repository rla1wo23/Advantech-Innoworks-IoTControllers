import json
import os
from tuya_connector import TuyaOpenAPI
import sys

sys.path.append('/opt/python')

ACCESS_ID = os.environ['ACCESS_ID']
ACCESS_KEY = os.environ['ACCESS_KEY']
ENDPOINT = os.environ['ENDPOINT']
DEVICE_CNT = 4
DEVICE_ID = [
    os.environ['DEVICE_ID1'],
    os.environ['DEVICE_ID2'],
    os.environ['DEVICE_ID3'],
    os.environ['DEVICE_ID4']
]
IOT_ID = [1, 2, 3, 4]

def lambda_handler(event, context):
    openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
    openapi.connect()

    def get_device_status(device_id):
        response = openapi.get(f'/v1.0/devices/{device_id}/status')
        if response['success']:
            for status in response['result']:
                if status['code'] == 'switch_1':
                    return status['value']
        return None

    current_status = []
    for i in range(DEVICE_CNT):
        tmp = 'on' if get_device_status(DEVICE_ID[i]) else 'off'
        current_status.append(tmp)

    response = []
    for i in range(DEVICE_CNT):
        response.append({
            'id': IOT_ID[i],
            'status': current_status[i]
        })

    return response