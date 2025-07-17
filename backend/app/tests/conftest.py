# conftest.py
import pytest
from app import create_app  # หรือ app_factory ถ้าคุณเปลี่ยนชื่อไฟล์
from models import User, Note  # ✅ Import models โดยตรง

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGODB_SETTINGS'] = {
        'db': 'daily_note',
        'host': 'mongodb+srv://baramee:baramee123@job6.qyctu.mongodb.net/',
        'port': 27017
    }

    with app.test_client() as client:
        with app.app_context():
            # ไม่มี db.init_app() สำหรับ mongoengine
            User.objects.delete()
            Note.objects.delete()
        yield client
