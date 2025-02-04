const express = require('express');
const cors = require('cors');
const pdfRoutes = require('./routes/pdfRoutes');

const app = express();
app.use(cors());
app.use(express.json());

app.use("/api/pdf", pdfRoutes);

const PORT = 4000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

//main express server, basically done