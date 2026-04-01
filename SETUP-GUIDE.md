# 📘 คู่มือ Setup สำหรับ Clone โปรเจกต์

เอกสารนี้สำหรับผู้ที่ต้องการ clone โปรเจกต์ **myAPP-Django-AIOTs** ไปรันบนเครื่องใหม่

---

## 📋 ข้อกำหนดเบื้องต้น

ก่อนเริ่ม ต้องมีโปรแกรมเหล่านี้ติดตั้งแล้ว:

- ✅ **Git** - สำหรับ clone repository
- ✅ **Python 3.8+** - สำหรับรัน Django
- ✅ **pip** - สำหรับติดตั้ง Python packages

### ตรวจสอบการติดตั้ง

```cmd
REM ตรวจสอบ Git
git --version

REM ตรวจสอบ Python
python --version
REM หรือ
py --version

REM ตรวจสอบ pip
pip --version
```

---

## 🚀 ขั้นตอนการ Setup (Step by Step)

### 1️⃣ Clone Repository

```cmd
REM Clone โปรเจกต์จาก GitHub
git clone https://github.com/thaitechzone/myAPP-Django-AIOTs.git
```

✅ **ผลลัพธ์ที่คาดหวัง:**
```
Cloning into 'myAPP-Django-AIOTs'...
remote: Enumerating objects: ...
Receiving objects: 100% ...
```

---

### 2️⃣ เข้าไปในโฟลเดอร์โปรเจกต์

```cmd
cd myAPP-Django-AIOTs
```

---

### 3️⃣ สร้าง Virtual Environment

```cmd
python -m venv venv
```

✅ **ผลลัพธ์:** โฟลเดอร์ `venv/` จะถูกสร้างขึ้น

---

### 4️⃣ เปิดใช้งาน Virtual Environment

```cmd
venv\Scripts\activate.bat
```

✅ **ผลลัพธ์:** จะเห็น `(venv)` ปรากฏหน้า command line

```cmd
(venv) D:\myAPP-Django-AIOTs>
```

---

### 5️⃣ ติดตั้ง Dependencies

```cmd
pip install -r requirements.txt
```

✅ **ผลลัพธ์:**
```
Successfully installed Django-6.0.3 ...
```

🕐 **ใช้เวลาประมาณ:** 1-2 นาที ขึ้นอยู่กับความเร็วอินเทอร์เน็ต

---

### 6️⃣ รัน Migration

```cmd
python manage.py migrate
```

✅ **ผลลัพธ์:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

📝 **คำสั่งนี้ทำอะไร:** สร้างตาราง database (SQLite) ที่จำเป็นสำหรับ Django

---

### 7️⃣ รัน Development Server

```cmd
python manage.py runserver
```

✅ **ผลลัพธ์:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 01, 2026 - 10:00:00
Django version 6.0.3, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### 8️⃣ เปิดเว็บในเบราว์เซอร์

เปิดเบราว์เซอร์แล้วไปที่:

- **หน้าแรก:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

✅ **ควรเห็น:** Landing Page สไตล์ Smart Farm โทนสีเขียว

---

### คำสั่งทั้งหมดในไฟล์เดียว

```cmd
REM 1. Clone repository
git clone https://github.com/thaitechzone/myAPP-Django-AIOTs.git

REM 2. เข้าไปในโฟลเดอร์
cd myAPP-Django-AIOTs

REM 3. สร้าง virtual environment
python -m venv venv

REM 4. เปิดใช้งาน virtual environment
venv\Scripts\activate.bat

REM 5. ติดตั้ง dependencies
pip install -r requirements.txt

REM 6. รัน migration
python manage.py migrate

REM 7. รัน server
python manage.py runserver
```

---

## 📁 โครงสร้างโปรเจกต์หลังจาก Setup

```
myAPP-Django-AIOTs/
├── venv/                         # ← ถูกสร้างจาก python -m venv venv
│   ├── Scripts/                  # (Windows)
│   └── ...
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── myapp/
│   ├── templates/
│   │   └── myapp/
│   │       └── landing.html
│   ├── views.py
│   └── ...
├── manage.py
├── db.sqlite3                    # ← ถูกสร้างจาก python manage.py migrate
├── requirements.txt
├── README.md
└── SETUP-GUIDE.md               # ← ไฟล์นี้
```

