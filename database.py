import sqlite3

conn = sqlite3.connect("car_prediction.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (

id INTEGER PRIMARY KEY AUTOINCREMENT,

brand TEXT,
model TEXT,
predicted_price INTEGER,

registration_year INTEGER,
vehicle_age INTEGER,
km_driven INTEGER,

fuel_type TEXT,
transmission_type TEXT,
seller_type TEXT,

owner_type TEXT,
car_condition TEXT,
insurance_status TEXT,
accident_history TEXT,

city TEXT,

engine INTEGER,
mileage REAL,
max_power REAL,
seats INTEGER,

date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()
conn.close()

print("Database Created Successfully")