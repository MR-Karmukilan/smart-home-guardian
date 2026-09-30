const fs = require('fs');
const path = require('path');

const replaceConfig = [
    {
        files: ['index.html'],
        replacements: [
            ['bg-dark-bg text-gray-100', 'bg-[#f4f1ea] text-black']
        ]
    },
    {
        files: ['src/App.jsx'],
        replacements: [
            ['bg-dark-bg', 'bg-[#f4f1ea]']
        ]
    },
    {
        files: [
            'src/components/Sidebar.jsx',
            'src/components/Topbar.jsx',
            'src/components/SensorCard.jsx',
            'src/pages/Dashboard.jsx',
            'src/pages/LiveMonitoring.jsx',
            'src/pages/AIAnalysis.jsx',
            'src/pages/Dataset.jsx',
            'src/pages/Alerts.jsx',
            'src/pages/Devices.jsx',
            'src/pages/Settings.jsx'
        ],
        replacements: [
            ['bg-dark-card', 'bg-white'],
            ['border-dark-border', 'border-[#8b4513]'],
            ['bg-[#0f172a]', 'bg-[#e8e4d9]'],
            ['text-gray-100', 'text-black'],
            ['text-gray-300', 'text-[#3e2723]'],
            ['text-gray-400', 'text-[#5d4037]'],
            ['text-gray-500', 'text-[#8d6e63]'],
            ['<span className="text-white">', '<span className="text-black font-bold">'],
            ['text-white focus:outline-none', 'text-black focus:outline-none']
        ]
    },
    {
        files: ['src/components/Sidebar.jsx'],
        replacements: [
            ["isActive ? 'bg-blue-600 text-white' : 'text-gray-400 hover:bg-dark-border hover:text-white'", "isActive ? 'bg-black text-white' : 'text-[#5d4037] hover:bg-[#e8e4d9] hover:text-black'"]
        ]
    },
    {
        files: ['src/pages/Settings.jsx', 'src/pages/Devices.jsx'],
        replacements: [
            ['bg-blue-600 hover:bg-blue-500', 'bg-black hover:bg-gray-800'],
        ]
    },
    {
        files: ['src/pages/LiveMonitoring.jsx'],
        replacements: [
            ['stroke="#94a3b8"', 'stroke="#5d4037"'],
            ["backgroundColor: '#1e293b'", "backgroundColor: '#ffffff'"],
            ["borderColor: '#334155'", "borderColor: '#8b4513'"]
        ]
    },
    {
        files: ['src/pages/Alerts.jsx'],
        replacements: [
            ['bg-dark-border hover:bg-gray-700', 'bg-[#e8e4d9] hover:bg-[#d7ccc8] text-black']
        ]
    },
    {
        files: ['src/index.css'],
        replacements: [
            ['background: #0f172a;', 'background: #f4f1ea;'],
            ['background: #334155;', 'background: #8b4513;'],
            ['background: #475569;', 'background: #a0522d;']
        ]
    }
];

replaceConfig.forEach(group => {
    group.files.forEach(file => {
        const fullPath = path.join(__dirname, file);
        if (fs.existsSync(fullPath)) {
            let content = fs.readFileSync(fullPath, 'utf8');
            group.replacements.forEach(([search, replace]) => {
                content = content.split(search).join(replace);
            });
            fs.writeFileSync(fullPath, content, 'utf8');
        }
    });
});

console.log("Theme updated to White, Brown, and Black.");
