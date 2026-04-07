# N8N Relay Control Test Guide (Latest)

เอกสารนี้สรุปขั้นตอนทดสอบ N8N integration กับ Django API ครบทั้งระบบ

## ภาพรวม N8N Integration

ระบบมีการเชื่อมต่อ 2 ทิศทาง:

### 1. Inbound Webhook (n8n → Django Dashboard)
- n8n สั่งงาน Relay ผ่าน Django API
- Endpoint: `POST /api/n8n/relay-control/`
- ต้องการ authentication ด้วย `X-N8N-Token` header
- Dashboard จะส่งคำสั่งไปยัง ESP32 ผ่าน MQTT

### 2. Outbound Webhooks (Django Dashboard → n8n)
- Dashboard ส่ง events ไปยัง n8n Webhook
- **Relay Command Event**: ทุกครั้งที่สั่ง relay จาก Dashboard/Admin
- **Telemetry Event**: ทุกครั้งที่ได้รับข้อมูล sensor จาก ESP32
- **Device Status Event**: เมื่ออุปกรณ์ online/offline
- ไม่ต้องใช้ authentication (แนะนำใช้ HTTPS และ secret path)

---

## PART 1: Inbound Webhook (n8n → Dashboard)

## 1) Endpoint และรูปแบบที่ถูกต้อง

- Base URL: `https://myapp-django-aiots.onrender.com`
- Endpoint: `https://myapp-django-aiots.onrender.com/api/n8n/relay-control/`
- Method: `POST`
- Header ที่ต้องมี:
  - `Content-Type: application/json`
  - `X-N8N-Token: <inbound_auth_token>`

หมายเหตุสำคัญ:
- Endpoint ต้องมี `/` ท้ายเสมอ
- ถ้าไม่มี `/` ท้าย อาจโดน redirect แล้วเกิด `405 Method Not Allowed`

## 2) เตรียมค่าก่อนทดสอบ

1. เข้า Django Admin: `/admin/`
2. ไปที่ `N8N Settings`
3. เปิด `Enable inbound webhook`
4. คัดลอก `Inbound auth token` (ค่า `inbound_auth_token`)
5. เตรียม `board_id` ของอุปกรณ์จริง
   - ตัวอย่างจริง: `ESP32-FARM-001-NATTAPHOL-PALM`

## 3) รูปแบบ Payload ที่รองรับ

### A. Action mode

```json
{
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "action": "pump_on"
}
```

Action ที่รองรับ:
- `all_on`
- `all_off`
- `pump_on`
- `pump_off`
- `fan_on`
- `fan_off`
- `heater_on`
- `heater_off`

### B. Direct relays mode

```json
{
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "relays": {
    "relay1_pump": true,
    "relay2_fan": false,
    "relay3_heater": true
  }
}
```

## 4) cURL สำหรับ Import ใน n8n HTTP Request (ครบทุกแบบ)

ใช้งานใน n8n:
1. สร้าง `HTTP Request` node
2. เลือก `Import cURL`
3. วางคำสั่งด้านล่าง (one-line)
4. เปลี่ยน `YOUR_INBOUND_TOKEN` และ `board_id` ให้เป็นค่าจริง

### 4.1 Template มาตรฐาน (Header token)

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"pump_on\"}"
```

### 4.2 Action mode ครบ 8 คำสั่ง

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"all_on\"}"
```

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"all_off\"}"
```

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"pump_on\"}"
```

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"pump_off\"}"
```

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"fan_on\"}"
```

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"fan_off\"}"
```

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"heater_on\"}"
```

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"heater_off\"}"
```

### 4.3 Direct relays mode (หลายรูปแบบ)

เปิด pump อย่างเดียว

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"relays\":{\"relay1_pump\":true}}"
```

เปิด fan อย่างเดียว

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"relays\":{\"relay2_fan\":true}}"
```

เปิด heater อย่างเดียว

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"relays\":{\"relay3_heater\":true}}"
```

กำหนดครบทุก relay

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/json" -H "X-N8N-Token: YOUR_INBOUND_TOKEN" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"relays\":{\"relay1_pump\":true,\"relay2_fan\":false,\"relay3_heater\":true}}"
```

### 4.4 Fallback auth (เมื่อส่ง Header ไม่สะดวก)

โค้ดฝั่งเซิร์ฟเวอร์รองรับ token ผ่าน query string และ form/body token ด้วย

ผ่าน query string

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/?token=YOUR_INBOUND_TOKEN" -H "Content-Type: application/json" -d "{\"board_id\":\"ESP32-FARM-001-NATTAPHOL-PALM\",\"action\":\"pump_on\"}"
```

