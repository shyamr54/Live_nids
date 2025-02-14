import React, { useState, useEffect } from "react";

function Dashboard() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.intrusion === 1) {
        setAlerts((prev) => [...prev, "🚨 Intrusion Detected!"]);
      }
    };

    return () => ws.close();
  }, []);

  return (
    <div>
      <h1>Intrusion Detection Dashboard</h1>
      <ul>
        {alerts.map((alert, idx) => (
          <li key={idx}>{alert}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
