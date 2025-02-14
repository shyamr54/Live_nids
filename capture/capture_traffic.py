import scapy.all as scapy
import requests
import time

API_URL = "http://127.0.0.1:8000/predict/"

def extract_features(packet):
    """Extracts relevant features from a network packet."""
    try:
        return [
            len(packet),  # ✅ Packet size
            packet.time % 60,  # ✅ Timestamp
            getattr(packet, "ttl", 0),  # ✅ TTL value (default 0 if missing)
            getattr(packet, "window", 0),  # ✅ TCP Window size (default 0 if missing)
            len(packet.payload) if isinstance(packet.payload, scapy.Raw) else 0  # ✅ Payload length (avoid errors)
        ]
    except Exception as e:
        print(f"⚠ Error extracting features: {e}")
        return None  # Return None instead of an empty list

def sniff_packets():
    print("⏳ Monitoring network traffic...")
    while True:
        packets = scapy.sniff(count=10, timeout=5)
        features = [extract_features(pkt) for pkt in packets if extract_features(pkt) is not None]

        if not features:  # 🚨 Ensure we do not send empty data
            print("⚠ No valid packets captured, skipping API call.")
            time.sleep(5)
            continue

        try:
            response = requests.post(API_URL, json={"features": features})
            
            if response.status_code != 200:
                print(f"⚠ API Error: {response.status_code} - {response.text}")
                continue
            
            try:
                prediction = response.json()  # ✅ Parse JSON response
            except requests.exceptions.JSONDecodeError:
                print("⚠ Error: Received invalid JSON from API")
                continue

            if prediction.get("intrusion") == 1:
                print("🚨 Intrusion Detected!")
            else:
                print("✅ No Intrusion Detected")

        except requests.exceptions.RequestException as e:
            print(f"⚠ Connection Error: {e}")

        time.sleep(5)

sniff_packets()
