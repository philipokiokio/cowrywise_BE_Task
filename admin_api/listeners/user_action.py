import json
from schemas.user_schemas import User
from services.user_service import create_user


async def action_create_user(data: str):

    user_dict = json.loads(data)

    user = User(**user_dict)

    try:
        await create_user(user=user)
    except Exception:
        pass
