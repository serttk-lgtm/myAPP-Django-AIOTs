# N8N Relay Control Test Guide (Latest)

เอกสารนี้สรุปขั้นตอนทดสอบการสั่ง Relay จาก n8n ไปยัง Django API ให้ใช้งานได้จริงล่าสุด

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

## 7) Checklist ทดสอบสั้น

- [ ] เปิด `Enable inbound webhook` แล้ว
- [ ] ใช้ token ล่าสุดจาก Admin
- [ ] URL ลงท้ายด้วย `/api/n8n/relay-control/`
- [ ] Method เป็น `POST`
- [ ] ส่ง `Content-Type: application/json`
- [ ] Payload มี `board_id`
- [ ] `board_id` ตรงกับอุปกรณ์จริงในระบบ

## 8) Security Note

- ห้าม commit token ลง repo
- ถ้า token เคยถูกแชร์ในแชต/หน้าจอ ให้ rotate token ใหม่ทันทีหลังทดสอบ
