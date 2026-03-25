from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class AttendanceCreate(BaseModel):
    student_id: int
    class_id: int
    timestamp: str
    id_card_status: str
    fingerprint_status: str
    attendance_status: str
    device_id: str