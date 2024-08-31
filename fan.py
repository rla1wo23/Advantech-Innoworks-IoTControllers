from miio import FanMiot
from flask import Flask, jsonify, request

ip_address = "165.246.116.10"
token = "a80dfeec0ae0e44949598a67bc443ab4"

fan = FanMiot(ip_address, token, model="dmaker.fan.p33")

def turn_off():
        fan.off()
def turn_on():
    fan.on()

def set_speed(speed: int):
    if 1 <= speed <= 100:
        fan.set_speed(speed)

print(fan.status().is_on)
app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    if request.method == 'GET':
        stat = "on" if fan.status().is_on == True else "off"
    return jsonify(id=5 ,status=stat)
@app.route('/control', methods=['GET'])
def control():
    if request.method == 'GET':
        if fan.status().is_on == True:
            fan.off()
        else:
            fan.on()
        stat = "on" if fan.status().is_on == True else "off"
        return jsonify(id=5 ,status=stat)
    
@app.route('/wind/<strength>', methods=['GET'])
def wind(strength):
    if request.method == 'GET':
        if fan.status().is_on == True:
            set_speed(int(strength))
            # stat = "on" if fan.status().is_on == True else "off"
            sp = fan.status().speed
            return jsonify(speed=sp)
        return jsonify(speed=0)

@app.route('/wind', methods=['GET'])
def get_wind():
    if request.method == 'GET':
        if fan.status().is_on == True:
            # stat = "on" if fan.status().is_on == True else "off"
            sp = fan.status().speed
            return jsonify(speed=sp)
        return jsonify(speed=0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)