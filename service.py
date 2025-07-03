from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def get_profile(db: Session):
    res = {}
    return res


async def get_profile(db: Session):

    query = db.query(models.Profile)

    profile_all = query.all()
    profile_all = (
        [new_data.to_dict() for new_data in profile_all] if profile_all else profile_all
    )
    res = {
        "profile_all": profile_all,
    }
    return res


async def post_join(db: Session, id: int):

    s_alias = aliased(models.Class)
    query = db.query(models.Students, s_alias)

    query = query.join(s_alias, and_(models.Students.id == models.Class.id))

    join_list = query.all()
    join_list = (
        [
            {
                "join_list_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "join_list_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in join_list
        ]
        if join_list
        else join_list
    )
    res = {
        "list": join_list,
    }
    return res


async def post_class(db: Session, id: int, subject: str):

    record_to_be_added = {"id": id, "subject": subject}
    new_class = models.Class(**record_to_be_added)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    add_a_record = new_class.to_dict()

    res = {
        "add_records": add_a_record,
    }
    return res


async def get_profile_id(db: Session, id: int):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.id == id))

    profile_one = query.first()

    profile_one = (
        (
            profile_one.to_dict()
            if hasattr(profile_one, "to_dict")
            else vars(profile_one)
        )
        if profile_one
        else profile_one
    )

    res = {
        "profile_one": profile_one,
    }
    return res


async def put_profile_id(
    db: Session,
    id: int,
    name: str,
    address: str,
    mobile: str,
    password: str,
    email: str,
):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.id == id))
    profile_edited_record = query.first()

    if profile_edited_record:
        for key, value in {
            "id": id,
            "name": name,
            "email": email,
            "mobile": mobile,
            "address": address,
            "password": password,
        }.items():
            setattr(profile_edited_record, key, value)

        db.commit()
        db.refresh(profile_edited_record)

        profile_edited_record = (
            profile_edited_record.to_dict()
            if hasattr(profile_edited_record, "to_dict")
            else vars(profile_edited_record)
        )
    res = {
        "profile_edited_record": profile_edited_record,
    }
    return res


async def delete_profile_id(db: Session, id: int):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        profile_deleted = record_to_delete.to_dict()
    else:
        profile_deleted = record_to_delete
    res = {
        "profile_deleted": profile_deleted,
    }
    return res


async def get_records(db: Session):

    query = db.query(models.Records)

    records_all = query.all()
    records_all = (
        [new_data.to_dict() for new_data in records_all] if records_all else records_all
    )
    res = {
        "records_all": records_all,
    }
    return res


async def get_records_id(db: Session, id: int):

    query = db.query(models.Records)
    query = query.filter(and_(models.Records.id == id))

    records_one = query.first()

    records_one = (
        (
            records_one.to_dict()
            if hasattr(records_one, "to_dict")
            else vars(records_one)
        )
        if records_one
        else records_one
    )

    res = {
        "records_one": records_one,
    }
    return res


async def post_records(db: Session, id: int, username: str, address: str):

    record_to_be_added = {"id": id, "address": address, "username": username}
    new_records = models.Records(**record_to_be_added)
    db.add(new_records)
    db.commit()
    db.refresh(new_records)
    records_inserted_record = new_records.to_dict()

    res = {
        "records_inserted_record": records_inserted_record,
    }
    return res


async def put_records_id(db: Session, id: int, username: str, address: str):

    query = db.query(models.Records)
    query = query.filter(and_(models.Records.id == id))
    records_edited_record = query.first()

    if records_edited_record:
        for key, value in {"id": id, "address": address, "username": username}.items():
            setattr(records_edited_record, key, value)

        db.commit()
        db.refresh(records_edited_record)

        records_edited_record = (
            records_edited_record.to_dict()
            if hasattr(records_edited_record, "to_dict")
            else vars(records_edited_record)
        )
    res = {
        "records_edited_record": records_edited_record,
    }
    return res


