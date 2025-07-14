from fastapi import APIRouter, Depends, status, HTTPException
from models.user import UserCreate, UserResponse, CollegeIdInput, UserUpdate
from psycopg2.extras import RealDictCursor
import psycopg2
from passlib.context import CryptContext
from datetime import datetime
from typing import List, Annotated
from core.database import get_db
from .auth import get_current_user
from core.cloudinary import handle_upload

router = APIRouter(prefix="/v1/users", tags=["users"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)]):
    conn, cursor = db
    hashed_password = pwd_context.hash(user.password)
    try:
        cursor.execute(
            """INSERT INTO users (email, password, first_name, last_name, phone_number, role) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, email, first_name, last_name, phone_number, college_id_url, role, created_at, updated_at, is_active""",
            (user.email, hashed_password, user.first_name, user.last_name, user.phone_number, user.role)
        )
        new_user = cursor.fetchone()
        conn.commit()
        return new_user  
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)]):
    conn, cursor = db
    cursor.execute("""SELECT id, email, first_name, last_name, phone_number, college_id_url, role, created_at, updated_at, is_active FROM users""")
    users = cursor.fetchall()
    return users  

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)]):
    conn, cursor = db
    cursor.execute(
        """SELECT id, email, first_name, last_name, phone_number, college_id_url, role, created_at, updated_at, is_active FROM users WHERE id = %s""",
        (str(id),)
    )
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/{id}/college-id", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def set_college_id(id: int, input: CollegeIdInput, db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)]):
    conn, cursor = db
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    url = str(input.college_id_url)
    if not any(url.lower().endswith(ext) for ext in valid_extensions):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL must point to an image (.jpg, .jpeg, .png, .gif)")
    
    cursor.execute(
        """UPDATE users SET college_id_url = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s 
            RETURNING id, email, first_name, last_name, phone_number, college_id_url, role, created_at, updated_at, is_active""",
        (url, id)
    )
    updated_user = cursor.fetchone()
    conn.commit()
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return updated_user


@router.put("/update", response_model=UserResponse)
def update_user(user: UserUpdate, current_user=Depends(get_current_user), db=Depends(get_db)):
    conn, cursor = db
    id = current_user["id"]
    update_fields = []
    update_values = []
    if user.first_name is not None:
        update_fields.append("first_name = %s")
        update_values.append(user.first_name)
    if user.last_name is not None:
        update_fields.append("last_name = %s")
        update_values.append(user.last_name)
    if user.email is not None:
        update_fields.append("email = %s")
        update_values.append(user.email)
    if user.phone_number is not None:
        update_fields.append("phone_number = %s")
        update_values.append(user.phone_number)
    if user.password is not None:
        update_fields.append("password = %s")
        update_values.append(pwd_context.hash(user.password))
    if user.is_active is not None:
        update_fields.append("is_active = %s")
        update_values.append(user.is_active)
    if user.college_id_url is not None:
        update_fields.append("college_id_url = %s")
        update_values.append(user.college_id_url)
    update_fields.append("updated_at = CURRENT_TIMESTAMP")

    if not update_fields:
        cursor.execute(
            """SELECT id, name, email, phone_number, is_active, created_at, updated_at 
            FROM users WHERE id = %s""",
            (str(id),)
        )
        user_data = cursor.fetchone()
        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to update doesn't exist")
        return {"message": "No fields provided for update", **user_data}

    update_query = f"""UPDATE users SET {', '.join(update_fields)} 
                    WHERE id = %s 
                    RETURNING id, first_name, last_name, email, phone_number, role, is_active, created_at, updated_at"""
    update_values.append(id)

    cursor.execute(update_query, tuple(update_values))
    updated_user = cursor.fetchone()
    conn.commit()
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to update doesn't exist")
    return {"message": "User updated successfully", **updated_user}