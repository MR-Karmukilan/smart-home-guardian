const fs = require('fs');
const path = require('path');

const fixers = [
    {
        file: 'src/App.jsx',
        replacements: [['import React from \'react\';\n', '']]
    },
    {
        file: 'src/components/SensorCard.jsx',
        replacements: [['import React from \'react\';\n', '']]
    },
    {
        file: 'src/components/Sidebar.jsx',
        replacements: [['import React from \'react\';\n', '']]
    },
    {
        file: 'src/components/Topbar.jsx',
        replacements: [
            ['import React from \'react\';\n', ''],
            ['const { demoMode, setDemoMode, sensorData } = useAppContext();', 'const { demoMode, setDemoMode } = useAppContext();']
        ]
    },
    {
        file: 'src/context/AppContext.jsx',
        replacements: [
            ['import React, { createContext, useState, useEffect, useContext } from \'react\';', 'import { createContext, useState, useEffect, useContext } from \'react\';']
        ]
    },
    {
        file: 'src/firebase/firebaseConfig.js',
        replacements: [
            ['import { initializeApp } from "firebase/app";', '// import { initializeApp } from "firebase/app";'],
            ['import { getFirestore } from "firebase/firestore";', '// import { getFirestore } from "firebase/firestore";'],
            ['const firebaseConfig', '// const firebaseConfig'],
            ['apiKey:', '// apiKey:'],
            ['authDomain:', '// authDomain:'],
            ['projectId:', '// projectId:'],
            ['storageBucket:', '// storageBucket:'],
            ['messagingSenderId:', '// messagingSenderId:'],
            ['appId:', '// appId:'],
            ['};', '// };']
        ]
    },
    {
        file: 'src/pages/AIAnalysis.jsx',
        replacements: [['import React, { useState } from \'react\';', 'import { useState } from \'react\';']]
    },
    {
        file: 'src/pages/Alerts.jsx',
        replacements: [['import React from \'react\';\n', '']]
    },
    {
        file: 'src/pages/Dashboard.jsx',
        replacements: [
            ['import React from \'react\';\n', ''],
            ['const { sensorData, settings } = useAppContext();', 'const { sensorData } = useAppContext();'],
            ['const getStatusColor = (status) => {\n    if (status === "Emergency") return "bg-red-500";\n    if (status === "Warning") return "bg-yellow-500";\n    return "bg-green-500";\n  };\n\n  return (', 'return (']
        ]
    },
    {
        file: 'src/pages/Dataset.jsx',
        replacements: [
            ['import React, { useState } from \'react\';', 'import { useState } from \'react\';'],
            ['import { Upload, FileText } from \'lucide-react\';', 'import { Upload } from \'lucide-react\';']
        ]
    },
    {
        file: 'src/pages/Devices.jsx',
        replacements: [['import React from \'react\';\n', '']]
    },
    {
        file: 'src/pages/LiveMonitoring.jsx',
        replacements: [['import React from \'react\';\n', '']]
    },
    {
        file: 'src/pages/Settings.jsx',
        replacements: [['import React from \'react\';\n', '']]
    }
];

fixers.forEach(fix => {
    const p = path.join(__dirname, fix.file);
    if(fs.existsSync(p)) {
        let content = fs.readFileSync(p, 'utf8');
        fix.replacements.forEach(([search, replace]) => {
            content = content.split(search).join(replace);
        });
        fs.writeFileSync(p, content, 'utf8');
    }
});
console.log("Lint errors fixed programmatically.");