ผ่าน form field token

```bash
curl -X POST "https://myapp-django-aiots.onrender.com/api/n8n/relay-control/" -H "Content-Type: application/x-www-form-urlencoded" -d "token=YOUR_INBOUND_TOKEN&board_id=ESP32-FARM-001-NATTAPHOL-PALM&action=pump_on"
```

หมายเหตุ:
- แนะนำให้ใช้ Header `X-N8N-Token` เป็นมาตรฐานหลัก
- ทุกตัวอย่างต้องคง `/` ท้าย endpoint เสมอ

## 5) ตัวอย่างตั้งค่า HTTP Request Node แบบ Manual

- Method: `POST`
- URL: `https://myapp-django-aiots.onrender.com/api/n8n/relay-control/`
- Send Headers: `ON`
  - `Content-Type: application/json`
  - `X-N8N-Token: <inbound_auth_token>`
- Send Body: `ON`
- Body Content Type: `JSON`
- JSON Body:

```json
{
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "action": "pump_on"
}
```

## 6) Expected Response

สำเร็จ (`HTTP 200`):

```json
{
  "success": true,
  "message": "Command sent to ESP32-FARM-001-NATTAPHOL-PALM",
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "action": "pump_on",
  "relays": {
    "relay1_pump": true
  }
}
```

ตัวอย่าง error ที่พบบ่อย:
- `401 Invalid token`
- `403 Inbound webhook is disabled`
- `400 board_id is required`
- `400 Unsupported action: <value>`
- `405 Method Not Allowed` (มักเกิดจาก URL ขาด `/` ท้าย)

## 7) Checklist ทดสอบ

### Inbound Webhook (n8n → Dashboard)

- [ ] เปิด `Enable inbound webhook` แล้ว
- [ ] ใช้ token ล่าสุดจาก Admin
- [ ] URL ลงท้ายด้วย `/api/n8n/relay-control/`
- [ ] Method เป็น `POST`
- [ ] ส่ง `Content-Type: application/json`
- [ ] Payload มี `board_id`
- [ ] `board_id` ตรงกับอุปกรณ์จริงในระบบ

### Outbound Webhook (Dashboard → n8n)

- [ ] สร้าง Webhook node ใน n8n
- [ ] คัดลอก Webhook URL จาก n8n
- [ ] เปิดใช้งาน webhook ที่ต้องการใน Django Admin
- [ ] กรอก Webhook URL ใน Django Admin
- [ ] บันทึกการตั้งค่า
- [ ] ทดสอบกระตุ้น event (เช่น สั่ง relay, รับ telemetry)
- [ ] ตรวจสอบว่า n8n Webhook node ได้รับข้อมูล

---

## PART 2: Outbound Webhooks (Dashboard → n8n)

## 8) Outbound Webhooks: Dashboard → n8n

ระบบสามารถส่งข้อมูลจาก Dashboard ไปยัง n8n Webhooks ได้ 3 ประเภท:

### 8.1) Relay Command Event

ส่งทุกครั้งที่มีการสั่ง Relay จาก Dashboard/Admin

**Payload:**

```json
{
  "event_type": "relay_command",
  "source": "dashboard" | "admin" | "n8n_inbound_webhook",
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "action": "pump_on",
  "success": true,
  "relays": {
    "relay1_pump": true,
    "relay2_fan": false,
    "relay3_heater": false
  },
  "timestamp": "2026-04-07T10:30:00.123456+07:00",
  "metadata": {}
}
```

**การตั้งค่า:**
- เปิดใช้งาน: `Enable outbound webhook`
- URL: `Outbound webhook URL` (n8n webhook URL สำหรับรับ relay command)

### 8.2) Telemetry Event

ส่งข้อมูล sensor และสถานะ relay จากอุปกรณ์ ESP32 ทุกครั้งที่ได้รับผ่าน MQTT

**Payload:**

