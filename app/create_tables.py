# create_tables.py
from app.database import engine, Base


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    role = Column(String)
    hashed_password = Column(String)

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    employees = relationship("Employee", back_populates="department", cascade="all, delete")

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey('departments.id', ondelete="SET NULL"))
    department = relationship("Department", back_populates="employees")
    skills = relationship("EmployeeSkill", back_populates="employee", cascade="all, delete-orphan")
    timesheets = relationship("Timesheet", backref="employee", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class EmployeeSkill(Base):
    __tablename__ = 'employee_skills'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    level = Column(String(20))
    employee = relationship("Employee", back_populates="skills")

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    projects = relationship("Project", backref="client", cascade="all, delete")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'))
    assignments = relationship("ProjectAssignment", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", backref="project", cascade="all, delete-orphan")
    milestones = relationship("Milestone", backref="project", cascade="all, delete-orphan")
    issues = relationship("Issue", backref="project", cascade="all, delete-orphan")

class ProjectAssignment(Base):
    __tablename__ = 'project_assignments'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    role = Column(String(50))
    project = relationship("Project", back_populates="assignments")
    employee = relationship("Employee")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    project_id = Column(Integer, ForeignKey('projects.id'))
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")

class TaskComment(Base):
    __tablename__ = 'task_comments'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    content = Column(Text)
    task = relationship("Task", back_populates="comments")

class Timesheet(Base):
    __tablename__ = 'timesheets'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    hours = Column(Integer)
    date = Column(DateTime)

class Milestone(Base):
    __tablename__ = 'milestones'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String(100))
    due_date = Column(DateTime)

class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    title = Column(String(100))
    description = Column(Text)
    status = Column(String(20))

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")
