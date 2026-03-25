from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import Base, User, Student, Professor, Class, Enrollment, AttendanceRecord
from schemas import LoginRequest, AttendanceCreate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Backend is working"}


@app.get("/attendance")
def get_all_attendance():
    db = SessionLocal()
    records = db.query(AttendanceRecord).all()
    db.close()
    return records


@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password
    ).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }


@app.post("/attendance")
def create_attendance(data: AttendanceCreate):
    db = SessionLocal()

    record = AttendanceRecord(
        student_id=data.student_id,
        class_id=data.class_id,
        timestamp=data.timestamp,
        id_card_status=data.id_card_status,
        fingerprint_status=data.fingerprint_status,
        attendance_status=data.attendance_status,
        device_id=data.device_id
    )

    db.add(record)
    db.commit()
    db.close()

    return {"message": "Attendance saved"}


@app.get("/student/{user_id}")
def get_student_dashboard(user_id: int):
    db = SessionLocal()

    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        db.close()
        raise HTTPException(status_code=404, detail="Student not found")

    records = db.query(AttendanceRecord).filter(
        AttendanceRecord.student_id == student.id
    ).all()
    db.close()

    return {
        "student_name": student.full_name,
        "student_number": student.student_number,
        "attendance": records
    }


@app.get("/professor/{user_id}")
def get_professor_dashboard(user_id: int):
    db = SessionLocal()

    professor = db.query(Professor).filter(Professor.user_id == user_id).first()
    if not professor:
        db.close()
        raise HTTPException(status_code=404, detail="Professor not found")

    classes = db.query(Class).filter(Class.professor_id == professor.id).all()

    result = []
    for c in classes:
        enrollments = db.query(Enrollment).filter(Enrollment.class_id == c.id).all()
        enrolled_count = len(enrollments)

        attendance = db.query(AttendanceRecord).filter(
            AttendanceRecord.class_id == c.id,
            AttendanceRecord.attendance_status == "present"
        ).all()
        attended_count = len(attendance)
        absent_count = enrolled_count - attended_count

        result.append({
            "class_id": c.id,
            "class_name": c.class_name,
            "enrolled_count": enrolled_count,
            "attended_count": attended_count,
            "absent_count": absent_count,
            "summary": f"{attended_count}/{enrolled_count}"
        })

    db.close()
    return {
        "professor_name": professor.full_name,
        "classes": result
    }


@app.get("/gold/{user_id}")
def get_gold_dashboard(user_id: int):
    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id,
        User.role == "gold_user"
    ).first()
    if not user:
        db.close()
        raise HTTPException(status_code=403, detail="Access denied")

    classes = db.query(Class).all()

    result = []
    for c in classes:
        enrollments = db.query(Enrollment).filter(Enrollment.class_id == c.id).all()
        enrolled_count = len(enrollments)

        attendance = db.query(AttendanceRecord).filter(
            AttendanceRecord.class_id == c.id,
            AttendanceRecord.attendance_status == "present"
        ).all()
        attended_count = len(attendance)
        absent_count = enrolled_count - attended_count

        result.append({
            "class_id": c.id,
            "class_name": c.class_name,
            "enrolled_count": enrolled_count,
            "attended_count": attended_count,
            "absent_count": absent_count,
            "summary": f"{attended_count}/{enrolled_count}"
        })

    db.close()
    return {
        "gold_name": "Soud",
        "classes": result
    }


@app.get("/class/{class_id}")
def get_class_details(class_id: int):
    db = SessionLocal()

    selected_class = db.query(Class).filter(Class.id == class_id).first()
    if not selected_class:
        db.close()
        raise HTTPException(status_code=404, detail="Class not found")

    enrollments = db.query(Enrollment).filter(Enrollment.class_id == class_id).all()

    students_data = []
    for enrollment in enrollments:
        student = db.query(Student).filter(Student.id == enrollment.student_id).first()
        attendance = db.query(AttendanceRecord).filter(
            AttendanceRecord.class_id == class_id,
            AttendanceRecord.student_id == student.id
        ).first()

        students_data.append({
            "student_name": student.full_name,
            "student_number": student.student_number,
            "timestamp": attendance.timestamp if attendance else "No record",
            "id_card_status": attendance.id_card_status if attendance else "not found",
            "fingerprint_status": attendance.fingerprint_status if attendance else "not matched",
            "attendance_status": attendance.attendance_status if attendance else "absent",
            "device_id": attendance.device_id if attendance else "-"
        })

    db.close()

    return {
        "class_id": selected_class.id,
        "class_name": selected_class.class_name,
        "students": students_data
    }