# Deploy Django Smart Farm บน Render (Web + MQTT Worker)

เอกสารนี้สรุปขั้นตอน deploy โปรเจกต์นี้บน Render แบบแนะนำสำหรับ production โดยแยกบริการเป็น:

- Web Service: ให้บริการ Django Admin, API, Dashboard
- Background Worker: รัน MQTT listener (`run_mqtt_worker`) ตลอดเวลา

## 1. แนวทางสถาปัตยกรรมบน Render

1. Web Service
- ทำหน้าที่รับ HTTP requests
- รันผ่าน Gunicorn
- ใช้ PostgreSQL (แนะนำ) แทน SQLite

2. Worker Service
- ทำหน้าที่เชื่อม MQTT broker และบันทึกข้อมูลลง DB
- ใช้คำสั่ง `python manage.py run_mqtt_worker`
- ต้องชี้ไป DB เดียวกับ Web Service

3. PostgreSQL (Render Managed Postgres)
- ให้ทั้ง Web และ Worker ใช้ connection เดียวกัน

## 2. สิ่งที่ควรเตรียมก่อน Deploy

1. เปลี่ยน `SECRET_KEY` และปิด `DEBUG`
2. ตั้ง `ALLOWED_HOSTS` ให้มีโดเมน Render
3. ใช้ PostgreSQL ใน production
4. ใช้ environment variables แทน hardcode ใน settings
5. เพิ่ม Gunicorn ลง dependencies

## 3. Environment Variables ที่ควรตั้งใน Render

ตั้งทั้ง Web และ Worker (ถ้าไม่ระบุเป็นพิเศษ)

- `DJANGO_SETTINGS_MODULE=myproject.settings`
- `SECRET_KEY=<random-strong-secret>`
- `DEBUG=False`
- `ALLOWED_HOSTS=<your-web-service>.onrender.com`
- `DATABASE_URL=<Render Postgres Internal/External URL>`
- `N8N_WEBHOOK_URL=<your n8n webhook>` (ถ้ามี)

สำหรับ MQTT (ถ้าจะ override ค่าใน DB/Settings)
- `MQTT_BROKER=broker.hivemq.com`
- `MQTT_PORT=1883`
- `MQTT_USER=`
- `MQTT_PASSWORD=`

หมายเหตุ:
- ในโปรเจกต์นี้ MQTT runtime ถูกจัดการผ่านหน้า Admin (`MQTT Settings`) เป็นหลัก
- env vars ยังมีประโยชน์สำหรับค่าเริ่มต้น/สำรอง

## 4. คำสั่ง Build และ Start (แนะนำ)

### 4.1 Web Service

- Build Command:

```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

- Start Command:

```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
```

### 4.2 Worker Service

- Build Command:

```bash
pip install -r requirements.txt && python manage.py migrate
```

- Start Command:

```bash
python manage.py run_mqtt_worker
```

### 4.3 Single Service Mode (Web + MQTT ใน service เดียว)

กรณีต้องการ deploy จุดเดียวเท่านั้น สามารถเปิดโหมดนี้ได้ โดยให้ web process สตาร์ต MQTT worker อัตโนมัติ:

ตั้งค่า env เพิ่มใน Web Service:

- `RUN_MQTT_IN_WEBSERVICE=True`
- `WEB_CONCURRENCY=1`  (สำคัญ: ลดความเสี่ยง worker ซ้ำ)

Start Command (เหมือนเดิม):

```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
```

ข้อควรระวัง:

- โหมดนี้เหมาะเมื่อยอมรับ trade-off ด้านความเสถียรได้
- ถ้า scale web มากกว่า 1 instance/process อาจเกิด MQTT worker หลายตัวพร้อมกัน
- สำหรับ production ระยะยาว แนะนำแยก Worker Service เหมือนหัวข้อ 4.2

## 5. โครง Deploy ทีละขั้นตอนบน Render

1. Push code ขึ้น GitHub branch ที่จะ deploy
2. สร้าง PostgreSQL บน Render
3. สร้าง Web Service จาก repo นี้
- Runtime: Python
- กำหนด Build/Start command ตามหัวข้อ 4.1
- ตั้ง env vars ตามหัวข้อ 3
4. สร้าง Worker Service จาก repo เดียวกัน
- กำหนด Build/Start command ตามหัวข้อ 4.2
- ใช้ env vars ชุดเดียวกับ Web (โดยเฉพาะ `DATABASE_URL`)
5. Deploy Web ก่อน แล้วตรวจหน้า `/admin/`
6. Deploy Worker แล้วดู logs ว่าเชื่อม MQTT ได้
7. เข้า Admin ตั้งค่า
- `MQTT Settings`
- `N8N Settings`
8. ทดสอบ flow end-to-end
- ESP32 -> MQTT -> Worker -> DB
- Dashboard/API -> MQTT control
- Dashboard/Worker -> N8N outbound (ถ้าเปิด)
- N8N -> Dashboard inbound control (ถ้าเปิด)

## 6. ตัวอย่างการตั้งค่า settings.py สำหรับ Production (แนวทาง)

เพิ่ม/ปรับให้รองรับ env vars (ตัวอย่าง):

```python
import os
from pathlib import Path

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]
```

Database (production):

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True,
    )
}
```

