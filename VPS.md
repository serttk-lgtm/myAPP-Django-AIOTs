# Deploy บน Render — คู่มือขั้นตอนล่าสุด

> อัปเดต: April 2026  
> Branch: `04_Add_N8N_Handle`  
> Stack: Django 6.0.3 · PostgreSQL (psycopg 3) · Gunicorn · WhiteNoise · paho-mqtt

---

## ภาพรวม Architecture

```
Render Web Service
├── Gunicorn (HTTP)
│   └── Django Admin / API / Dashboard
└── [Optional] MQTT Worker thread (ถ้าเปิด RUN_MQTT_IN_WEBSERVICE=True)

Render Worker Service  ← แนะนำสำหรับ production
└── python manage.py run_mqtt_worker

Supabase / Render PostgreSQL
└── ใช้ร่วมกันทั้ง Web และ Worker
```

---

## ขั้นตอนที่ 1 — เตรียม Code ก่อน Push

### 1.1 ตรวจ requirements.txt
ต้องมีครบ:
```
Django==6.0.3
gunicorn==23.0.0
psycopg[binary]==3.2.13
whitenoise==6.9.0
paho-mqtt==2.1.0
requests==2.32.3
```

### 1.2 ตรวจ settings.py
- `load_env_file(BASE_DIR / '.env')` อยู่บนสุดของไฟล์ ✅
- `build_database_config()` ไม่มี SQLite fallback แล้ว — raise `ImproperlyConfigured` ถ้าไม่มี `DATABASE_URL` ✅
- `USE_WHITENOISE` เปิดอัตโนมัติเมื่อ `DEBUG=False` ✅

### 1.3 Push ขึ้น GitHub
```powershell
git add -A
git commit -m "deploy: ready for Render production"
git push origin 04_Add_N8N_Handle
```

---

## ขั้นตอนที่ 2 — เตรียม Database (PostgreSQL)

**ตัวเลือก A: ใช้ Supabase (ตามที่ตั้งค่าไว้แล้ว)**
- ไม่ต้องทำอะไรเพิ่ม — `DATABASE_URL` ใน `.env` ชี้ไปที่ Supabase แล้ว
- Copy URL จาก Supabase → Project Settings → Database → Connection string (URI)
- Format: `postgresql://postgres.[project-ref]:[password]@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres`

**ตัวเลือก B: ใช้ Render Managed PostgreSQL**
1. ใน Render Dashboard → New → PostgreSQL
2. ตั้งชื่อ เลือก Region ใกล้ users
3. Copy "Internal Database URL" (ใช้ภายใน Render เร็วกว่า)

---

## ขั้นตอนที่ 3 — สร้าง Web Service บน Render

1. Render Dashboard → **New → Web Service**
2. Connect GitHub repo `thaitechzone/myAPP-Django-AIOTs`
3. เลือก branch ที่จะ deploy (`04_Add_N8N_Handle` หรือ `master`)
4. ตั้งค่า:

| Field | Value |
|-------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| Start Command | `gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT` |

---

## ขั้นตอนที่ 4 — ตั้ง Environment Variables

ไปที่ **Environment** tab ของ Web Service แล้วเพิ่มครบทุกตัวนี้:

### ✅ Required (บังคับ)

| Variable | ค่า | หมายเหตุ |
|----------|-----|----------|
| `SECRET_KEY` | `<random 50+ chars>` | Generate ด้วย `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | `False` | **สำคัญ: ห้ามลืม** |
| `ALLOWED_HOSTS` | `<your-app>.onrender.com` | เพิ่มหลาย domain ด้วยคอมม่า |
| `CSRF_TRUSTED_ORIGINS` | `https://<your-app>.onrender.com` | ต้องมี https:// นำหน้า |
| `DATABASE_URL` | URL จาก Supabase หรือ Render Postgres | รองรับ `postgres://` หรือ `postgresql://` เท่านั้น |

### ⚙️ Optional แต่แนะนำ

