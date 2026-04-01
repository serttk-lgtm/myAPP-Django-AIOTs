# 🌿 Smart Farm Full Stack Dashboard - Django Project

โปรเจกต์ Django Framework สำหรับสร้าง Landing Page และ Dashboard แบบ Full Stack พร้อม UI สไตล์ Smart Farm โทนสีเขียว

> 📘 **สำหรับผู้ที่ Clone โปรเจกต์มาใหม่:** อ่านคู่มือฉบับเต็มได้ที่ [SETUP-GUIDE.md](SETUP-GUIDE.md)

---

## � เริ่มต้นอย่างรวดเร็ว (Quick Start)

### สำหรับผู้ที่ Clone โปรเจกต์มาใช้งาน

```cmd
REM 1. Clone repository
git clone https://github.com/thaitechzone/myAPP-Django-AIOTs.git
cd myAPP-Django-AIOTs

REM 2. สร้างและเปิดใช้งาน virtual environment
python -m venv venv
venv\Scripts\activate.bat

REM 3. ติดตั้ง dependencies
pip install -r requirements.txt

REM 4. รัน migration
python manage.py migrate

REM 5. รัน development server
python manage.py runserver

REM 6. เปิดเบราว์เซอร์ไปที่ http://127.0.0.1:8000/
```

### ✅ ตรวจสอบว่า Setup สำเร็จ

- เห็น `(venv)` หน้า command line
- ไม่มี error จากการติดตั้ง packages
- Server รันได้ที่ http://127.0.0.1:8000/
- เห็นหน้า Landing Page สไตล์ Smart Farm

---

## ⚙️ คำสั่งสำหรับใช้งานประจำวัน

หลังจาก clone และ setup เรียบร้อยแล้ว เมื่อเปิด terminal ใหม่ทุกครั้ง ให้ใช้คำสั่งเหล่านี้:

```cmd
REM 1. เข้าไปยังโฟลเดอร์โปรเจกต์
cd myAPP-Django-AIOTs

REM 2. เปิดใช้งาน virtual environment
venv\Scripts\activate.bat

REM 3. รัน development server
python manage.py runserver
```

> 💡 **หมายเหตุ:** ต้อง activate virtual environment ทุกครั้งที่เปิด terminal ใหม่

---

## 🔧 แก้ไขปัญหาที่พบบ่อยหลัง Clone

---

### ❌ ปัญหา: Python ไม่อยู่ใน PATH

```
'python' is not recognized as an internal or external command
```

**วิธีแก้:**
- ติดตั้ง Python ใหม่และเลือก "Add Python to PATH"
- หรือใช้ `py` แทน `python`:
```cmd
py -m venv venv
py manage.py runserver
```

---

### ❌ ปัญหา: ModuleNotFoundError หลังติดตั้ง

```
ModuleNotFoundError: No module named 'django'
```

**วิธีแก้:**
```cmd
REM 1. ตรวจสอบว่า activate venv แล้ว (ต้องมี (venv) หน้า command line)
REM 2. ติดตั้ง dependencies อีกครั้ง
pip install -r requirements.txt

REM 3. ตรวจสอบว่าติดตั้งสำเร็จ
pip list
```

---

### ❌ ปัญหา: requirements.txt ไม่มีหรือเสียหาย

**วิธีแก้:**
```cmd
REM ติดตั้ง Django แบบ manual
pip install django

REM สร้าง requirements.txt ใหม่
pip freeze > requirements.txt
```

---

### ❌ ปัญหา: Port 8000 ถูกใช้งานอยู่

```
Error: That port is already in use.
```

**วิธีแก้:**
```cmd
REM ใช้ port อื่นแทน เช่น 8080
python manage.py runserver 8080

REM เปิดเบราว์เซอร์ที่ http://127.0.0.1:8080/
```

---

### ❌ ปัญหา: Database เสียหายหรือขัดข้อง

