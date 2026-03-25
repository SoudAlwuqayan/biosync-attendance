from database import SessionLocal, engine
from models import Base, User, Student, Professor, Class, Enrollment, AttendanceRecord

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear old data
db.query(AttendanceRecord).delete()
db.query(Enrollment).delete()
db.query(Class).delete()
db.query(Student).delete()
db.query(Professor).delete()
db.query(User).delete()
db.commit()

# Users
student_user_1 = User(email="student1@sdsu.edu", password="1234", role="student")
student_user_2 = User(email="student2@sdsu.edu", password="1234", role="student")
student_user_3 = User(email="student3@sdsu.edu", password="1234", role="student")

professor_user = User(email="raturaj@sdsu.edu", password="1234", role="professor")
gold_user = User(email="soud@sdsu.edu", password="1234", role="gold_user")

db.add_all([student_user_1, student_user_2, student_user_3, professor_user, gold_user])
db.commit()

db.refresh(student_user_1)
db.refresh(student_user_2)
db.refresh(student_user_3)
db.refresh(professor_user)
db.refresh(gold_user)

# Students
student1 = Student(user_id=student_user_1.id, full_name="Ali Hassan", student_number="1001")
student2 = Student(user_id=student_user_2.id, full_name="Sara Khalid", student_number="2045")
student3 = Student(user_id=student_user_3.id, full_name="Omar Salem", student_number="3012")

# Professor
professor = Professor(user_id=professor_user.id, full_name="Raturaj")

db.add_all([student1, student2, student3, professor])
db.commit()

db.refresh(student1)
db.refresh(student2)
db.refresh(student3)
db.refresh(professor)

# Classes
class1 = Class(class_name="COMPE 491 - Senior Design", professor_id=professor.id)
class2 = Class(class_name="EE 425 - Embedded Systems", professor_id=professor.id)
class3 = Class(class_name="COMPE 470 - Digital Circuits", professor_id=professor.id)

db.add_all([class1, class2, class3])
db.commit()

db.refresh(class1)
db.refresh(class2)
db.refresh(class3)

# Enrollments
enrollments = [
    Enrollment(student_id=student1.id, class_id=class1.id),
    Enrollment(student_id=student2.id, class_id=class1.id),
    Enrollment(student_id=student3.id, class_id=class1.id),

    Enrollment(student_id=student1.id, class_id=class2.id),
    Enrollment(student_id=student2.id, class_id=class3.id),
]

db.add_all(enrollments)
db.commit()

# Attendance records
attendance_records = [
    AttendanceRecord(
        student_id=student1.id,
        class_id=class1.id,
        timestamp="2026-03-24 10:30",
        id_card_status="found",
        fingerprint_status="matched",
        attendance_status="present",
        device_id="ESP32_01"
    ),
    AttendanceRecord(
        student_id=student2.id,
        class_id=class1.id,
        timestamp="2026-03-24 10:32",
        id_card_status="found",
        fingerprint_status="matched",
        attendance_status="present",
        device_id="ESP32_01"
    ),
    AttendanceRecord(
        student_id=student3.id,
        class_id=class1.id,
        timestamp="2026-03-24 10:35",
        id_card_status="found",
        fingerprint_status="not matched",
        attendance_status="absent",
        device_id="ESP32_01"
    ),
    AttendanceRecord(
        student_id=student1.id,
        class_id=class2.id,
        timestamp="2026-03-24 12:00",
        id_card_status="found",
        fingerprint_status="matched",
        attendance_status="present",
        device_id="ESP32_02"
    ),
]

db.add_all(attendance_records)
db.commit()

db.close()

print("Seed data inserted successfully.")