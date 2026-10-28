from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCreate, UserResponse

router = APIRouter()

fake_db = {} #временная БД, потом заменю

@router.post("/api/v1/users", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    #Проверка на дубликат
    if user.username in fake_db:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Пользователь с таким логином уже существует"
        )
#сохраняю пока в словарь
    fake_db[user.username] = user 

#И возвращаю ответ (без пароля)
    return UserResponse(
        id = 1,
        username = user.username,
        email = user.email
)
