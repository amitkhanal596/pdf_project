import React from "react";

function TableDisplay({ data }) {
    if (!data || data.length === 0) {
        return <p>No data available</p>;
    }

    return (
        <ul>
            {Object.keys(data).map((key, value) => {
                return (
                    <div>
                        <li>{key}</li>
                            {data[key].map((item, index) => {
                                return (
                                    <ul>
                                        <li>{item}</li>
                                    </ul>
                                );
                            })}

                    </div>
                    
                );
                
            })}
        </ul>
    );
}

export default TableDisplay;
