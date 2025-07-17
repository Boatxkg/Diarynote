# config.py
class Config:
    SECRET_KEY = 'mongodb+srv://baramee:<db_password>@job6.qyctu.mongodb.net/'
    JWT_SECRET_KEY = 'your-jwt-secret'
    MONGODB_SETTINGS = {
        'db': 'daily_note',
        'host': 'mongodb+srv://baramee:baramee123@job6.qyctu.mongodb.net/',
        'port': 27017
    }   