| Variable | ค่าแนะนำ | หมายเหตุ |
|----------|----------|----------|
| `DB_CONN_MAX_AGE` | `0` | ใช้ `0` สำหรับ Supabase Pooler (PgBouncer) |
| `DB_SSLMODE` | `require` | Default อยู่แล้ว |
| `SITE_URL` | `https://<your-app>.onrender.com` | ใช้ใน absolute URL generation |
| `USE_WHITENOISE` | `True` | Default เปิดอัตโนมัติเมื่อ DEBUG=False |

### 🔌 MQTT / N8N (ถ้าใช้งาน)

| Variable | ค่า |
|----------|-----|
| `MQTT_BROKER` | `broker.hivemq.com` (หรือ broker ของคุณ) |
| `MQTT_PORT` | `1883` |
| `MQTT_USER` | ถ้ามี |
| `MQTT_PASSWORD` | ถ้ามี |
| `N8N_WEBHOOK_URL` | URL ของ n8n ถ้าใช้ outbound |

### ✅ ค่าที่ทดสอบแล้วบน Host (ใช้งานได้จริง)

ชุดด้านล่างคือค่าหลักที่ยืนยันแล้วว่า deploy ทำงานได้บน Render:

```env
ALLOWED_HOSTS=myapp-django-aiots.onrender.com
DATABASE_URL=postgresql://postgres.zqdybzextauatcgyliwm:xxx@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
DB_CONN_MAX_AGE=0
DEBUG=False
DJANGO_SETTINGS_MODULE=myproject.settings
RUN_MQTT_IN_WEBSERVICE=True
SECRET_KEY=xxx
WEB_CONCURRENCY=1
```

หมายเหตุ:
- ค่า `SECRET_KEY` และ password ใน `DATABASE_URL` ต้องเก็บเป็นความลับเสมอ
- แนะนำเพิ่ม `CSRF_TRUSTED_ORIGINS=https://myapp-django-aiots.onrender.com` เพื่อเลี่ยง CSRF error ใน production

---

## ขั้นตอนที่ 5 — เลือกโหมด MQTT Worker

### โหมด A: Worker Service แยก (แนะนำสำหรับ production)

สร้าง **Worker Service** ใหม่บน Render จาก repo เดียวกัน:

| Field | Value |
|-------|-------|
| Build Command | `pip install -r requirements.txt && python manage.py migrate` |
| Start Command | `python manage.py run_mqtt_worker` |

- ใช้ Environment Variables ชุดเดียวกับ Web Service (โดยเฉพาะ `DATABASE_URL`)
- **ไม่ต้องตั้ง** `RUN_MQTT_IN_WEBSERVICE`

### โหมด B: Single Service (Web + MQTT รวมกัน)

เพิ่ม env vars ใน Web Service:

| Variable | Value |
|----------|-------|
| `RUN_MQTT_IN_WEBSERVICE` | `True` |
| `WEB_CONCURRENCY` | `1` |

> ⚠️ **คำเตือน**: `WEB_CONCURRENCY=1` บังคับ — ถ้า scale หลาย process จะเกิด MQTT worker หลายตัวพร้อมกัน  
> โหมดนี้เหมาะกับ hobby/dev เท่านั้น

---

## ขั้นตอนที่ 6 — Deploy และตรวจสอบ

### 6.1 Trigger Deploy
- Render จะ deploy อัตโนมัติเมื่อ push ถ้าเปิด Auto-Deploy
- หรือกด **Manual Deploy** ใน Dashboard

### 6.2 ดู Build Log
Build Command จะรัน:
1. `pip install -r requirements.txt` — ติดตั้ง dependencies
2. `python manage.py migrate` — apply migrations ลง PostgreSQL
3. `python manage.py collectstatic --noinput` — รวม static files

### 6.3 ตรวจสอบหลัง Deploy

| ขั้นตอน | URL / Command |
|---------|---------------|
| เข้าหน้า Admin | `https://<your-app>.onrender.com/admin/` |
| ดู Log ของ Web | Render Dashboard → Web Service → Logs |
| ดู Log ของ Worker | Render Dashboard → Worker Service → Logs |
| ตรวจ MQTT connect | หา log: `Connected to MQTT broker` |