async def delete_records_id(db: Session, id: int):

    query = db.query(models.Records)
    query = query.filter(and_(models.Records.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        records_deleted = record_to_delete.to_dict()
    else:
        records_deleted = record_to_delete
    res = {
        "records_deleted": records_deleted,
    }
    return res


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )
    res = {
        "users_all": users_all,
    }
    return res


async def get_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "users_one": users_one,
    }
    return res


async def put_users_id(
    db: Session, id: int, username: str, password: str, test: str, test123: str
):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "id": id,
            "test": test,
            "test123": test123,
            "password": password,
            "username": username,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )
    res = {
        "users_edited_record": users_edited_record,
    }
    return res


async def delete_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete
    res = {
        "users_deleted": users_deleted,
    }
    return res


async def get_students(db: Session):

    query = db.query(models.Students)

    students_all = query.all()
    students_all = (
        [new_data.to_dict() for new_data in students_all]
        if students_all
        else students_all
    )
    res = {
        "students_all": students_all,
    }
    return res


async def get_students_id(db: Session, id: int):

    query = db.query(models.Students)
    query = query.filter(and_(models.Students.id == id))

    students_one = query.first()

    students_one = (
        (
            students_one.to_dict()
            if hasattr(students_one, "to_dict")
            else vars(students_one)
        )
        if students_one
        else students_one
    )

    res = {
        "students_one": students_one,
    }
    return res


async def post_students(db: Session, id: int, name: str, age: str):

    record_to_be_added = {"id": id, "age": age, "name": name}
    new_students = models.Students(**record_to_be_added)
    db.add(new_students)
    db.commit()
    db.refresh(new_students)
    students_inserted_record = new_students.to_dict()

    res = {
        "students_inserted_record": students_inserted_record,
    }
    return res


async def put_students_id(db: Session, id: int, name: str, age: str):

    query = db.query(models.Students)
    query = query.filter(and_(models.Students.id == id))
    students_edited_record = query.first()

    if students_edited_record:
        for key, value in {"id": id, "age": age, "name": name}.items():
            setattr(students_edited_record, key, value)

        db.commit()
        db.refresh(students_edited_record)

        students_edited_record = (
            students_edited_record.to_dict()
            if hasattr(students_edited_record, "to_dict")
            else vars(students_edited_record)
        )
    res = {
        "students_edited_record": students_edited_record,
    }
    return res


async def delete_students_id(db: Session, id: int):

    query = db.query(models.Students)
    query = query.filter(and_(models.Students.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        students_deleted = record_to_delete.to_dict()
    else:
        students_deleted = record_to_delete
    res = {
        "students_deleted": students_deleted,
    }
    return res


async def post_profile(
    db: Session,
    id: int,
    name: str,
    address: str,
    mobile: str,
    password: str,
    email: str,
):

    record_to_be_added = {
        "id": id,
        "name": name,
        "email": email,
        "mobile": mobile,
        "address": address,
        "password": password,
    }
    new_profile = models.Profile(**record_to_be_added)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    profile_inserted_record = new_profile.to_dict()

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.id == id))
    test = query.first()

    if test:
        for key, value in {
            "id": id,
            "name": name,
            "email": name,
            "mobile": name,
            "address": name,
            "password": name,
        }.items():
            setattr(test, key, value)

        db.commit()
        db.refresh(test)

        test = test.to_dict() if hasattr(test, "to_dict") else vars(test)

    for loop_1 in range(id, 10):

        break
    res = {
        "profile_inserted_record": profile_inserted_record,
        "test": test,
    }
    return res


async def post_users(
    db: Session, id: int, username: str, password: str, test: str, test123: str
):

    test145 = aliased(models.Profile)
    query = db.query(models.Users, test145)

    query = query.join(test145, and_(models.Users.id == models.Profile.id))

    test1 = query.all()
    test1 = (
        [
            {
                "test1_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "test1_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in test1
        ]
        if test1
        else test1
    )
    res = {
        "test": test1,
    }
    return res
