from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re

app = Flask(__name__)
CORS(app, origins=["http://localhost:4000"])


def extract_sections(pdf_path):
    sections = {
        "First-Year Foundations": [],
        "Focus Capacities": [],
        "Empirical Laboratory Investigation": [],
        "Reflection and Integration": [],
        "Disciplinary Distribution": [],
        "Major Requirements": [],  
        "Mathematics Courses": [],  
        "Science Courses": []  
    }


    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            width = page.width
            height = page.height

            if i == 0:
                top_crop = height * 0.24
                bottom_crop = height * 0.96
            else:
                top_crop = height * .08
                bottom_crop = height * 0.96

            left_bbox = (0, top_crop, width / 2, bottom_crop)
            right_bbox = (width / 2, top_crop, width, bottom_crop)

            left_text = page.within_bbox(left_bbox).extract_text() or ""
            right_text = page.within_bbox(right_bbox).extract_text() or ""

            page_text = left_text + "\n" + right_text
            lines = page_text.split("\n")

            current_section = None

            for line in lines:
                line = line.strip()

                if "First-Year Foundations" in line:
                    current_section = "First-Year Foundations"
                elif line.startswith("Overall Requirement Not Satisfied: Focus Capacities") or line.startswith("Satisfied: Focus Capacities"):
                    current_section = "Focus Capacities"
                elif "Empirical Laboratory" in line:
                    current_section = "Empirical Laboratory Investigation"
                elif "Reflection and Integration" in line:
                    current_section = "Reflection and Integration"
                elif "Disciplinary Distribution" in line:
                    current_section = "Disciplinary Distribution"
                elif "Major Requirements" in line:
                    current_section = "Major Requirements"
                elif "Mathematics Courses" in line:
                    current_section = "Mathematics Courses"
                elif "Science Courses" in line:
                    current_section = "Science Courses"
                elif "Campus Life Experience" in line:
                    break
                elif "Focus Capacities Tally" in line:
                    break
                
                if current_section and line:
                    sections[current_section].append(line)
                    #print(line)

    for key in list(sections):
        i = 0
        while i < len(sections[key]):
            if sections[key][i].startswith("Satisfied"):
                del sections[key][i]
            elif sections[key][i].startswith("D Satisfied"):
                del sections[key][i:i+3]
            elif sections[key][i].startswith("Overall"):
                del sections[key][i]
            elif sections[key][i].startswith("D Not Satisfied"):
                i += 1
            elif sections[key][i].startswith("Not Satisfied"):
                del sections[key][i]
            elif sections[key][i].startswith("Required Major Courses"):
                del sections[key][i]
            elif "1 taken" in sections[key][i]:
                del sections[key][i:i+2]
            elif "0 needed" in sections[key][i]:
                del sections[key][i]
            else:
                i += 1


    for key in sections:
        for index in range(0, len(sections[key])):
            sections[key][index] = sections[key][index].replace("D Not Satisfied: ", "")



    return sections


def merge_course_requirements(data):
    updated_data = {}
    pattern = re.compile(r"· Courses: (\d+) required, \d+ taken, (\d+) needed")

    for key, values in data.items():
        if values:  # Only process non-empty lists
            new_values = []
            i = 0
            while i < len(values):
                match = pattern.match(values[i])
                if match and new_values:
                    courses_needed = match.group(2)  # Extract number of needed courses
                    new_values[-1] += f" |||{courses_needed} course{'s' if courses_needed != '1' else ''} needed|||"
                else:
                    new_values.append(values[i])
                i += 1  # Move to the next item
                
            updated_data[key] = new_values
        else:
            updated_data[key] = values  # Keep empty lists unchanged

    return updated_data



@app.route("/process-pdf", methods=["POST"])
def process_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    pdf_file = request.files["file"]
    pdf_path = "/tmp/uploaded.pdf"
    pdf_file.save(pdf_path)

    extracted_data = extract_sections(pdf_path)
    extracted_data = merge_course_requirements(extracted_data)
    return jsonify(extracted_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)










