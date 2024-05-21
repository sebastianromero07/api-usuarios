from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from db import conn, commit
from uvicorn import run

# Definir el modelo Pydantic para los usuarios
class User(BaseModel):
    firstname: str
    lastname: str
    gender: str
    age: int
    phone: str
    address: str

app = FastAPI()

@app.get("/users")
async def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    users = [{"id": row[0], "firstname": row[1], "lastname": row[2], "gender": row[3], "age": row[4], "phone": row[5], "address": row[6]} for row in rows]
    return users

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., title="The ID of the user to get")):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "firstname": row[1], "lastname": row[2], "gender": row[3], "age": row[4], "phone": row[5], "address": row[6]}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users")
async def create_user(user: User):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (firstname, lastname, gender, age, phone, address) VALUES (%s, %s, %s, %s, %s, %s)",
                   (user.firstname, user.lastname, user.gender, user.age, user.phone, user.address))
    commit()
    return {"message": "User created successfully"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET firstname=%s, lastname=%s, gender=%s, age=%s, phone=%s, address=%s WHERE id=%s",
                   (user.firstname, user.lastname, user.gender, user.age, user.phone, user.address, user_id))
    commit()
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    commit()
    return {"message": "User deleted successfully"} 

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8001)
