from fastapi import APIRouter, Response, status, HTTPException, Depends
from models.item import ItemCreate, ItemUpdate, ItemResponse
from core.database import get_db
from typing import List
from typing import Annotated  # Use typing_extensions if Python < 3.9
from .auth import get_current_user
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter(prefix="/v1/items", tags=["items"])

@router.get("/", response_model=List[ItemResponse])
async def get_all_items(db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)]):
    conn, cursor = db
    cursor.execute(
        """SELECT id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at 
           FROM items"""
    )
    items = cursor.fetchall()
    return [{"message": "Items retrieved successfully", **item} for item in items]

@router.get("/{id}", response_model=ItemResponse)
async def get_item(id: int, db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)]):
    conn, cursor = db
    cursor.execute(
        """SELECT id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at 
           FROM items WHERE id = %s""",
        (str(id),)
    )
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Required item not found")
    return {"message": "Item retrieved successfully", **item}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
def add_item(
    item: ItemCreate,
    db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)],
    current_user: dict = Depends(get_current_user),
):
    conn, cursor = db
    cursor.execute(
        """INSERT INTO items (name, description, price_per_hour, price_per_day, category, location, is_available, images, owner_id) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
           RETURNING id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at""",
        (item.name, item.description, item.price_per_hour, item.price_per_day, item.category, item.location, item.is_available, item.images, current_user["id"])
    )
    new_item = cursor.fetchone()
    conn.commit()
    return {"message": "Item added successfully", **new_item}

@router.delete("/{id}", response_model=ItemResponse)
async def delete_item(
    id: int,
    db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)],
    current_user: dict = Depends(get_current_user)
):
    conn, cursor = db
    cursor.execute("SELECT owner_id FROM items WHERE id = %s", (str(id),))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The item does not exist")
    if item["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item")
    
    cursor.execute(
        """DELETE FROM items WHERE id = %s 
           RETURNING id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at""",
        (str(id),)
    )
    deleted_item = cursor.fetchone()
    conn.commit()
    return {"message": "Item deleted successfully", **deleted_item}

@router.put("/{id}", response_model=ItemResponse)
async def update_item(
    id: int,
    item: ItemUpdate,
    db: Annotated[tuple[psycopg2.extensions.connection, psycopg2.extras.RealDictCursor], Depends(get_db)],
    current_user: dict = Depends(get_current_user),
):
    conn, cursor = db
    cursor.execute("SELECT owner_id FROM items WHERE id = %s", (str(id),))
    existing_item = cursor.fetchone()
    if not existing_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item to update doesn't exist")
    if existing_item["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this item")
    
    update_fields = []
    update_values = []
    if item.name is not None:
        update_fields.append("name = %s")
        update_values.append(item.name)
    if item.description is not None:
        update_fields.append("description = %s")
        update_values.append(item.description)
    if item.price_per_hour is not None:
        update_fields.append("price_per_hour = %s")
        update_values.append(item.price_per_hour)
    if item.price_per_day is not None:
        update_fields.append("price_per_day = %s")
        update_values.append(item.price_per_day)
    if item.category is not None:
        update_fields.append("category = %s")
        update_values.append(item.category)
    if item.location is not None:
        update_fields.append("location = %s")
        update_values.append(item.location)
    if item.is_available is not None:
        update_fields.append("is_available = %s")
        update_values.append(item.is_available)
    if item.images is not None:
        update_fields.append("images = %s")
        update_values.append(item.images)
    update_fields.append("updated_at = CURRENT_TIMESTAMP")

    if not update_fields:
        cursor.execute(
            """SELECT id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at 
               FROM items WHERE id = %s""",
            (str(id),)
        )
        item_data = cursor.fetchone()
        return {"message": "No fields provided for update", **item_data}

    update_query = f"""UPDATE items SET {', '.join(update_fields)} 
                      WHERE id = %s 
                      RETURNING id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at"""
    update_values.append(id)

    cursor.execute(update_query, tuple(update_values))
    updated_item = cursor.fetchone()
    conn.commit()
    return {"message": "Item updated successfully", **updated_item}