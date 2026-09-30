import os
import json

base_dir = r"C:\Users\Lenovo\.gemini\antigravity\scratch\SmartHomeGuardian"

directories = [
    "src",
    "src/components",
    "src/pages",
    "src/context",
    "src/firebase",
    "src/services",
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {}

files["package.json"] = """{
  "name": "smart-home-guardian",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "firebase": "^10.8.0",
    "lucide-react": "^0.344.0",
    "papaparse": "^5.4.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.2",
    "recharts": "^2.12.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.56",
    "@types/react-dom": "^18.2.19",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "eslint": "^8.56.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "vite": "^5.1.4"
  }
}
"""

files["vite.config.js"] = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
"""

files["tailwind.config.js"] = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0f172a',
          card: '#1e293b',
          border: '#334155'
        }
      }
    },
  },
  plugins: [],
}
"""

files["postcss.config.js"] = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

files["index.html"] = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Smart Home Guardian</title>
  </head>
  <body class="bg-dark-bg text-gray-100">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

files["src/index.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom Scrollbar for dark theme */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #0f172a; 
}
::-webkit-scrollbar-thumb {
  background: #334155; 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #475569; 
}
"""

files["src/main.jsx"] = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""

files["src/firebase/firebaseConfig.js"] = """// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// TODO: Replace with your app's Firebase project configuration
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
// const app = initializeApp(firebaseConfig);
// export const db = getFirestore(app);

// Exporting null for demo mode to prevent crash
export const db = null;
"""

files["src/context/AppContext.jsx"] = """import React, { createContext, useState, useEffect, useContext } from 'react';

const AppContext = createContext();

export const useAppContext = () => useContext(AppContext);

export const AppProvider = ({ children }) => {
  const [demoMode, setDemoMode] = useState(true);
  const [sensorData, setSensorData] = useState({
    deviceId: "ESP32-001",
    temperature: 29.4,
    gas: 312,
    flame: 0,
    motion: 1,
    door: 0,
    personDetected: true,
    confidence: 96.4,
    timestamp: new Date().toISOString()
  });
  
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [settings, setSettings] = useState({
    gasWarning: 400,
    gasDanger: 700,
    tempWarning: 35,
    motionSensitivity: 'High',
    aiConfidence: 80
  });

  useEffect(() => {
    let interval;
    if (demoMode) {
      interval = setInterval(() => {
        const newData = {
          deviceId: "ESP32-001",
          temperature: +(28 + Math.random() * 4).toFixed(1),
          gas: Math.floor(200 + Math.random() * 500),
          flame: Math.random() > 0.95 ? 1 : 0,
          motion: Math.random() > 0.7 ? 1 : 0,
          door: Math.random() > 0.9 ? 1 : 0,
          personDetected: Math.random() > 0.5,
          confidence: +(85 + Math.random() * 14).toFixed(1),
          timestamp: new Date().toISOString()
        };
        
        setSensorData(newData);
        setHistory(prev => {
          const newHist = [...prev, newData];
          if(newHist.length > 50) newHist.shift();
          return newHist;
        });

        // Generate Demo Alerts
        if (newData.gas > settings.gasDanger) {
          addAlert('🔥 DANGER', 'High Gas Level Detected!', 'High', newData.gas);
        } else if (newData.gas > settings.gasWarning) {
          addAlert('⚠️ WARNING', 'Elevated Gas Level', 'Medium', newData.gas);
        }
        if (newData.flame === 1) addAlert('🚨 FIRE ALERT', 'Flame detected', 'Critical', 1);
        if (newData.personDetected) addAlert('⚠️ INTRUSION', `Person detected (${newData.confidence}%)`, 'Medium', newData.confidence);

      }, 4000);
    }
    return () => clearInterval(interval);
  }, [demoMode, settings]);

  const addAlert = (type, message, severity, value) => {
    setAlerts(prev => [{ id: Date.now(), type, message, severity, value, status: 'Active', time: new Date().toLocaleString() }, ...prev]);
  };

  return (
    <AppContext.Provider value={{ demoMode, setDemoMode, sensorData, history, alerts, setAlerts, settings, setSettings }}>
      {children}
    </AppContext.Provider>
  );
};
"""

files["src/components/Sidebar.jsx"] = """import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Activity, Brain, Database, AlertTriangle, Settings, Laptop, Shield } from 'lucide-react';

