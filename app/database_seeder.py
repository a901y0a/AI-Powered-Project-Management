from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal,Base
from models import (
     User, Employee, Department, Project, Client, ProjectAssignment,
    Task, TaskComment, Skill, EmployeeSkill, Milestone, Timesheet, Issue
)
from database import engine
from faker import Faker
import random
from passlib.hash import bcrypt
from datetime import datetime

fake = Faker()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def seed_database():
    # Delete existing data respecting FK constraints
    db.query(TaskComment).delete()
    db.query(Task).delete()
    db.query(ProjectAssignment).delete()
    db.query(Milestone).delete()
    db.query(Issue).delete()
    db.query(Project).delete()
    db.query(Client).delete()
    db.query(Timesheet).delete()
    db.query(EmployeeSkill).delete()
    db.query(Skill).delete()
    db.query(Employee).delete()
    db.query(Department).delete()
    db.query(User).delete()
    db.commit()

    # Departments
    departments = []
    for _ in range(5):
        dept = Department(name=fake.company_suffix() + " Dept")
        db.add(dept)
        departments.append(dept)
    db.commit()

    # Users
    users = []
    for _ in range(10):
        username = fake.user_name()
        password = "password123"
        hashed_pw = bcrypt.hash(password)
        user = User(
            username=username,
            hashed_password=hashed_pw,
            role=random.choice(["admin", "employee"]),
        )
        db.add(user)
        users.append(user)
    db.commit()

    print("Users created:")
    for user in users:
        print(f"Username: {user.username}, Password: password123")

        

    # Skills
    skills = []
    for name in ["Python", "JavaScript", "SQL", "React", "AWS"]:
        skill = Skill(name=name)
        db.add(skill)
        skills.append(skill)
    db.commit()

    # Employees
    employees = []
    for _ in range(10):
        emp = Employee(
            name=fake.name(),
            email=fake.email(),
            department_id=random.choice(departments).id,
        )
        db.add(emp)
        employees.append(emp)
    db.commit()

    # Employee Skills
    for emp in employees:
        for _ in range(random.randint(1, 3)):
            emp_skill = EmployeeSkill(
                employee_id=emp.id,
                skill_id=random.choice(skills).id,
                level=random.choice(["Beginner", "Intermediate", "Expert"]),
            )
            db.add(emp_skill)
    db.commit()

    # Clients
    clients = []
    for _ in range(5):
        client = Client(name=fake.company())
        db.add(client)
        clients.append(client)
    db.commit()

    # Projects
    projects = []
    for _ in range(5):
        proj = Project(
            name=fake.catch_phrase(),
            client_id=random.choice(clients).id,
        )
        db.add(proj)
        projects.append(proj)
    db.commit()

    # Assignments
    for proj in projects:
        for _ in range(random.randint(1, 4)):
            assignment = ProjectAssignment(
                project_id=proj.id,
                employee_id=random.choice(employees).id,
                role=random.choice(["Developer", "Manager"]),
            )
            db.add(assignment)
    db.commit()

    # Tasks and Comments
    tasks = []
    for proj in projects:
        for _ in range(random.randint(2, 5)):
            task = Task(
                title=fake.sentence(nb_words=3),
                project_id=proj.id,
            )
            db.add(task)
            tasks.append(task)
    db.commit()

    for task in tasks:
        for _ in range(random.randint(0, 3)):
            comment = TaskComment(
                task_id=task.id,
                content=fake.paragraph(nb_sentences=2),
            )
            db.add(comment)
    db.commit()

    # Milestones
    for proj in projects:
        milestone = Milestone(
            project_id=proj.id,
            name="Milestone 1",
            due_date=fake.date_time_this_year(),
        )
        db.add(milestone)
    db.commit()

    # Timesheets
    for emp in employees:
        timesheet = Timesheet(
            employee_id=emp.id,
            hours=random.randint(1, 8),
            date=datetime.now(),
        )
        db.add(timesheet)
    db.commit()

    # Issues
    for proj in projects:
        issue = Issue(
            project_id=proj.id,
            title=fake.sentence(nb_words=4),
            description=fake.text(),
            status="Open",
        )
        db.add(issue)
    db.commit()

    print("\n✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
