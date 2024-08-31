from miio import FanMiot
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 IP 주소와 토큰을 가져옴
ip_address = os.getenv('IP_ADDRESS')
token = os.getenv('TOKEN')

# 팬 초기화
fan = FanMiot(ip_address, token, model="dmaker.fan.p33")

def turn_off():
    fan.off()

def turn_on():
    fan.on()

def set_speed(speed: int):
    if 1 <= speed <= 100:
        fan.set_speed(speed)

print(fan.status().is_on)

if __name__ == '__main__':
    turn_off()
