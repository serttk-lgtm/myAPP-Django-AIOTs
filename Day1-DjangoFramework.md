# Day 1 - คำสั่งสร้าง Project Django Framework

## ขั้นตอนที่ 1: ติดตั้ง Python และตรวจสอบเวอร์ชัน

```bash
# ตรวจสอบเวอร์ชัน Python
python --version

# ตรวจสอบเวอร์ชัน pip
pip --version
```

---

## ขั้นตอนที่ 2: สร้าง Virtual Environment

```bash
# สร้าง virtual environment ชื่อ venv
python -m venv venv

# เปิดใช้งาน virtual environment (Windows)
venv\Scripts\activate

# เปิดใช้งาน virtual environment (Mac/Linux)
source venv/bin/activate
```

> หลังจาก activate สำเร็จ จะเห็น `(venv)` นำหน้า command line

---

## ขั้นตอนที่ 3: ติดตั้ง Django

```bash
# ติดตั้ง Django เวอร์ชันล่าสุด
pip install django

# หรือติดตั้ง Django เวอร์ชันที่ต้องการ
pip install django==5.0

# ตรวจสอบเวอร์ชัน Django ที่ติดตั้ง
python -m django --version
```

---

## ขั้นตอนที่ 4: สร้าง Django Project

```bash
# สร้าง project ใหม่ (เปลี่ยน myproject เป็นชื่อ project ที่ต้องการ)
django-admin startproject myproject .

# เข้าไปในโฟลเดอร์ project
cd myproject
```

โครงสร้างไฟล์ที่ได้:
```
myproject/
├── manage.py
└── myproject/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

---

## ขั้นตอนที่ 5: รัน Development Server

```bash
# รัน server ที่ port 8000 (default)
python manage.py runserver

# รัน server ที่ port อื่น เช่น 8080
python manage.py runserver 8080
```

> เปิด browser ไปที่ `http://127.0.0.1:8000/` เพื่อตรวจสอบว่า Django ทำงานได้ปกติ

---

## ขั้นตอนที่ 6: สร้าง Django App

```bash
# สร้าง app ใหม่ภายใน project (เปลี่ยน myapp เป็นชื่อ app ที่ต้องการ)
python manage.py startapp myapp
```

โครงสร้างไฟล์ app ที่ได้:
```
myapp/
├── migrations/
│   └── __init__.py
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```

---

## ขั้นตอนที่ 7: ลงทะเบียน App ใน settings.py

เปิดไฟล์ `myproject/settings.py` และเพิ่ม app เข้าไปใน `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # เพิ่มบรรทัดนี้
]
```

---

## ขั้นตอนที่ 8: สร้าง Database (Migration)

```bash
# สร้างไฟล์ migration จาก model ที่กำหนดใน models.py
python manage.py makemigrations

# นำ migration ไปสร้างตารางใน database
python manage.py migrate
```

---

## ขั้นตอนที่ 9: สร้าง Superuser (Admin)

```bash
# สร้างบัญชี admin สำหรับเข้า Django Admin Panel
python manage.py createsuperuser
```

> กรอก Username, Email และ Password ตามที่ระบบถาม  
> เข้าใช้งาน Admin ได้ที่ `http://127.0.0.1:8000/admin/`

---

## ขั้นตอนที่ 10: บันทึก Dependencies

```bash
# บันทึกรายการ package ที่ติดตั้งลงไฟล์ requirements.txt
pip freeze > requirements.txt

# ติดตั้ง package จาก requirements.txt (สำหรับใช้งานในเครื่องอื่น)
pip install -r requirements.txt
```

---

## สรุปคำสั่งทั้งหมด (Quick Reference)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

pip install django
django-admin startproject myproject
cd myproject

python manage.py startapp myapp
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

pip freeze > requirements.txt
```
