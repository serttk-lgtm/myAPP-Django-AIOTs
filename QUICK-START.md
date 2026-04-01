# ⚡ Quick Start - myAPP-Django-AIOTs

เอกสารฉบับย่อสำหรับ Clone และรันโปรเจกต์อย่างรวดเร็ว

---

## 🚀 สำหรับผู้ใช้ครั้งแรก (First Time Setup)

```cmd
git clone https://github.com/thaitechzone/myAPP-Django-AIOTs.git
cd myAPP-Django-AIOTs
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

🌐 **เปิดเบราว์เซอร์:** http://127.0.0.1:8000/

---

## 💻 สำหรับใช้งานประจำวัน (Daily Use)

หลังจาก setup แล้ว เมื่อเปิด terminal ใหม่ทุกครั้ง:

```cmd
cd myAPP-Django-AIOTs
venv\Scripts\activate.bat
python manage.py runserver
```

🛑 **หยุด Server:** `Ctrl+C`

---

## 🔧 คำสั่งที่ใช้บ่อย

```cmd
REM Activate virtual environment (ต้องทำทุกครั้งที่เปิด terminal ใหม่)
venv\Scripts\activate.bat

REM รัน development server
python manage.py runserver

REM รัน server ที่ port อื่น
python manage.py runserver 8080

REM สร้าง migration
python manage.py makemigrations

REM ใช้ migration
python manage.py migrate

REM สร้าง superuser (สำหรับ admin panel)
python manage.py createsuperuser

REM เปิด Python shell (Django)
python manage.py shell

REM ติดตั้ง package ใหม่และบันทึก
pip install <package_name>
pip freeze > requirements.txt

REM ดู package ที่ติดตั้งแล้ว
pip list

REM อัพเดท package
pip install --upgrade <package_name>
```

---

## 🆘 แก้ปัญหาด่วน

### ❌ Python ไม่พบ
ใช้ `py` แทน `python`:
```cmd
py -m venv venv
py manage.py runserver
```

### ❌ ModuleNotFoundError
```cmd
REM ตรวจสอบว่า activate venv แล้ว (ต้องเห็น (venv) หน้า command line)
pip install -r requirements.txt
```

### ❌ Port 8000 ใช้งานไม่ได้
```cmd
python manage.py runserver 8080
```

### ❌ Database Error
```cmd
del db.sqlite3
python manage.py migrate
```

---

## 📂 โครงสร้างโปรเจกต์

```
myAPP-Django-AIOTs/
├── venv/                    # Virtual environment
├── myproject/               # Django project settings
│   ├── settings.py
│   └── urls.py
├── myapp/                   # Django app
│   ├── templates/
│   │   └── myapp/
│   │       └── landing.html
│   └── views.py
├── manage.py               # Django management command
├── db.sqlite3              # SQLite database
├── requirements.txt        # Python dependencies
├── README.md               # เอกสารหลัก
├── SETUP-GUIDE.md          # คู่มือ setup ฉบับเต็ม
└── QUICK-START.md          # ไฟล์นี้
```

---

## 📚 เอกสารเพิ่มเติม

- 📖 [README.md](README.md) - เอกสารหลักของโปรเจกต์
- 📖 [SETUP-GUIDE.md](SETUP-GUIDE.md) - คู่มือ setup ฉบับเต็มพร้อมวิธีแก้ปัญหา
- 📖 [Day1-DjangoFramework.md](Day1-DjangoFramework.md) - บทเรียน Django

---

## ✅ Checklist

- [ ] Clone repository
- [ ] สร้าง virtual environment
- [ ] Activate venv (เห็น `(venv)` หน้า command line)
- [ ] ติดตั้ง dependencies
- [ ] รัน migration
- [ ] รัน server
- [ ] เปิดเบราว์เซอร์ที่ http://127.0.0.1:8000/

---

**ติดปัญหา?** อ่านคู่มือฉบับเต็มที่ [SETUP-GUIDE.md](SETUP-GUIDE.md)

**Happy Coding! 🌱💻**
