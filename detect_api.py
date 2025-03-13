import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPDigestAuth
import re
import json
import xmltodict

# Настройки камеры
IP = "192.168.2.70"  # IP камеры
USER = "admin"        # Логин
PASS = "12345"        # Пароль

# URL потока событий ISAPI
URL = f"http://{IP}/ISAPI/Event/notification/alertStream"

def xml_to_json(xml_data):
    """Преобразует XML в JSON"""
    try:
        json_data = xmltodict.parse(xml_data)
        return json.dumps(json_data, indent=4, ensure_ascii=False)
    except Exception as e:
        print("❌ Ошибка конвертации XML в JSON:", e)
        return None

def extract_xml(raw_data):
    """Извлекает только XML из потока, удаляя заголовки"""
    match = re.search(r"<EventNotificationAlert.*?</EventNotificationAlert>", raw_data, re.S)
    return match.group(0) if match else None

def parse_motion_event(xml_data):
    """Парсит XML и ищет события движения"""
    try:
        root = ET.fromstring(xml_data)

        ns = {"hik": "http://www.hikvision.com/ver20/XMLSchema"}  # Пространство имён Hikvision
        event_type = root.find(".//hik:eventType", ns)
        event_state = root.find(".//hik:eventState", ns)

        if event_type is not None and event_state is not None:
            if event_type.text == "VMD" and event_state.text == "active":
                print("‼️ Движение обнаружено!")
            else:
                print(f"ℹ️ Другое событие: {event_type.text}, состояние: {event_state.text}")
    except ET.ParseError as e:
        print("❌ Ошибка парсинга XML:", e)

# Подключаемся к потоку событий
with requests.get(URL, auth=HTTPDigestAuth(USER, PASS), stream=True) as response:
    buffer = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode()
            buffer += decoded_line

            if "</EventNotificationAlert>" in buffer:  
                cleaned_xml = extract_xml(buffer)
                if cleaned_xml:
                    json_output = xml_to_json(cleaned_xml)
                    print(json_output)
                    #print("🔹 Очищенный XML:", cleaned_xml)  # Для отладки
                    parse_motion_event(cleaned_xml)
                else:
                    print("❌ XML не найден в потоке данных!")

                buffer = ""  # Очищаем буфер после обработки
