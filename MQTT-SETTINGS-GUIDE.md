# MQTT Settings Panel Guide

## 📌 Overview

MQTT Settings Panel ช่วยให้คุณสามารถกำหนดค่า MQTT Broker และ Topics ได้อย่างสะดวกผ่าน Django Admin UI โดยไม่ต้องแก้ไขโค้ดหรือไฟล์ settings.py

## 🚀 Quick Start

### 1. เข้าถึง MQTT Settings Panel

1. เข้าสู่ Django Admin: `http://127.0.0.1:8000/admin/`
2. ในเมนู **MYAPP** คลิก **MQTT Settings**
3. ระบบจะแสดงหน้าการตั้งค่า MQTT

### 2. กำหนดค่า Broker (🌐 Broker Configuration)

ส่วนนี้ใช้สำหรับตั้งค่าการเชื่อมต่อกับ MQTT Broker

| ฟิลด์ | คำอธิบาย | ค่าเริ่มต้น |
|-------|---------|------------|
| **Broker** | hostname หรือ IP address ของ MQTT Broker | `broker.hivemq.com` |
| **Port** | พอร์ตที่ใช้เชื่อมต่อ (1883 สำหรับ TCP, 8883 สำหรับ SSL) | `1883` |
| **Username** | ชื่อผู้ใช้สำหรับ authentication (ถ้ามี) | *(ว่าง)* |
| **Password** | รหัสผ่านสำหรับ authentication (ถ้ามี) | *(ว่าง)* |

**ตัวอย่าง:**
```
Broker: broker.hivemq.com
Port: 1883
Username: (leave empty for public broker)
Password: (leave empty for public broker)
```

### 3. กำหนด Topics (📡 Topic Configuration)

ส่วนนี้ใช้สำหรับตั้งค่า Topic patterns สำหรับการรับส่งข้อมูล

| ฟิลด์ | คำอธิบาย | ค่าเริ่มต้น |
|-------|---------|------------|
| **Telemetry Topic** | Topic สำหรับรับข้อมูล telemetry จากอุปกรณ์ | `smartfarm/+/telemetry` |
| **Status Topic** | Topic สำหรับรับสถานะจากอุปกรณ์ | `smartfarm/+/status` |
| **Control Topic Pattern** | Pattern สำหรับส่งคำสั่งควบคุมไปยังอุปกรณ์ | `smartfarm/{board_id}/control` |

**การใช้ Wildcards:**
- `+` (single-level wildcard) = จับคู่กับ 1 ระดับไดที่แก่-ก็ได้
  - ตัวอย่าง: `smartfarm/+/telemetry` จะจับคู่กับ:
    - `smartfarm/ESP32-001/telemetry` ✅
    - `smartfarm/ESP32-002/telemetry` ✅
    - `smartfarm/device1/telemetry` ✅
    - `smartfarm/a/b/telemetry` ❌ (มากกว่า 1 ระดับ)

- `#` (multi-level wildcard) = จับคู่กับหลายระดับ
  - ตัวอย่าง: `smartfarm/#` จะจับคู่กับ:
    - `smartfarm/ESP32-001/telemetry` ✅
    - `smartfarm/ESP32-001/status` ✅
    - `smartfarm/a/b/c/d` ✅

**Control Topic Pattern:**
- ใช้ `{board_id}` เป็น placeholder ที่จะถูกแทนที่ด้วย board_id ของอุปกรณ์จริง
- ตัวอย่าง: `smartfarm/{board_id}/control`
  - เมื่อส่งคำสั่งไปยัง `ESP32-001` จะกลายเป็น `smartfarm/ESP32-001/control`

### 4. Advanced Settings (⚙️ Advanced Settings)

| ฟิลด์ | คำอธิบาย | ค่าเริ่มต้น |
|-------|---------|------------|
| **Keepalive** | ระยะเวลา keepalive ในหน่วยวินาที | `60` |
| **QoS** | Quality of Service level | `QoS 0` |

