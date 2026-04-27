import psycopg2
import requests
import json
import time
from datetime import datetime

# Connection Configuration
PG_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "de_telemetry",
    "user": "de_admin",
    "password": "DeAdmin2026!"
}

HEC_URL = "https://localhost:8088/services/collector/event"
HEC_TOKEN = "f9d0f92a-fcad-4a02-a76e-0b9a325cffe8"

def forward_alerts():
    try:
        # Connect to Postgres
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()
        
        # Query recent alerts
        query = """
            SELECT alert_id, endpoint_id, severity, message, created_at 
            FROM telemetry.alerts 
            ORDER BY created_at DESC 
            LIMIT 100
        """
        cur.execute(query)
        rows = cur.fetchall()
        
        events = []
        for row in rows:
            alert_id, endpoint_id, severity, message, created_at = row
            
            # Convert timestamp to Unix epoch
            unix_time = time.mktime(created_at.timetuple())
            
            # Construct Splunk Event
            payload = {
                "time": unix_time,
                "source": "citi_telemetry_postgres",
                "sourcetype": "citi_alert",
                "event": {
                    "alert_id": alert_id,
                    "endpoint_id": endpoint_id,
                    "severity": severity,
                    "message": message,
                    "created_at": created_at.isoformat()
                }
            }
            # Add to batch (newline separated for bulk API)
            events.append(json.dumps(payload))
        
        # Batch send (10 events per POST)
        batch_size = 10
        for i in range(0, len(events), batch_size):
            batch = "\n".join(events[i:i+batch_size])
            headers = {"Authorization": f"Splunk {HEC_TOKEN}"}
            response = requests.post(HEC_URL, headers=headers, data=batch, verify=False)
            response.raise_for_status()

        print(f"Sent {len(events)} events to Splunk")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    forward_alerts()
