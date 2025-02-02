from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import csv

app = FastAPI()

# Enable CORS to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"]   # Allow all headers
)

# Load CSV data into memory
def load_students():
    students = []
    with open("q-fastapi.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })
    return students

students_data = load_students()

@app.get("/api")
def get_students(class_name: List[str] = Query(None, alias="class")):
    if class_name:
        filtered_students = [s for s in students_data if s["class"] in class_name]
        return {"students": filtered_students}
    return {"students": students_data}

# Run the FastAPI app using Uvicorn
# Command to run: uvicorn filename:app --reload