```json
{
  "event_type": "telemetry",
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "rssi": -65,
  "sensor_data": {
    "water_temp": 28.5,
    "air_temp": 32.1,
    "air_humidity": 75.3,
    "water_overflow": false,
    "water_dry": false
  },
  "relay_status": {
    "relay1_pump": true,
    "relay2_fan": false,
    "relay3_heater": false
  },
  "timestamp": "2026-04-07T10:30:05.789012+07:00",
  "metadata": {}
}
```

**การตั้งค่า:**
- เปิดใช้งาน: `Enable telemetry webhook`
- URL: `Telemetry webhook URL` (n8n webhook URL สำหรับรับ telemetry)

### 8.3) Device Status Event

ส่งสถานะอุปกรณ์เมื่อเปลี่ยนแปลง (online/offline)

**Payload:**

```json
{
  "event_type": "device_status",
  "board_id": "ESP32-FARM-001-NATTAPHOL-PALM",
  "status": "online",
  "ip_address": "192.168.1.100",
  "firmware_version": "1.0.0",
  "last_seen": "2026-04-07T10:30:00.123456+07:00",
  "timestamp": "2026-04-07T10:30:00.500000+07:00",
  "metadata": {}
}
```

**การตั้งค่า:**
- เปิดใช้งาน: `Enable device status webhook`
- URL: `Device status webhook URL` (n8n webhook URL สำหรับรับ status)

### 8.4) ตัวอย่างการตั้งค่า Outbound Webhook ใน Django Admin

1. ไปที่ `/admin/myapp/n8nsettings/`
2. สร้าง webhook ใน n8n (Webhook node)
3. คัดลอก Webhook URL จาก n8n (Test URL หรือ Production URL)
4. เปิดใช้งานแต่ละประเภทตามต้องการ:
   - `Enable outbound webhook` + กรอก `Outbound webhook URL`
   - `Enable telemetry webhook` + กรอก `Telemetry webhook URL`
   - `Enable device status webhook` + กรอก `Device status webhook URL`
5. บันทึกการตั้งค่า

### 8.5) ตัวอย่าง n8n Workflow สำหรับรับ Outbound Events

**Webhook Node Configuration:**
- Method: `POST`
- Path: `/webhook/<custom-path>` (เช่น `/webhook/relay-events`)
- Response Code: `200`
- Response Data: `First entry JSON`

**ตัวอย่าง expression ใน n8n:**

```javascript
// ดึง event_type
{{ $json.event_type }}

// กรอง event ตามประเภท
{{ $json.event_type === "telemetry" }}

// ดึงอุณหภูมิน้ำ
{{ $json.sensor_data.water_temp }}

// ตรวจสอบว่า pump เปิดอยู่หรือไม่
{{ $json.relay_status.relay1_pump === true }}
```

## 9) Security Note

- ห้าม commit token ลง repo
- ถ้า token เคยถูกแชร์ในแชท/หน้าจอ ให้ rotate token ใหม่ทันทีหลังทดสอบ
- Outbound webhooks ไม่ต้องใช้ authentication (ถ้าต้องการความปลอดภัย ควรใช้ HTTPS และ secret token ใน URL path)

---

## สรุปการใช้งาน

**Use Case ตัวอย่าง:**

1. **n8n สั่ง Relay อัตโนมัติ (Inbound)**
   - ใช้ Cron node หรือ Webhook trigger ใน n8n
   - HTTP Request node → `POST /api/n8n/relay-control/`
   - Dashboard รับคำสั่ง → ส่งไปยัง ESP32 ผ่าน MQTT

2. **บันทึกข้อมูล Telemetry ลง Google Sheets (Outbound)**
   - ตั้งค่า `Enable telemetry webhook` + `Telemetry webhook URL`
   - n8n รับข้อมูล telemetry ผ่าน Webhook node
   - เพิ่ม Google Sheets node เพื่อบันทึกข้อมูล

3. **แจ้งเตือนผ่าน LINE เมื่ออุปกรณ์ offline (Outbound)**
   - ตั้งค่า `Enable device status webhook` + `Device status webhook URL`
   - n8n รับ event `device_status` ที่ `status === "offline"`
   - ส่งข้อความแจ้งเตือนผ่าน LINE Notify

4. **Automation Loop แบบเต็มรูป**
   - ESP32 ส่ง telemetry → Dashboard → n8n (Outbound)
   - n8n วิเคราะห์ข้อมูล (เช่น อุณหภูมิสูง)
   - n8n สั่งเปิด fan → Dashboard → ESP32 (Inbound)