---

## ⚙️ คำสั่งสำหรับใช้งานประจำวัน

หลังจาก setup เรียบร้อยแล้ว เมื่อเปิด terminal ใหม่ทุกครั้ง ให้ทำตามนี้:

```cmd
cd myAPP-Django-AIOTs
venv\Scripts\activate.bat
python manage.py runserver
```

🛑 **หยุด Server:** กด `Ctrl+C` หรือ `Ctrl+Break`

---

## 🔧 คำสั่งเพิ่มเติม (Optional)

### สร้าง Superuser สำหรับ Admin Panel

```cmd
python manage.py createsuperuser
```

จะถูกถามให้ใส่:
- Username
- Email (optional)
- Password

หลังจากนั้นสามารถ login ที่ http://127.0.0.1:8000/admin/

---

### รันที่ Port อื่น

```cmd
REM รันที่ port 8080 แทน 8000
python manage.py runserver 8080

REM เปิดเบราว์เซอร์ที่ http://127.0.0.1:8080/
```

---

### รันแบบเปิดให้เครื่องอื่นเข้าถึงได้

```cmd
REM เปิดให้เครื่องอื่นในเครือข่ายเดียวกันเข้าถึงได้
python manage.py runserver 0.0.0.0:8000

REM เครื่องอื่นสามารถเข้าถึงได้ผ่าน http://<your-ip>:8000/
```

---

### อัพเดท Dependencies

```cmd
REM ติดตั้ง package เพิ่ม
pip install <package_name>

REM บันทึกลงใน requirements.txt
pip freeze > requirements.txt
```

---

## 🆘 แก้ไขปัญหาที่พบบ่อย

### ❌ ปัญหา 1: Python ไม่อยู่ใน PATH

**อาการ:**
```
'python' is not recognized as an internal or external command
```

**วิธีแก้:**

**Option 1:** ติดตั้ง Python ใหม่
- ดาวน์โหลดจาก https://www.python.org/downloads/
- เลือก "Add Python to PATH" ตอนติดตั้ง

**Option 2:** ใช้ `py` launcher แทน
```cmd
py -m venv venv
py manage.py runserver
```