Static files (แนะนำเพิ่ม WhiteNoise หากไม่มี CDN):

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

## 7. Dependencies ที่แนะนำเพิ่ม

อัปเดต [requirements.txt](requirements.txt) ให้มีอย่างน้อย:

- `gunicorn`
- `dj-database-url`
- `psycopg[binary]`
- `whitenoise`

## 8. จุดสำคัญของโปรเจกต์นี้ (ต้องรู้ก่อนขึ้น production)

1. `run_mqtt_worker` ควรรันใน Worker แยก ไม่ควรพึ่งการ auto-start ใน web process
2. Web และ Worker ต้องใช้ DB เดียวกัน
3. ถ้าใช้ free plan และ service หลับ (sleep) จะกระทบ real-time
4. ถ้าต้องการเสถียร ให้ใช้ plan ที่ไม่ sleep
5. จัดการ token ของ N8N inbound ให้ปลอดภัย และหมุน token เป็นระยะ

## 9. Checklist ก่อน Go Live

1. ตั้ง `DEBUG=False`
2. เปลี่ยน `SECRET_KEY`
3. ตั้ง `ALLOWED_HOSTS` ถูกต้อง
4. ใช้ PostgreSQL แล้ว migrate ผ่าน
5. Web Service เปิดใช้งานและเข้าหน้า admin ได้
6. Worker Service online และ subscribe topic สำเร็จ
7. ทดสอบ relay control จาก Dashboard
8. ทดสอบ telemetry เข้า DB
9. ทดสอบ N8N outbound/inbound ครบ
10. เปิด log monitoring และแจ้งเตือน error

## 10. Troubleshooting ที่พบบ่อย

1. Web ขึ้นไม่ได้เพราะไม่มี Gunicorn
- เพิ่ม `gunicorn` ใน requirements แล้ว redeploy

2. DB error บน Render
- ตรวจ `DATABASE_URL` และ apply migrations ใหม่

3. Worker ไม่รับข้อมูล MQTT
- เช็ค logs ของ worker
- เช็ค broker/topic ใน `MQTT Settings`
- เช็คว่า service ยังรันอยู่ (ไม่ sleep)

4. N8N inbound 401
- เช็ค `X-N8N-Token` ให้ตรงกับ `inbound_auth_token`

5. static files ไม่ขึ้น
- เพิ่ม `collectstatic` ใน build command
- ตั้ง `STATIC_ROOT` และ WhiteNoise

---

เอกสารนี้เน้นให้ deploy ได้จริงบน Render สำหรับโปรเจกต์ปัจจุบัน โดยรองรับทั้ง Dashboard/API และ MQTT worker แยก process อย่างปลอดภัยและดูแลง่าย