---

## ขั้นตอนที่ 7 — ตั้งค่าหลัง Deploy (Admin)

1. เข้า `https://<your-app>.onrender.com/admin/`
2. Login ด้วย superuser (ถ้ายังไม่มี ให้รัน `python manage.py createsuperuser` ใน Render Shell)
3. ไปที่ **MQTT Settings** → ตั้ง Broker, Port, Topics
4. ไปที่ **N8N Settings** → ตั้ง Webhook URL (ถ้าใช้)
5. ทดสอบ relay control จาก Dashboard

> ⚠️ **Security**: ถ้า admin password เดิมเป็น `admin1234` ให้เปลี่ยนทันทีด้วย:
> ```
> python manage.py changepassword admin
> ```

---

## ขั้นตอนที่ 8 — Checklist ก่อน Go Live

- [ ] `DEBUG=False` ตั้งใน env
- [ ] `SECRET_KEY` เป็น random string ที่แข็งแกร่ง (ไม่ใช่ default)
- [ ] `ALLOWED_HOSTS` มีโดเมน Render ถูกต้อง
- [ ] `CSRF_TRUSTED_ORIGINS` มี `https://` นำหน้าโดเมน
- [ ] `DATABASE_URL` ชี้ไป PostgreSQL (ไม่มี `sqlite://`)
- [ ] `python manage.py migrate` ผ่านใน Build Log
- [ ] หน้า `/admin/` เปิดได้และ login ผ่าน
- [ ] MQTT Worker log แสดง `Connected to MQTT broker`
- [ ] ทดสอบ telemetry จาก ESP32 → Database
- [ ] Admin password เปลี่ยนจาก default แล้ว

---

## Troubleshooting ที่พบบ่อย

### ❌ `ImproperlyConfigured: DATABASE_URL is required`
`DATABASE_URL` ไม่ได้ตั้งใน Render Environment → เพิ่ม env var แล้ว redeploy

### ❌ `ImproperlyConfigured: Unsupported DATABASE_URL scheme: sqlite`
มี `DATABASE_URL=sqlite:///...` ตกค้างอยู่ → แก้ให้เป็น `postgresql://...`

### ❌ Static files ไม่โหลด (CSS หาย)
- ตรวจว่า `python manage.py collectstatic` รันใน Build Command
- ตรวจว่า `USE_WHITENOISE=True` หรือ `DEBUG=False` (เปิดอัตโนมัติ)

### ❌ CSRF Error เมื่อ submit form
เพิ่ม `CSRF_TRUSTED_ORIGINS=https://<your-app>.onrender.com` ใน env

### ❌ Worker ไม่เชื่อม MQTT
- ตรวจ log ของ Worker Service
- ตรวจ MQTT Settings ใน Admin ว่า Broker/Port ถูกต้อง
- ตรวจว่า Broker ไม่บล็อค connection จาก IP ของ Render

### ❌ `OperationalError: SSL connection required`  
เพิ่ม `DB_SSLMODE=require` ใน env (หรือตรวจว่า `DATABASE_URL` มี `?sslmode=require` ต่อท้าย)

---

## Quick Reference — Environment Variables ครบชุด

```env
# Required
SECRET_KEY=xxx
DEBUG=False
ALLOWED_HOSTS=myapp-django-aiots.onrender.com
CSRF_TRUSTED_ORIGINS=https://myapp-django-aiots.onrender.com
DATABASE_URL=postgresql://postgres.zqdybzextauatcgyliwm:xxx@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
DJANGO_SETTINGS_MODULE=myproject.settings

# Database tuning
DB_CONN_MAX_AGE=0
DB_SSLMODE=require

# MQTT Worker mode (เลือกอย่างใดอย่างหนึ่ง)
RUN_MQTT_IN_WEBSERVICE=True
WEB_CONCURRENCY=1

# Optional
SITE_URL=https://myapp-django-aiots.onrender.com
N8N_WEBHOOK_URL=https://your-n8n.com/webhook/xxx
```
