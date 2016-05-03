#!/usr/bin/env python3

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from app.mod.auth.models import User
from app.database import Base, db_session, engine
import enum

class Project(Base):
    __tablename__ = "project"
    project_id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    status = Column(Enum("active", "archived"))

    def __init__(self, name=None, status="active"):
        self.name = name
        self.status = status

    def get(id):
        Project.query.get(int(id))

    def get_id(self):
        return self.project_id

    def get_projects(user, group):
        sql = text('select distinct p.name, p.project_id, pp.group ' + \
                   'from project p, user u, project_permission pp ' + \
                   'where p.project_id=pp.project_id and pp.user_id=' + \
                   str(user.get_id()) + ' and pp.group="' + group + '"')

        result = engine.execute(sql)
        print ("result: ", result)
        projects = { "name": [], "id": [] }


        for row in result:
            projects["name"].append(row[0])
            projects["id"].append(row[1])
            print ("Project: ", row[0],'\t',row[1])

        return projects

    def remove_project(id):
        print("remove_project called: " + str(id))
        #sql = text('delete from project where project_id="'+ str(id) + '"')
        #engine.execute(sql)
        db_session.query(Project).filter(Project.project_id == id)\
                          .delete(synchronize_session='evaluate')
        db_session.commit()

    def __repr__(self):
        return "<Project %r>" % (self.name)

class ProjectPermission(Base):
    __tablename__ = "project_permission"
    project_id = Column (Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    group = Column(Enum("admin", "user"), nullable=False)

    def __init__(self, user_id=None, project_id=None, group=None):
        self.user_id = user_id
        self.project_id = project_id
        self.group = group

    def get(id):
        return ProjectPermission.query.get(int(id))

    def get_pid(self):
        return self.project_id

    def get_uid(self):
        return self.user_id

    def __repr__(self):
        return "<ProjectPermission %r>" % (self.project_id)

class TimeEntry(Base):
    __tablename__ = "time_entry"
    task_entry_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.task_id"), unique=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), unique=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class Task(Base):
    __tablename__ = "task"
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), unique=True, nullable=False)
    status = Column (Enum("Open","Closed", name='tasks_status'))
    description = Column(String(150), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    tags = relationship("Tag", backref="task")

class Tag(Base):
    __tablename__ = "tag"
    tag_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task.task_id"), unique=True, nullable=False)
    task_name = Column(String(32))
