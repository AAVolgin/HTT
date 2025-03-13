
from onvif import ONVIFCamera
import time
from lxml import etree

def parse_event(event):
    try:
        message = event.Message['_value_1']
        
        # Преобразуем XML в объект lxml
        xml_tree = etree.ElementTree(message)

        # Достаём нужные данные
        utc_time = message.attrib.get("UtcTime", "Unknown Time")
        operation = message.attrib.get("PropertyOperation", "Unknown Operation")

        is_motion = xml_tree.find(".//{http://www.onvif.org/ver10/schema}SimpleItem[@Name='IsMotion']")
        is_motion_value = is_motion.attrib["Value"] if is_motion is not None else "Unknown"

        rule = xml_tree.find(".//{http://www.onvif.org/ver10/schema}SimpleItem[@Name='Rule']")
        rule_name = rule.attrib["Value"] if rule is not None else "Unknown"

        # Выводим данные
        print(f"\n🕒 Время события: {utc_time}")
        print(f"🔄 Тип операции: {operation}")
        print(f"📜 Правило: {rule_name}")
        print(f"🚨 Движение: {is_motion_value}")

        # Если движение зафиксировано, реагируем
        if is_motion_value.lower() == "true":
            print("‼️ Движение обнаружено! 🚀")

    except Exception as e:
        print("Ошибка парсинга события:", e)

camera = ONVIFCamera('192.168.2.70', 80, 'admin', '12345', '/home/mumrik/python-onvif-zeep/wsdl')

events_service = camera.create_events_service()
subscription = events_service.CreatePullPointSubscription()
pullpoint_service = camera.create_pullpoint_service(subscription.SubscriptionReference.Address)

print("Ожидание событий...")

while True:
    try:
        response = pullpoint_service.PullMessages({'Timeout': 5, 'MessageLimit': 10})
        for msg in response.NotificationMessage:
            parse_event(msg)  # Расшифровка события
    except Exception as e:
        print("Ошибка получения событий:", e)
