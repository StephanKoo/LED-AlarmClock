
import requests
import json
from requests.structures import CaseInsensitiveDict
import time
from datetime import datetime
import socket

def getIpInfo():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.168.0.1', 1))
        ipAddress = s.getsockname()[0]
        return 'IP: ' + ipAddress;
        # TODO auch prüfen, ob erreichbar, sonst ausgeben, dass nicht erreichbar
    except Exception:
        return None
        # Fehlermeldung verarbeiten
    finally:
        s.close()

def ReadYrTemp(lat, lon):
    #with open("/home/pi/Python/YrData.txt", "r") as yrdata:
    #    yrd = yrdata.read()
    #jdata = json.loads(yrd)

    try:
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["User-agent"] = "My User Agent 1.0"
    
        url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat="+lat+"&lon="+lon+""
        resp = requests.get(url, headers=headers)
        #print(resp.text)
        jdata = json.loads(resp.text)
        
        maxTemp = -100
        minTemp = 100
    
        for i in range(0, 18):
            thisTemp = jdata['properties']['timeseries'][i]['data']['instant']['details']['air_temperature']
            
            if i == 0:
                curTemp = thisTemp
                
            if thisTemp > maxTemp:
                maxTemp = thisTemp
            
            if thisTemp < minTemp:
                minTemp = thisTemp
        return "Wetter: " + str(round(minTemp)) + "-" + str(round(maxTemp)) + " C"
    except:
        return None;

#lat = 0.000000
#lng = 9.999999
#type = rise or set
def getSunData(lat, lng, type):
    url = "https://api.sunrise-sunset.org/json?lat="+str(lat)+"&lng="+str(lng)+"&date=today&formatted=0"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["User-agent"] = "My User Agent 1.0"
    resp = requests.get(url, headers=headers)
    jdata = json.loads(resp.text)
    res = ""
    
    if type == "rise" :
        res = jdata['results']['sunrise']
        res = res[0:19]
    elif type == "set":
        res = jdata['results']['sunset']
        res = res[0:19]
    #print(res)
    
    if res == "":
        return ""
    else:
        return datetime_from_utc_to_local(res)

def datetime_from_utc_to_local(utc_datetime):
    utc_datetime = datetime.strptime(utc_datetime, "%Y-%m-%dT%H:%M:%S")
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def isDayTime(sunrise, sunset):
    hour = datetime.now().strftime('%h')
    
    #if hour <= sunrise.strftime('%h') or hour >= sunset.strftime('%h'):
    #    return False
    #else:
    #    return True
    return True

def CPUTemp():
    try:
        import gpiozero as gz
        cpu_temp = gz.CPUTemperature().temperature
        return str(round(cpu_temp, 1))
    except:
        return "??"
