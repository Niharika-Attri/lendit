from fastapi import APIRouter, Response, status, HTTPException
from models.item import ItemCreate, ItemResponse, ItemUpdate
from typing import List
from core.database import conn, cursor  

router = APIRouter(prefix="/v1/items", tags=["items"])

@router.get("/", response_model=List[ItemResponse])
async def get_all_items():
    cursor.execute("""SELECT * FROM items""")
    items = cursor.fetchall()
    return items

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
def add_item(item: ItemCreate, response: Response):
    cursor.execute(
        """INSERT INTO items (name, description, price_per_hour, price_per_day, category, location, is_available, images) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""",
        (item.name, item.description, item.price_per_hour, item.price_per_day, item.category, item.location, item.is_available, item.images)
    )
    new_item = cursor.fetchone()
    conn.commit()
    return new_item

@router.get("/{id}", response_model=ItemResponse)
async def get_item(id: int):
    cursor.execute("""SELECT * FROM items WHERE id = %s""", (str(id),))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Required item not found")
    return item

@router.delete("/{id}")
async def delete_item(id: int):
    cursor.execute("""DELETE FROM items WHERE id = %s RETURNING *""", (str(id),))
    deleted_item = cursor.fetchone()
    conn.commit()
    if not deleted_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The item does not exist")
    return {delete_item}

@router.put("/{id}", response_model=ItemResponse)
async def update_item(id: int, item: ItemUpdate):
    # Build dynamic UPDATE query based on provided fields
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

    # Always update updated_at
    update_fields.append("updated_at = CURRENT_TIMESTAMP")

    if not update_fields:
        # If no fields to update, return the current item
        cursor.execute(
            """SELECT id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at 
               FROM items WHERE id = %s""",
            (str(id),)
        )
        item_data = cursor.fetchone()
        if not item_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item to update doesn't exist")
        return {"message": "No fields provided for update", **item_data}

    # Build and execute the UPDATE query
    update_query = f"""UPDATE items SET {', '.join(update_fields)} 
                      WHERE id = %s 
                      RETURNING id, name, description, price_per_hour, price_per_day, category, location, is_available, images, created_at, updated_at"""
    update_values.append(id)

    cursor.execute(update_query, tuple(update_values))
    updated_item = cursor.fetchone()
    conn.commit()

    if updated_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item to update doesn't exist")
    return {"message": "Item updated successfully", **updated_item}