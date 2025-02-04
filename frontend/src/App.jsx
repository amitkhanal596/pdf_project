import React, { useState } from "react";
import TableDisplay from "./components/TableDisplay";

function App() {
    const [file, setFile] = useState(null);
    const [data, setData] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:4000/api/pdf/upload-pdf", {
                method: "POST",
                body: formData,
                headers: {
                    "Accept": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const json = await response.json();
            setData(json); // Store JSON data in state
            console.log(json);
        } catch (error) {
            console.error("Upload failed:", error.message);
        }
    };

    return (
        <div>
            <h1>UNC Degree Progress Tracker</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload PDF</button>
            {data ? <TableDisplay data={data} /> : <p>No data yet</p>}
        </div>
    );
}

export default App;

