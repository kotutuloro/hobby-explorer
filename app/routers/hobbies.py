from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from ..dependencies import SessionDep
from ..models import *


router = APIRouter()


@router.post("/hobbies")
def create_hobby(hobby: Hobby):
    return {"hobby": hobby, "message": "Hobby created (placeholder)"}


@router.get("/hobbies/{hobby_id}")
def get_hobby(hobby_id: UUID):
    return {"hobby_id": hobby_id, "message": "Get hobby (placeholder)"}


@router.delete("/hobbies/{hobby_id}")
def delete_hobby(hobby_id: UUID):
    return {"hobby_id": hobby_id, "message": "Delete hobby (placeholder)"}
