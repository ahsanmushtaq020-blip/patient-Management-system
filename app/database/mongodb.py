from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Atlas URI
uri = "mongodb://Library:Library@cluster0-shard-00-00.xuf76pr.mongodb.net:27017,cluster0-shard-00-01.xuf76pr.mongodb.net:27017,cluster0-shard-00-02.xuf76pr.mongodb.net:27017/?ssl=true&replicaSet=atlas-xxxxx-shard-0&authSource=admin&retryWrites=true&w=majority"

client = None
db = None

try:
    # Initialize Client
    client = MongoClient(uri)

    # Connection test
    client.admin.command("ping")

    print("✅ Connected successfully to MongoDB Atlas!")

    # Database setup
    db = client["patient_db"]

    patient_collection = db["patients"]
    doctor_collection = db["doctors"]
    appointment_collection = db["appointments"]
    user_collection = db["users"]
    prescription_collection = db["prescriptions"]

except Exception as e:
    print(f"❌ Connection failed: {e}")

    patient_collection = None
    doctor_collection = None
    appointment_collection = None
    user_collection = None
    prescription_collection = None


# Optional function
def get_patient():
    return client