**QoS Levels:**
- **QoS 0 - At most once:** เร็วที่สุดแต่อาจสูญหายได้ ✅ *แนะนำสำหรับข้อมูล telemetry*
- **QoS 1 - At least once:** รับประกันการส่งถึง แต่อาจซ้ำได้
- **QoS 2 - Exactly once:** ช้าที่สุดแต่ไม่มีการซ้ำ

## ⚠️ สิ่งที่ต้องทราบ

### 1. การ Restart Server

**สำคัญ:** เมื่อเปลี่ยนการตั้งค่า MQTT Settings แล้ว ต้อง **restart Django server** เพื่อให้การเปลี่ยนแปลงมีผล

```powershell
# หยุด server ด้วย Ctrl+C ในหน้า terminal

# จากนั้นรันใหม่
python manage.py run_mqtt_worker
```

หลังจาก save การตั้งค่า ระบบจะแสดงข้อความแจ้งเตือน:

```
⚠️ MQTT Settings updated successfully. 
Please restart Django server for changes to take effect.
Stop the server with Ctrl+C and run: python manage.py run_mqtt_worker
```

### 2. Singleton Pattern

- ระบบอนุญาตให้มีการตั้งค่าเพียง **1 record เท่านั้น**
- ไม่สามารถเพิ่มหรือลบ settings record ได้
- แก้ไขค่าได้เท่านั้น

### 3. Default Values

เมื่อเข้าถึง MQTT Settings ครั้งแรก ระบบจะสร้างค่าเริ่มต้นอัตโนมัติ:

```python
Broker: broker.hivemq.com
Port: 1883
Telemetry Topic: smartfarm/+/telemetry
Status Topic: smartfarm/+/status
Control Topic Pattern: smartfarm/{board_id}/control
Keepalive: 60 seconds
QoS: 0 (At most once)
```

## 🔧 Use Cases

### Use Case 1: เปลี่ยน MQTT Broker

**สถานการณ์:** ต้องการเปลี่ยนจาก public broker ไป private broker

1. เข้า MQTT Settings
2. เปลี่ยน Broker เป็น `mqtt.yourcompany.com`
3. เปลี่ยน Port เป็น `1883` (หรือ `8883` สำหรับ SSL)
4. ใส่ Username และ Password (ถ้าจำเป็น)
5. คลิก **SAVE**
6. Restart Django server

### Use Case 2: แยก Environment (Development/Production)

**Development:**
```
Broker: test.mosquitto.org
Port: 1883
Telemetry Topic: dev/smartfarm/+/telemetry
Control Topic Pattern: dev/smartfarm/{board_id}/control
```

**Production:**
```
Broker: broker.hivemq.com
Port: 1883
Telemetry Topic: prod/smartfarm/+/telemetry
Control Topic Pattern: prod/smartfarm/{board_id}/control
```

### Use Case 3: เพิ่ม Namespace/Prefix

**สถานการณ์:** ต้องการแยก topics ของ project ต่างๆ บน broker เดียวกัน

```
Telemetry Topic: project1/smartfarm/+/telemetry
Status Topic: project1/smartfarm/+/status
Control Topic Pattern: project1/smartfarm/{board_id}/control
```

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│         Django Admin UI                 │
│  http://localhost:8000/admin/           │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │    MQTT Settings Panel            │ │
│  │  • Broker: broker.hivemq.com      │ │
│  │  • Port: 1883                     │ │
│  │  • Topics: smartfarm/+/...        │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
                 │
                 │ Save Changes
                 ▼
┌─────────────────────────────────────────┐
│         MQTTSettings Model              │
│         (Database Table)                │
│  • Singleton pattern (pk=1)             │
│  • get_settings() classmethod           │
└─────────────────────────────────────────┘
                 │
                 │ Read on Startup
                 ▼
┌─────────────────────────────────────────┐
│         MQTTHandler                     │
│  (mqtt_handler.py)                      │
│                                         │
│  def __init__(self):                    │
│      settings = MQTTSettings.get_settings() │
│      self.client.connect(                │
│          settings.broker,                │
│          settings.port                   │
│      )                                   │
└─────────────────────────────────────────┘
                 │
                 │ MQTT Protocol
                 ▼