**วิธีแก้:**
```cmd
REM ลบ database เก่าและสร้างใหม่
REM ⚠️ ระวัง: จะลบข้อมูลทั้งหมด
del db.sqlite3

REM รัน migration ใหม่
python manage.py migrate
```

---

## 📋 สารบัญ

1. [เริ่มต้นอย่างรวดเร็ว (Quick Start)](#-เริ่มต้นอย่างรวดเร็ว-quick-start)
2. [ติดตั้งและเตรียมสภาพแวดล้อม](#2-ติดตั้งและเตรียมสภาพแวดล้อม)
3. [สร้าง Django Project](#3-สร้าง-django-project)
4. [สร้าง Landing Page](#4-สร้าง-landing-page)
5. [รัน Development Server](#5-รัน-development-server)
6. [แนะนำ Prompt สำหรับใช้ AI](#6-แนะนำ-prompt-สำหรับใช้-ai)

---

## 2. ติดตั้งและเตรียมสภาพแวดล้อม

### ✅ ขั้นตอนที่ 1: ตรวจสอบ Python

```cmd
REM ตรวจสอบเวอร์ชัน Python (ต้องการ Python 3.8+)
python --version

REM ตรวจสอบ pip
pip --version
```

### ✅ ขั้นตอนที่ 2: สร้าง Virtual Environment

```cmd
REM สร้าง virtual environment
python -m venv venv

REM เปิดใช้งาน
venv\Scripts\activate.bat
```

> 💡 เมื่อ activate สำเร็จจะเห็น `(venv)` อยู่หน้า command line

### ✅ ขั้นตอนที่ 3: ติดตั้ง Django

```cmd
REM ติดตั้ง Django เวอร์ชันล่าสุด
pip install django

REM ตรวจสอบเวอร์ชัน Django
python -m django --version
```

---

## 3. สร้าง Django Project

### ✅ สร้าง Project และ App

```cmd
REM สร้าง Django project
django-admin startproject myproject
cd myproject

REM สร้าง Django app
python manage.py startapp myapp
```

### ✅ ลงทะเบียน App ใน settings.py

แก้ไขไฟล์ `myproject/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # ← เพิ่มบรรทัดนี้
]
```

### ✅ ทำ Migration

```cmd
REM สร้างและรัน migration
python manage.py makemigrations
python manage.py migrate

REM สร้าง superuser สำหรับ admin (optional)
python manage.py createsuperuser
```

---

## 4. สร้าง Landing Page

### ✅ สร้าง View Function

แก้ไขไฟล์ `myapp/views.py`:

```python
from django.shortcuts import render

def landing_page(request):
    return render(request, 'myapp/landing.html')
```

### ✅ ตั้งค่า URL Routing

แก้ไขไฟล์ `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # ← หน้าแรก
    path('admin/', admin.site.urls),
]
```

### ✅ สร้างโฟลเดอร์ templates

```cmd
REM สร้างโฟลเดอร์สำหรับเก็บ HTML template
mkdir myapp\templates\myapp
```

### ✅ สร้างไฟล์ landing.html

สร้างไฟล์ `myapp/templates/myapp/landing.html` ด้วยเนื้อหา UI ที่ต้องการ

> 💡 **Tip**: ใช้ AI ช่วยสร้าง UI ได้ด้วย prompt ที่ชัดเจน (ดูตัวอย่างในหัวข้อถัดไป)

---

## 5. รัน Development Server

### ✅ สตาร์ท Django Server

```cmd
REM รัน server
python manage.py runserver

REM รัน server ที่ port อื่น (เช่น 8080)
python manage.py runserver 8080
```

### ✅ เปิดเว็บในเบราว์เซอร์

เปิด browser และไปที่:
- **หน้าแรก**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 6. แนะนำ Prompt สำหรับใช้ AI

### 🤖 Prompt สำหรับสร้าง Landing Page UI

**ตัวอย่าง Prompt ที่ดี:**

```
ช่วยสร้าง Landing Page : Full Stack Dev UI Dashboard ให้หน่อย 
สไตล์ Smart Farm สีสันโทนเขียว สวยงาม 
พร้อมทั้งเปิดหน้าแรกใน http://127.0.0.1:8000/ ให้แสดงผลได้ทันที
```

**องค์ประกอบของ Prompt ที่ดี:**
1. **ระบุชัดเจน** - บอกว่าต้องการ Landing Page หรือ Dashboard
2. **ระบุสไตล์** - เช่น "สไตล์ Smart Farm", "โมเดิร์น", "มินิมอล"
3. **ระบุโทนสี** - เช่น "โทนเขียว", "โทนฟ้า", "สีพาสเทล"
4. **ระบุความต้องการ** - เช่น "สวยงาม", "responsive", "มี animation"
5. **ระบุผลลัพธ์** - เช่น "ให้แสดงผลได้ทันที", "พร้อมใช้งาน"

---

### 🤖 Prompt Template สำหรับฟีเจอร์อื่นๆ

#### 1. สร้างระบบ CRUD

```
ช่วยสร้างระบบจัดการข้อมูล [ชื่อข้อมูล] ให้หน่อย
ต้องการ Create, Read, Update, Delete
พร้อม UI แบบตาราง และ form สำหรับแก้ไข
ใช้สไตล์ [ระบุสไตล์] โทนสี [ระบุสี]
```

**ตัวอย่าง:**
```
ช่วยสร้างระบบจัดการข้อมูลเซนเซอร์ให้หน่อย
ต้องการ Create, Read, Update, Delete
พร้อม UI แบบตาราง และ form สำหรับแก้ไข
ใช้สไตล์โมเดิร์น โทนสีเขียว-ขาว
```

#### 2. เพิ่ม Authentication

```
ช่วยเพิ่มระบบ Login/Logout ให้กับโปรเจกต์ Django
ต้องการหน้า Login, Register, และ Logout
พร้อม UI แบบ [ระบุสไตล์]
```

#### 3. สร้าง API Endpoint

```
ช่วยสร้าง REST API สำหรับ [ชื่อข้อมูล] ให้หน่อย
ต้องการ GET, POST, PUT, DELETE endpoints
พร้อม serializer และ documentation
```

#### 4. เพิ่ม Dashboard Widgets

```
ช่วยเพิ่ม widget แสดง [ข้อมูลที่ต้องการ] ใน Dashboard
แบบ real-time หรือ สรุปเป็นกราฟ
สไตล์ [ระบุสไตล์] โทนสี [ระบุสี]
```

**ตัวอย่าง:**
```
ช่วยเพิ่ม widget แสดงอุณหภูมิและความชื้นใน Dashboard
แบบ real-time พร้อมกราฟเส้น
สไตล์โมเดิร์น โทนสีเขียวธรรมชาติ
```

#### 5. ปรับแต่ง UI/UX

```
ช่วยปรับ UI ของ [ชื่อหน้า] ให้ [ระบุความต้องการ]
เพิ่ม [รายละเอียดที่ต้องการ]
โทนสี [ระบุสี] สไตล์ [ระบุสไตล์]
```

**ตัวอย่าง:**
```
ช่วยปรับ UI ของหน้า Landing ให้มี animation เคลื่อนไหว
เพิ่มปุ่ม CTA และ section testimonials
โทนสีเขียว-ขาว สไตล์ สมาร์ทฟาร์ม
```

---

### 🎯 Tips สำหรับการใช้ AI อย่างมีประสิทธิภาพ

1. **ระบุบริบท** - บอก AI ว่าคุณกำลังทำโปรเจกต์อะไร
2. **แบ่งงานเป็นชิ้นเล็ก** - ไม่ควรขอทำทุกอย่างพร้อมกัน
3. **ให้ข้อมูลเพียงพอ** - ระบุสี, สไตล์, ฟีเจอร์ที่ต้องการ
4. **ตรวจสอบผลลัพธ์** - ทดสอบและให้ feedback กลับไป
5. **ใช้ภาษาที่ชัดเจน** - หลีกเลี่ยงคำที่คลุมเครือ

---

## 📦 โครงสร้างโปรเจกต์

```
myAPP-Django-AIOTs/
├── venv/                    # Virtual environment
├── myproject/               # Django project folder
│   ├── __init__.py
│   ├── settings.py         # การตั้งค่าโปรเจกต์
│   ├── urls.py             # URL routing หลัก
│   ├── wsgi.py
│   └── asgi.py
├── myapp/                   # Django app folder
│   ├── migrations/
│   ├── templates/
│   │   └── myapp/
│   │       └── landing.html # Landing page template
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Model สำหรับ database
│   ├── views.py            # View functions
│   └── tests.py
├── manage.py               # Django management script
├── db.sqlite3              # Database (SQLite)
├── requirements.txt        # Python dependencies
└── README.md               # เอกสารนี้
```

---

## 🚀 คำสั่งที่ใช้บ่อย

```cmd
REM เปิด virtual environment
venv\Scripts\activate.bat

REM รัน development server
python manage.py runserver

REM สร้าง migration จาก model ใหม่
python manage.py makemigrations

REM ใช้ migration กับ database
python manage.py migrate

REM สร้าง superuser
python manage.py createsuperuser

REM สร้าง app ใหม่
python manage.py startapp [app_name]

REM บันทึก dependencies
pip freeze > requirements.txt

REM ติดตั้ง dependencies
pip install -r requirements.txt
```

---

## 🎨 ฟีเจอร์ที่มีใน Landing Page ปัจจุบัน

- ✅ UI Dashboard สไตล์ Smart Farm โทนสีเขียว
- ✅ แสดงข้อมูล Real-time Statistics
- ✅ Sensor Live Feed แบบ Card Layout
- ✅ Resource Usage Progress Bars
- ✅ Responsive Design (รองรับ Mobile)
- ✅ Gradient Background ธรรมชาติ
- ✅ Animation แบบค่อยๆ ปรากฏ

---

## 📝 หมายเหตุ

- โปรเจกต์นี้ใช้ **Django 6.0.3** และ **Python 3.14**
- Database ใช้ **SQLite** (เหมาะสำหรับ development)
- ไฟล์ `SECRET_KEY` ใน settings.py ควรเปลี่ยนก่อนใช้งาน production
- สามารถปรับแต่ง UI ใน `myapp/templates/myapp/landing.html` ได้ตามต้องการ

---

## 🆘 แก้ไขปัญหาที่พบบ่อย

### ปัญหา: ModuleNotFoundError: No module named 'django'

**วิธีแก้:**
```cmd
REM ตรวจสอบว่า activate virtual environment แล้ว
REM ติดตั้ง Django ใหม่
pip install django
```

### ปัญหา: TemplateDoesNotExist

**วิธีแก้:**
- ตรวจสอบว่าโฟลเดอร์ `templates/myapp/` ถูกสร้างแล้ว
- ตรวจสอบว่า app ถูกเพิ่มใน `INSTALLED_APPS` ใน settings.py

### ปัญหา: Port 8000 already in use

**วิธีแก้:**
```cmd
REM ใช้ port อื่นแทน
python manage.py runserver 8080
```

---

## 📚 แหล่งเรียนรู้เพิ่มเติม

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Tutorial for Beginners](https://www.djangoproject.com/start/)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

## 👨‍💻 สร้างโดย

Full Stack Development with AI Assistance  
สร้างด้วย Django Framework & GitHub Copilot

**วันที่สร้าง:** April 2026

---

**Happy Coding! 🌱💻**
