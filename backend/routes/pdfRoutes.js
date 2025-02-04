const express = require("express");
const multer = require("multer");
const axios = require("axios");
const FormData = require("form-data");
const stream = require("stream");

const router = express.Router();
const upload = multer();

router.post("/upload-pdf", upload.single("file"), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: "No file uploaded" });
        }

        const fileStream = new stream.PassThrough();
        fileStream.end(req.file.buffer);

        const formData = new FormData();
        formData.append("file", req.file.buffer, { filename: req.file.originalname, contentType: req.file.mimetype });

        const response = await axios.post("http://localhost:5001/process-pdf", formData, {
            headers: formData.getHeaders(),
        });

        res.json(response.data);
    } catch (error) {
        console.error("Error processing PDF:", error.message);
        res.status(500).json({ error: "Failed to process PDF" });
    }
});


module.exports = router;
