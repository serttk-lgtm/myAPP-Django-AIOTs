"""
สคริปต์สำหรับลบข้อมูล TelemetryLog ที่ซ้ำกัน
รัน: python cleanup_duplicates.py
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import TelemetryLog
from django.db.models import Count

def cleanup_duplicates():
    """ลบ TelemetryLog entries ที่มีข้อมูลเหมือนกันทุกอย่าง (ยกเว้น id)"""
    
    print("🔍 กำลังค้นหาข้อมูลซ้ำ...")
    
    # หา TelemetryLog ที่มีค่าเหมือนกันทั้ง device, rssi, created_at
    # และเก็บเฉพาะรายการแรก ลบที่เหลือทิ้ง
    
    all_logs = TelemetryLog.objects.all().order_by('created_at')
    total_count = all_logs.count()
    
    print(f"📊 พบข้อมูลทั้งหมด: {total_count} รายการ")
    
    # Group by device + created_at (ถือว่าข้อมูลที่มาพร้อมกันคือซ้ำ)
    seen_combinations = set()
    duplicates_to_delete = []
    
    for log in all_logs:
        # สร้าง key จาก device_id, created_at (ปัดเศษวินาที), rssi, sensor_data
        key = (
            log.device_id,
            log.created_at.replace(microsecond=0),  # ใช้เวลาเดียวกัน
            log.rssi,
            str(log.sensor_data),
            str(log.relay_status)
        )
        
        if key in seen_combinations:
            # พบข้อมูลซ้ำ
            duplicates_to_delete.append(log.id)
        else:
            seen_combinations.add(key)
    
    duplicate_count = len(duplicates_to_delete)
    
    if duplicate_count == 0:
        print("✅ ไม่พบข้อมูลซ้ำ")
        return
    
    print(f"🗑️  พบข้อมูลซ้ำ: {duplicate_count} รายการ")
    print(f"📝 จะเหลือข้อมูล: {total_count - duplicate_count} รายการ")
    
    # ขอยืนยันก่อนลบ
    confirm = input("\n❓ ต้องการลบข้อมูลซ้ำหรือไม่? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        # ลบข้อมูลซ้ำ
        deleted_count = TelemetryLog.objects.filter(id__in=duplicates_to_delete).delete()[0]
        print(f"✅ ลบข้อมูลซ้ำแล้ว: {deleted_count} รายการ")
        print(f"📊 ข้อมูลคงเหลือ: {TelemetryLog.objects.count()} รายการ")
    else:
        print("❌ ยกเลิกการลบข้อมูล")

if __name__ == '__main__':
    cleanup_duplicates()
