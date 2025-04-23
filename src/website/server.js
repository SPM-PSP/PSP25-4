const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

// 将静态文件目录设置为当前目录（即包含 try.html）
const publicDir = path.join(__dirname);
app.use(express.static(publicDir));

app.use(express.json());

// 写入 feedback.txt
app.post('/submit-feedback', (req, res) => {
    const feedback = req.body.feedback;
    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] ${feedback}\n`;

    const feedbackPath = path.join(__dirname, 'feedback.txt');
    fs.appendFile(feedbackPath, line, (err) => {
        if (err) {
            console.error('写入失败：', err);
            return res.status(500).json({success: false, message: '服务器错误'  }); 
        }
        res.status(200).json({ success: true, message: '反馈已保存'  }); 
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`服务器已启动： http://localhost:${PORT}`);
});
