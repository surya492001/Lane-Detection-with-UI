const express = require('express');
const app = express();
const path = require('path');
const multer = require('multer');

// Set up storage for multer to handle file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Handle POST request to /process_frame
app.post('/process_frame', upload.single('video'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    // Process the video file here
    // For example, you can save it to the disk or perform analysis

    // Respond with success message
    res.status(200).json({ message: 'Video processed successfully' });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