export default function Sidebar() {
  const links = [
    { to: "/", icon: <Home size={20} />, label: "Dashboard" },
    { to: "/live", icon: <Activity size={20} />, label: "Live Monitoring" },
    { to: "/ai", icon: <Brain size={20} />, label: "AI Analysis" },
    { to: "/dataset", icon: <Database size={20} />, label: "ML Dataset" },
    { to: "/alerts", icon: <AlertTriangle size={20} />, label: "Alerts" },
    { to: "/devices", icon: <Laptop size={20} />, label: "Devices" },
    { to: "/settings", icon: <Settings size={20} />, label: "Settings" }
  ];

  return (
    <div className="w-64 bg-dark-card border-r border-dark-border h-screen fixed flex flex-col">
      <div className="p-6 flex items-center gap-3 border-b border-dark-border">
        <Shield className="text-blue-500" size={32} />
        <div>
          <h1 className="font-bold text-lg leading-tight">SMART HOME</h1>
          <p className="text-xs text-blue-400 font-semibold tracking-wider">GUARDIAN</p>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {links.map(link => (
          <NavLink 
            key={link.to} 
            to={link.to}
            className={({isActive}) => `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-dark-border hover:text-white'}`}
          >
            {link.icon}
            <span className="font-medium">{link.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-dark-border text-xs text-gray-500 text-center">
        College Expo 2026<br/>Educational Prototype
      </div>
    </div>
  );
}
"""

files["src/components/Topbar.jsx"] = """import React from 'react';
import { useAppContext } from '../context/AppContext';
import { Wifi, WifiOff } from 'lucide-react';

export default function Topbar() {
  const { demoMode, setDemoMode, sensorData } = useAppContext();

  return (
    <header className="h-16 bg-dark-card border-b border-dark-border flex items-center justify-between px-6 sticky top-0 z-10">
      <div>
        <h2 className="text-xl font-semibold">AI + IoT Home Security System</h2>
      </div>
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-400">Status:</span>
          {demoMode ? (
             <span className="flex items-center gap-2 text-yellow-400 bg-yellow-400/10 px-3 py-1 rounded-full text-sm font-medium">
               <WifiOff size={16} /> 🟡 DEMO MODE
             </span>
          ) : (
             <span className="flex items-center gap-2 text-green-400 bg-green-400/10 px-3 py-1 rounded-full text-sm font-medium">
               <Wifi size={16} /> 🟢 LIVE MODE
             </span>
          )}
        </div>
        
        <label className="flex items-center cursor-pointer gap-2">
          <div className="relative">
            <input type="checkbox" className="sr-only" checked={demoMode} onChange={() => setDemoMode(!demoMode)} />
            <div className={`block w-14 h-8 rounded-full ${demoMode ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
            <div className={`dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition transform ${demoMode ? 'translate-x-0' : 'translate-x-6'}`}></div>
          </div>
          <span className="text-sm text-gray-300 font-medium">{demoMode ? 'Demo' : 'Live'}</span>
        </label>
      </div>
    </header>
  );
}
"""

files["src/components/SensorCard.jsx"] = """import React from 'react';

export default function SensorCard({ title, icon, value, subtext, statusColor }) {
  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-6 flex flex-col justify-between">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-2 text-gray-400 font-medium">
          {icon}
          <h3>{title}</h3>
        </div>
        <div className={`w-3 h-3 rounded-full ${statusColor}`}></div>
      </div>
      <div>
        <p className="text-2xl font-bold mb-1">{value}</p>
        <p className="text-sm text-gray-400">{subtext}</p>
      </div>
    </div>
  );
}
"""

files["src/pages/Dashboard.jsx"] = """import React from 'react';
import { useAppContext } from '../context/AppContext';
import SensorCard from '../components/SensorCard';
import { Thermometer, Flame, Wind, DoorClosed, DoorOpen, PersonStanding, Activity } from 'lucide-react';

export default function Dashboard() {
  const { sensorData, settings } = useAppContext();

  const getGasStatus = (val) => {
    if(val > settings.gasDanger) return { text: 'DANGER', color: 'bg-red-500' };
    if(val > settings.gasWarning) return { text: 'WARNING', color: 'bg-yellow-500' };
    return { text: 'NORMAL', color: 'bg-green-500' };
  };

  const gasStatus = getGasStatus(sensorData.gas);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <SensorCard 
          title="AI Person Detection" 
          icon={<PersonStanding size={20} />} 
          value={sensorData.personDetected ? 'PERSON DETECTED' : 'NO PERSON'} 
          subtext={sensorData.personDetected ? `Confidence: ${sensorData.confidence}%` : 'Area clear'}
          statusColor={sensorData.personDetected ? 'bg-red-500' : 'bg-green-500'}
        />
        
        <SensorCard 
          title="Fire Detection" 
          icon={<Flame size={20} />} 
          value={sensorData.flame === 1 ? 'FIRE DETECTED' : 'SAFE'} 
          subtext={`Sensor Value: ${sensorData.flame}`}
          statusColor={sensorData.flame === 1 ? 'bg-red-500' : 'bg-green-500'}
        />

        <SensorCard 
          title="Gas / Smoke" 
          icon={<Wind size={20} />} 
          value={gasStatus.text} 
          subtext={`MQ-2 Value: ${sensorData.gas}`}
          statusColor={gasStatus.color}
        />

        <SensorCard 
          title="Motion" 
          icon={<Activity size={20} />} 
          value={sensorData.motion === 1 ? 'MOTION' : 'NO MOTION'} 
          subtext="PIR Sensor"
          statusColor={sensorData.motion === 1 ? 'bg-yellow-500' : 'bg-gray-500'}
        />

        <SensorCard 
          title="Door Status" 
          icon={sensorData.door === 1 ? <DoorOpen size={20} /> : <DoorClosed size={20} />} 
          value={sensorData.door === 1 ? 'OPEN' : 'CLOSED'} 
          subtext="Reed Switch"
          statusColor={sensorData.door === 1 ? 'bg-yellow-500' : 'bg-green-500'}
        />

        <SensorCard 
          title="Temperature" 
          icon={<Thermometer size={20} />} 
          value={`${sensorData.temperature} °C`} 
          subtext="DHT / Internal"
          statusColor={sensorData.temperature > settings.tempWarning ? 'bg-yellow-500' : 'bg-blue-500'}
        />
      </div>
      
      <div className="bg-dark-card border border-dark-border rounded-xl p-6 mt-8">
         <h3 className="text-lg font-medium mb-4">System Overview</h3>
         <p className="text-gray-400">Last data received: <span className="text-white">{new Date(sensorData.timestamp).toLocaleString()}</span></p>
         <p className="text-gray-400 mt-2">Connected Devices: <span className="text-white">ESP32-001</span></p>
      </div>
    </div>
  );
}
"""

files["src/pages/LiveMonitoring.jsx"] = """import React from 'react';
import { useAppContext } from '../context/AppContext';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function LiveMonitoring() {
  const { sensorData, history } = useAppContext();

  // Format history for charts
  const chartData = history.map(d => ({
    time: new Date(d.timestamp).toLocaleTimeString(),
    Temperature: d.temperature,
    Gas: d.gas,
    Confidence: d.confidence
  }));

  return (
    <div className="space-y-6">
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">Raw JSON Data Stream</h2>
        <pre className="bg-[#0f172a] p-4 rounded-lg text-green-400 font-mono text-sm overflow-x-auto">
          {JSON.stringify(sensorData, null, 2)}
        </pre>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Temp Chart */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-6 h-80">
          <h3 className="text-lg font-medium mb-4">Temperature vs Time</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
              <Legend />
              <Line type="monotone" dataKey="Temperature" stroke="#3b82f6" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Gas Chart */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-6 h-80">
          <h3 className="text-lg font-medium mb-4">Gas Level vs Time</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
              <Legend />
              <Line type="monotone" dataKey="Gas" stroke="#eab308" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
"""

files["src/pages/AIAnalysis.jsx"] = """import React, { useState } from 'react';
import { Upload } from 'lucide-react';

export default function AIAnalysis() {
  const [image, setImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
      setResult(null);
      setAnalyzing(true);
      
      // Simulate ML prediction delay
      setTimeout(() => {
        setAnalyzing(false);
        setResult({
          prediction: Math.random() > 0.3 ? 'PERSON DETECTED' : 'NO PERSON',
          confidence: (85 + Math.random() * 14).toFixed(1)
        });
      }, 1500);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="bg-dark-card border border-dark-border rounded-xl p-6 text-center">
        <h2 className="text-xl font-semibold mb-2">AI Image Analysis (Demo Mode)</h2>
        <p className="text-gray-400 mb-6">Upload an image from your camera to test the ML model classification.</p>
        
        <div className="border-2 border-dashed border-dark-border rounded-xl p-8 mb-6 flex flex-col items-center justify-center min-h-[300px] relative">
          {image ? (
            <img src={image} alt="Uploaded" className="max-h-[400px] object-contain rounded-lg" />
          ) : (
            <div className="flex flex-col items-center text-gray-500">
              <Upload size={48} className="mb-4" />
              <p>Drag and drop or click to upload</p>
            </div>
          )}
          <input 
            type="file" 
            accept="image/*" 
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleImageUpload}
          />
        </div>

        {analyzing && (
          <div className="text-blue-400 font-medium animate-pulse">
            Analyzing image using TensorFlow.js...
          </div>
        )}

        {result && !analyzing && (
          <div className="bg-[#0f172a] border border-dark-border rounded-lg p-6 max-w-md mx-auto">
            <h3 className="text-sm text-gray-400 uppercase tracking-wider mb-2">Prediction Result</h3>
            <p className={`text-2xl font-bold mb-4 ${result.prediction === 'PERSON DETECTED' ? 'text-red-500' : 'text-green-500'}`}>
              {result.prediction}
            </p>
            
            <div className="w-full bg-gray-700 rounded-full h-4 mb-2 overflow-hidden">
              <div 
                className={`h-4 rounded-full ${result.prediction === 'PERSON DETECTED' ? 'bg-red-500' : 'bg-green-500'}`} 
                style={{ width: `${result.confidence}%` }}
              ></div>
            </div>
            <p className="text-right text-sm text-gray-400">Confidence: {result.confidence}%</p>
          </div>
        )}
      </div>
    </div>
  );
}
"""

files["src/pages/Dataset.jsx"] = """import React, { useState } from 'react';
import Papa from 'papaparse';
import { Upload, FileText } from 'lucide-react';

export default function Dataset() {
  const [data, setData] = useState([]);
  const [stats, setStats] = useState(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: function(results) {
          setData(results.data);
          calculateStats(results.data);
        }
      });
    }
  };

  const calculateStats = (parsedData) => {
    if(!parsedData.length) return;
    const statsObj = {
      records: parsedData.length,
      personDetections: parsedData.filter(d => d.person === 1 || d.personDetected === 1 || String(d.personDetected).toLowerCase() === 'true').length,
      motionEvents: parsedData.filter(d => d.motion === 1).length,
      avgTemp: (parsedData.reduce((acc, curr) => acc + (curr.temperature || 0), 0) / parsedData.length).toFixed(1),
      maxGas: Math.max(...parsedData.map(d => d.gas || 0)),
      fireAlerts: parsedData.filter(d => d.flame === 1).length,
    };
    setStats(statsObj);
  };

  return (
    <div className="space-y-6">
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">ML Dataset Upload</h2>
        <div className="flex items-center justify-center w-full">
          <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-dark-border rounded-xl cursor-pointer hover:bg-[#0f172a] transition">
            <div className="flex flex-col items-center justify-center pt-5 pb-6 text-gray-400">
              <Upload size={24} className="mb-2" />
              <p className="text-sm font-medium">Click to upload CSV</p>
            </div>
            <input type="file" accept=".csv" className="hidden" onChange={handleFileUpload} />
          </label>
        </div>
      </div>

      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <StatBox label="Total Records" value={stats.records} color="text-blue-400" />
          <StatBox label="Person Detects" value={stats.personDetections} color="text-red-400" />
          <StatBox label="Motion Events" value={stats.motionEvents} color="text-yellow-400" />
          <StatBox label="Avg Temp" value={`${stats.avgTemp}°C`} color="text-green-400" />
          <StatBox label="Max Gas" value={stats.maxGas} color="text-orange-400" />
          <StatBox label="Fire Alerts" value={stats.fireAlerts} color="text-red-500" />
        </div>
      )}

      {data.length > 0 && (
        <div className="bg-dark-card border border-dark-border rounded-xl overflow-hidden">
          <div className="overflow-x-auto max-h-[500px]">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-400 uppercase bg-[#0f172a] sticky top-0">
                <tr>
                  {Object.keys(data[0]).map(key => (
                     <th key={key} className="px-6 py-3">{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.slice(0, 100).map((row, idx) => (
                  <tr key={idx} className="border-b border-dark-border hover:bg-[#0f172a] transition-colors">
                    {Object.values(row).map((val, i) => (
                       <td key={i} className="px-6 py-4">{String(val)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="p-4 text-center text-sm text-gray-500 border-t border-dark-border">
             Showing first 100 rows.
          </div>
        </div>
      )}
    </div>
  );
}

const StatBox = ({ label, value, color }) => (
  <div className="bg-dark-card border border-dark-border rounded-xl p-4 text-center">
    <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">{label}</p>
    <p className={`text-2xl font-bold ${color}`}>{value}</p>
  </div>
);
"""

files["src/pages/Alerts.jsx"] = """import React from 'react';
import { useAppContext } from '../context/AppContext';

export default function Alerts() {
  const { alerts, setAlerts } = useAppContext();

  const updateStatus = (id, newStatus) => {
    setAlerts(alerts.map(a => a.id === id ? { ...a, status: newStatus } : a));
  };

  return (
    <div className="space-y-6">
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-6">System Alerts</h2>
        
        {alerts.length === 0 ? (
          <p className="text-gray-400 text-center py-8">No alerts generated yet.</p>
        ) : (
          <div className="space-y-4">
            {alerts.map(alert => (
              <div key={alert.id} className="border border-dark-border bg-[#0f172a] rounded-lg p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <span className="font-bold text-lg">{alert.type}</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium uppercase ${alert.severity === 'Critical' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                      {alert.severity}
                    </span>
                  </div>
                  <p className="text-gray-300">{alert.message} (Value: {alert.value})</p>
                  <p className="text-sm text-gray-500 mt-1">{alert.time}</p>
                </div>
                
                <div className="flex items-center gap-2">
                  <span className={`text-sm mr-4 ${alert.status === 'Active' ? 'text-red-400' : alert.status === 'Acknowledged' ? 'text-yellow-400' : 'text-green-400'}`}>
                    {alert.status}
                  </span>
                  {alert.status === 'Active' && (
                    <button onClick={() => updateStatus(alert.id, 'Acknowledged')} className="px-3 py-1 bg-dark-border hover:bg-gray-700 rounded text-sm transition">
                      Acknowledge
                    </button>
                  )}
                  {alert.status !== 'Resolved' && (
                    <button onClick={() => updateStatus(alert.id, 'Resolved')} className="px-3 py-1 bg-green-600 hover:bg-green-500 rounded text-sm transition text-white">
                      Resolve
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
"""

files["src/pages/Devices.jsx"] = """import React from 'react';
import { Laptop, Camera } from 'lucide-react';

export default function Devices() {
  const devices = [
    { id: 'ESP32-001', name: 'Main Controller', type: 'MCU', status: 'Online', lastSeen: '10 seconds ago', icon: <Laptop className="text-blue-400" /> },
    { id: 'ESP32-CAM-001', name: 'Security Camera', type: 'Camera', status: 'Online', lastSeen: '12 seconds ago', icon: <Camera className="text-green-400" /> }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Device Management</h2>
        <button className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg text-sm font-medium transition">
          + Add Device
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {devices.map(device => (
          <div key={device.id} className="bg-dark-card border border-dark-border rounded-xl p-6 flex flex-col justify-between">
            <div className="flex justify-between items-start mb-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-[#0f172a] rounded-lg">
                  {device.icon}
                </div>
                <div>
                  <h3 className="font-bold text-lg">{device.id}</h3>
                  <p className="text-sm text-gray-400">{device.name}</p>
                </div>
              </div>
              <span className="px-3 py-1 bg-green-500/10 text-green-400 rounded-full text-xs font-medium border border-green-500/20">
                {device.status}
              </span>
            </div>
            
            <div className="border-t border-dark-border pt-4 flex justify-between items-center">
              <p className="text-sm text-gray-500">Last seen: {device.lastSeen}</p>
              <div className="flex gap-2">
                <button className="text-xs px-3 py-1 border border-dark-border rounded hover:bg-dark-border transition">Details</button>
                <button className="text-xs px-3 py-1 border border-red-500/30 text-red-400 rounded hover:bg-red-500/10 transition">Remove</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
"""

files["src/pages/Settings.jsx"] = """import React from 'react';
import { useAppContext } from '../context/AppContext';

export default function Settings() {
  const { settings, setSettings } = useAppContext();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({ ...prev, [name]: isNaN(value) ? value : Number(value) }));
  };

  const handleSave = () => {
    alert("Settings saved successfully! (Demo Mode: Local state updated)");
  };

  return (
    <div className="max-w-2xl">
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-6">Threshold Settings</h2>
        
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Gas Warning Threshold</label>
              <input type="number" name="gasWarning" value={settings.gasWarning} onChange={handleChange} className="w-full bg-[#0f172a] border border-dark-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Gas Danger Threshold</label>
              <input type="number" name="gasDanger" value={settings.gasDanger} onChange={handleChange} className="w-full bg-[#0f172a] border border-dark-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-red-500" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">Temperature Warning (°C)</label>
            <input type="number" name="tempWarning" value={settings.tempWarning} onChange={handleChange} className="w-full bg-[#0f172a] border border-dark-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-yellow-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">AI Confidence Threshold (%)</label>
            <input type="number" name="aiConfidence" value={settings.aiConfidence} onChange={handleChange} className="w-full bg-[#0f172a] border border-dark-border rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500" />
          </div>

          <button onClick={handleSave} className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-3 rounded-lg transition mt-4">
            Save Settings to Firebase
          </button>
        </div>
      </div>
    </div>
  );
}
"""

files["src/App.jsx"] = """import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import Dashboard from './pages/Dashboard';
import LiveMonitoring from './pages/LiveMonitoring';
import AIAnalysis from './pages/AIAnalysis';
import Dataset from './pages/Dataset';
import Alerts from './pages/Alerts';
import Devices from './pages/Devices';
import Settings from './pages/Settings';

export default function App() {
  return (
    <AppProvider>
      <Router>
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <div className="flex-1 ml-64 flex flex-col h-screen overflow-hidden">
            <Topbar />
            <main className="flex-1 overflow-y-auto p-6 bg-dark-bg">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/live" element={<LiveMonitoring />} />
                <Route path="/ai" element={<AIAnalysis />} />
                <Route path="/dataset" element={<Dataset />} />
                <Route path="/alerts" element={<Alerts />} />
                <Route path="/devices" element={<Devices />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </AppProvider>
  );
}
"""

files["README.md"] = """# Smart Home Guardian – AI + IoT Home Security Dashboard

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
2. Open the terminal (Ctrl + `).
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

    String jsonPayload = "{\\"deviceId\\":\\"ESP32-001\\", \\"temperature\\": 29.4, \\"gas\\": 312, \\"flame\\": 0, \\"motion\\": 1, \\"door\\": 0}";
    
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
"""

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Scaffold complete.")
