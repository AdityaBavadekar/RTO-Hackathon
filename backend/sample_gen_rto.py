import random
import string

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_email():
    return f"{random_string(8)}@{random.choice(['gmail.com', 'yahoo.com', 'example.com'])}"

def random_phone_number():
    return f"+91{random.randint(6000000000, 9999999999)}"

def random_lat_long():
    return round(random.uniform(-90, 90), 6), round(random.uniform(-180, 180), 6)

def random_website():
    return f"https://{random_string(5).lower()}.com"

def random_office_hours():
    return f"{random.randint(9, 11)}:00 AM - {random.randint(5, 7)}:00 PM"

def generate_rto_metadata():
    return {
        "office_type": random.choice(["Regional", "District", "Central"]),
        "established_year": random.randint(1970, 2025),
        "services": random.sample(
            ["Licensing", "Vehicle Registration", "Road Tax Collection", "Permits"], 
            random.randint(1, 4)
        ),
    }

def generate_sample_rto():
    lat, long = random_lat_long()
    username = random_string(8)
    return {
        "username": username,
        "password": username,
        "rto_name": f"RTO {random_string(5)}",
        "rto_address": f"{random.randint(100, 999)} {random.choice(['Main St', 'Park Ave', 'Oak Rd'])}, City {random.randint(1, 100)}",
        "rto_lat": lat,
        "rto_long": long,
        "rto_website": random_website(),
        "rto_main_email": random_email(),
        "rto_contact_number": random_phone_number(),
        "rto_office_hours": random_office_hours(),
        "rto_report_to_mails": [random_email() for _ in range(random.randint(1, 3))],
        "rto_metadata": generate_rto_metadata(),
    }
    
def send_post():
    import requests
    print("------------------------------------------")
    print("Sending POST request...")
    sample_data = generate_sample_rto()
    url = "http://127.0.0.1:8000/api/rto/auth/register"
    response = requests.post(url, json=sample_data)
    print(response.json())
    # print(sample_data)
    print("------------------------------------------")


if __name__ == "__main__":
    for _ in range(5): send_post()