**Option 3:** เพิ่ม Python เข้า PATH Manual
1. ค้นหา "Environment Variables" ใน Windows
2. แก้ไข "Path" ใน System Variables
3. เพิ่ม path ไปยัง Python (เช่น `C:\Python312\`)

---

### ❌ ปัญหา 2: ModuleNotFoundError

**อาการ:**
```
ModuleNotFoundError: No module named 'django'
```

**สาเหตุ:** ลืม activate virtual environment หรือติดตั้ง package ไม่สำเร็จ

**วิธีแก้:**

```cmd
REM 1. ตรวจสอบว่า activate venv แล้ว
REM ต้องเห็น (venv) หน้า command line

REM 2. ถ้ายังไม่ได้ activate
venv\Scripts\activate.bat

REM 3. ติดตั้ง dependencies อีกครั้ง
pip install -r requirements.txt

REM 4. ตรวจสอบว่าติดตั้งสำเร็จ
pip list
```

---

### ❌ ปัญหา 3: requirements.txt ไม่พบหรือเสียหาย

**อาการ:**
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory
```

**วิธีแก้:**

```cmd
REM ติดตั้ง Django แบบ manual
pip install django

REM สร้าง requirements.txt ใหม่
pip freeze > requirements.txt
```

---

### ❌ ปัญหา 4: Port 8000 ถูกใช้งานอยู่

**อาการ:**
```
Error: That port is already in use.
```

**วิธีแก้:**

**Option 1:** ใช้ port อื่น
```cmd
python manage.py runserver 8080
REM เปิดเบราว์เซอร์ที่ http://127.0.0.1:8080/
```

**Option 2:** ปิด process ที่ใช้ port 8000
```cmd
REM หา process ที่ใช้ port 8000
netstat -ano | findstr :8000

REM ปิด process (เปลี่ยน <PID> เป็นเลข PID ที่เจอ)
taskkill /PID <PID> /F
```

---

### ❌ ปัญหา 5: Database Migration ล้มเหลว

**อาการ:**
```
django.db.utils.OperationalError: ...
```

**วิธีแก้:**

```cmd
REM ลบ database เก่า (⚠️ ระวัง: จะลบข้อมูลทั้งหมด)
del db.sqlite3

REM ลบ migration files เก่า (ถ้าจำเป็น)
del myapp\migrations\*.py

REM เว้น __init__.py ไว้
REM สร้าง __init__.py ใหม่
type nul > myapp\migrations\__init__.py

REM รัน migration ใหม่
python manage.py makemigrations
python manage.py migrate
```

---

### ❌ ปัญหา 6: TemplateDoesNotExist

**อาการ:**
```
TemplateDoesNotExist at /
myapp/landing.html
```

**สาเหตุ:** ไฟล์ template หายหรือโฟลเดอร์ไม่ถูกต้อง

**วิธีแก้:**

```cmd
REM ตรวจสอบว่าโฟลเดอร์และไฟล์มีอยู่
REM โครงสร้างที่ถูกต้อง:
REM myapp/
REM   templates/
REM     myapp/
REM       landing.html

REM ถ้าไม่มี ให้สร้างโฟลเดอร์
mkdir myapp\templates\myapp

REM ตรวจสอบว่า myapp ถูกเพิ่มใน INSTALLED_APPS
REM ใน myproject/settings.py
```

---

### ❌ ปัญหา 8: Static files ไม่โหลด

**อาการ:** CSS/JS/รูปภาพไม่แสดง

**วิธีแก้:**

```cmd
REM รวบรวม static files
python manage.py collectstatic

REM ตรวจสอบ settings.py ว่ามี
REM STATIC_URL = '/static/'
```

---

### ❌ ปัญหา 9: Git Clone ช้ามาก

**วิธีแก้:**

```cmd
REM Clone แบบ shallow (เร็วกว่า)
git clone --depth 1 https://github.com/thaitechzone/myAPP-Django-AIOTs.git
```

---

## ✅ Checklist การ Setup

ใช้ checklist นี้ตรวจสอบว่า setup สำเร็จครบทุกขั้นตอน:

- [ ] Clone repository สำเร็จ
- [ ] เข้าไปในโฟลเดอร์โปรเจกต์
- [ ] สร้าง virtual environment (`venv/` folder ถูกสร้าง)
- [ ] Activate virtual environment (เห็น `(venv)` หน้า command line)
- [ ] ติดตั้ง dependencies จาก requirements.txt
- [ ] รัน migration สำเร็จ (`db.sqlite3` ถูกสร้าง)
- [ ] รัน development server สำเร็จ
- [ ] เปิดเบราว์เซอร์ที่ http://127.0.0.1:8000/ เห็นหน้าเว็บ
- [ ] หน้า Landing Page แสดงผลถูกต้อง (สไตล์ Smart Farm โทนสีเขียว)

---

## 🎓 เรียนรู้เพิ่มเติม

หลังจาก setup เรียบร้อยแล้ว แนะนำให้อ่านเอกสารเพิ่มเติม:

- 📖 [README.md](README.md) - เอกสารหลักของโปรเจกต์
- 📖 [Day1-DjangoFramework.md](Day1-DjangoFramework.md) - บทเรียน Django พื้นฐาน
- 🌐 [Django Official Documentation](https://docs.djangoproject.com/)

---

## 📞 ติดต่อและรายงานปัญหา

หากพบปัญหาที่ไม่สามารถแก้ไขได้:

1. ตรวจสอบ [Issues](https://github.com/thaitechzone/myAPP-Django-AIOTs/issues) ใน GitHub
2. สร้าง issue ใหม่พร้อมรายละเอียด error message
3. ระบุ OS, Python version, และขั้นตอนที่ทำมา

---

## 🎉 สำเร็จแล้ว!

ถ้าทำตาม checklist ครบแล้ว คุณพร้อมเริ่มพัฒนาแล้ว!

ขั้นตอนถัดไป:
- ศึกษาโค้ดใน `myapp/views.py` และ `myapp/templates/`
- ลองปรับแต่ง UI ใน `landing.html`
- อ่าน README.md เพื่อเรียนรู้วิธีเพิ่มฟีเจอร์ใหม่

**Happy Coding! 🌱💻**

---

**เอกสารนี้อัพเดทล่าสุด:** April 2026