┌─────────────────────────────────────────┐
│         MQTT Broker                     │
│  (broker.hivemq.com:1883)               │
└─────────────────────────────────────────┘
                 │
                 │ Subscribe/Publish
                 ▼
┌─────────────────────────────────────────┐
│         ESP32 Devices                   │
│  • ESP32-FARM-001                       │
│  • ESP32-FARM-002                       │
│  • ...                                  │
└─────────────────────────────────────────┘
```

## 🧪 Testing

### 1. ทดสอบการเชื่อมต่อ Broker

หลังจากบันทึกการตั้งค่าและ restart server แล้ว ตรวจสอบ log:

```
INFO mqtt_handler Connecting to MQTT broker at broker.hivemq.com:1883
INFO mqtt_handler Connected to MQTT broker successfully
INFO mqtt_handler Subscribed to topics: smartfarm/+/telemetry, smartfarm/+/status (QoS 0)
```

### 2. ทดสอบการรับข้อมูล

ใช้ MQTT client tool (เช่น MQTTX, mosquitto_pub) เพื่อส่งข้อความทดสอบ:

```bash
mosquitto_pub -h broker.hivemq.com -t "smartfarm/TEST-001/telemetry" -m '{"water_temp": 25.5}'
```

### 3. ทดสอบการส่งคำสั่ง

1. เข้า Relay Test Panel: `http://127.0.0.1:8000/admin/myapp/relay-control/`
2. เลือก board_id ที่ต้องการ
3. คลิกปุ่มควบคุม relay
4. ตรวจสอบ log:

```
INFO mqtt_handler Publishing to smartfarm/ESP32-001/control: {'command': 'relay_control', 'relays': {...}}
```

## 🔒 Security Best Practices

1. **ใช้ Username/Password:** สำหรับ production environment
2. **ใช้ SSL/TLS:** เปลี่ยน port เป็น 8883 และใช้ broker ที่รองรับ SSL
3. **จำกัด Topic Access:** ใช้ ACL (Access Control List) บน broker เพื่อจำกัด permissions
4. **เก็บรหัสผ่านอย่างปลอดภัย:** ใน production ควรใช้ environment variables แทนการเก็บใน database

## 📝 Changelog

- **2026-04-05:** สร้าง MQTT Settings Panel พร้อม Dynamic Configuration
- เพิ่ม MQTTSettings model (Singleton pattern)
- เพิ่ม MQTTSettingsAdmin UI
- อัปเดต mqtt_handler.py ให้อ่านค่าจากฐานข้อมูล
- เพิ่ม help text และ descriptions สำหรับทุกฟิลด์

## 🆘 Troubleshooting

### ปัญหา: การเปลี่ยนแปลงไม่มีผล

**วิธีแก้:** Restart Django server

```powershell
# Stop server
Ctrl+C

# Start again
python manage.py run_mqtt_worker
```

### ปัญหา: ไม่สามารถเชื่อมต่อ Broker

**ตรวจสอบ:**
1. Broker hostname/IP ถูกต้องหรือไม่
2. Port ถูกต้องหรือไม่ (1883 for TCP, 8883 for SSL)
3. Firewall อนุญาตการเชื่อมต่อหรือไม่
4. Username/Password ถูกต้องหรือไม่ (ถ้าจำเป็น)

### ปัญหา: ไม่ได้รับข้อความจากอุปกรณ์

**ตรวจสอบ:**
1. Topic pattern ถูกต้องหรือไม่
2. อุปกรณ์ publish ไปยัง topic ที่ตรงกับ pattern หรือไม่
3. QoS level เหมาะสมหรือไม่

**ตัวอย่าง:**
- ถ้าอุปกรณ์ส่งไปยัง `smartfarm/device1/data`
- แต่ Telemetry Topic ตั้งเป็น `smartfarm/+/telemetry`
- จะไม่ได้รับข้อความ ❌

**แก้ไข:** เปลี่ยน Telemetry Topic เป็น `smartfarm/+/#` หรือ `smartfarm/+/data`

---

**เอกสารนี้อัปเดตล่าสุด:** 5 เมษายน 2026
