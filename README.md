# Smart Home Guardian – AI + IoT Home Security Dashboard

A complete responsive web application for monitoring a smart home using ESP32 sensors and an AI/ML model, built for a College Expo 2026.

## Features
- Real-time monitoring dashboard
- Historical CSV dataset parsing & stats
- AI/ML demo prediction page
- Live chart rendering (Recharts)
- Threshold-based alert system
- Device & Threshold Management

## How to Run in VS Code

1. Open this folder in VS Code.
2. Open the terminal (`Ctrl + ``).
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
5. Click on the local server link (e.g. `http://localhost:5173`) to view the app in your browser.

## How to Switch from Demo Mode to Live Mode
In the top right corner of the dashboard, you will find a toggle switch. By default, it is in **Demo Mode**, which generates realistic simulated data every 4 seconds. Toggle it to switch to **Live Mode** when you have connected your real ESP32 and Firebase setup.

## How to Connect Firebase
1. Go to the Firebase Console and create a new project.
2. Enable **Firestore Database** and **Authentication**.
3. Create a Web App in Firebase settings and copy the `firebaseConfig` object.
4. Open `src/firebase/firebaseConfig.js`.
5. Replace the placeholder config with your actual config.
6. Uncomment the `initializeApp` and `getFirestore` exports.

## ESP32 HTTP POST Example
To send real sensor data from your ESP32 to this application (via a backend or directly to Firebase Functions/REST API), use the following Arduino IDE code structure:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverName = "http://YOUR_API_ENDPOINT/api/sensor-data"; // Or Firebase Realtime/Firestore REST URL

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"deviceId\":\"ESP32-001\", \"temperature\": 29.4, \"gas\": 312, \"flame\": 0, \"motion\": 1, \"door\": 0}";
    
    int httpResponseCode = http.POST(jsonPayload);
    http.end();
  }
  delay(5000); // Send data every 5 seconds
}
```

## How to connect the ML model later
In `src/pages/AIAnalysis.jsx`, the current setup uses a `setTimeout` to mock a prediction. When you have your TensorFlow.js model ready:
1. Import `@tensorflow/tfjs` and your trained model (e.g. MobileNet or custom Teachable Machine model).
2. Load the model inside a `useEffect`.
3. In the `handleImageUpload` function, pass the image HTML element to `model.predict()`.
4. Replace the random output with the real tensor classification results.
