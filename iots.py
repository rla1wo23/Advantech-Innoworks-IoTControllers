import os
from tuya_connector import TuyaOpenAPI, TuyaOpenPulsar, TuyaCloudPulsarTopic

# 환경변수에서 Tuya Cloud 프로젝트 설정 정보 가져오기
ACCESS_ID = os.getenv('ACCESS_ID')
ACCESS_KEY = os.getenv('ACCESS_KEY')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DEVICE_ID = os.getenv('DEVICE_ID')
ENDPOINT = os.getenv('ENDPOINT', "https://openapi.tuyaus.com")  # 기본값 설정
MQ_ENDPOINT = os.getenv('MQ_ENDPOINT', "wss://mqe.tuyaus.com:8285/")  # 기본값 설정

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()
open_pulsar = TuyaOpenPulsar(ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.PROD)

# 메시지 리스너 추가
open_pulsar.add_message_listener(lambda msg: print(f"Received message: {msg}"))

# 메시지 큐 시작
open_pulsar.start()

# 장치 상태 조회 함수
def get_device_status(device_id):
    response = openapi.get(f'/v1.0/devices/{device_id}/status')
    if response['success']:
        for status in response['result']:
            if status['code'] == 'switch_1':
                return status['value']
    return None

# 스마트 플러그 제어 함수
def control_smart_plug(device_id, status):
    commands = [{'code': 'switch_1', 'value': status}]
    response = openapi.post(f'/v1.0/devices/{device_id}/commands', {'commands': commands})
    return response

# 현재 상태를 확인하고 스마트 플러그를 토글
current_status = get_device_status(DEVICE_ID)
if current_status is not None:
    new_status = not current_status
    response = control_smart_plug(DEVICE_ID, new_status)
    print(f'Smart Plug Toggled: {response}')
else:
    print('Failed to get the current status of the device')

# 메시지 큐 중지
open_pulsar.stop()
