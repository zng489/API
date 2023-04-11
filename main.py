from fastapi import FastAPI, Path
from file_json import students
from typing import Optional
from student import Student
from update_student import UpdateStudent

app = FastAPI()

@app.get("/")
def index():
    return {"name":"First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="The ID of the student you want to view", gt=0)):
    # great than
    # less than
    return students[student_id]

@app.get("/get-by-name")
def get_student(*, student_id:int, put_name: Optional[str] = None, test:int):
    #def get_student(put_name:str):
    #def get_student(*, put_name: Optional[str] = None, test:int):
    for student_id in students:
        if students[student_id]["name"] == put_name:
            return students[student_id]
    return {"Data":"Not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student : Student):
    if student_id in students:
        return {"Error":"Student exists"}

    students[student_id] = student
    return student[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error":"Student does not exist"}

    elif student.name != None:
        students[student_id].name = student.name
    
    elif student.age != None:
        students[student_id].age = student.age

    elif student.year != None:
        students[student_id].year = student.year

    #students[student_id] = student
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error":"Student does not exist"}

    del students[student_id]
    return {"Message":"Student deleted successfully"}

#main:app --reload  