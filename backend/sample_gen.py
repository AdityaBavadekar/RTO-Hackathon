import base64
import random
import datetime

# Function to generate random latitude and longitude
def random_coordinates():
    return round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6)

# Function to generate a random base64 encoded image string
def generate_base64_image():
    # Example of encoding a small string as base64 for demonstration purposes
    sample_data = b"This is a sample image data"
    return base64.b64encode(sample_data).decode('utf-8')

# Function to generate random metadata
def generate_camera_metadata():
    return {
        "camera_id": f"CAM-{random.randint(1000, 9999)}",
        "resolution": f"{random.choice([720, 1080, 4_000])}p",
        "lens": f"{random.choice(['Wide', 'Standard', 'Telephoto'])} Lens",
        "timestamp": datetime.datetime.now().isoformat(),
    }

# Generate sample data
def generate_sample_incident():
    lat, long = random_coordinates()
    return {
        "incident_location": random.choice(["Park", "School", "Mall", "Unknown"]),
        "incident_lat": lat,
        "incident_long": long,
        "incident_timestamp": datetime.datetime.now().isoformat(),
        "incident_image": generate_base64_image(),
        "incident_camera_metadata": generate_camera_metadata(),
    }
    
def send_post():
    import requests
    print("------------------------------------------")
    print("Sending POST request...")
    sample_data = generate_sample_incident()
    url = "http://127.0.0.1:8000/api/record_incident"
    response = requests.post(url, json=sample_data)
    print(response.json())
    print("------------------------------------------")

if __name__ == "__main__":
    for _ in range(5): send_post()