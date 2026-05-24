from app.db.mongo import users_collection


# 🔍 Find user
def find_user(email):
    return users_collection.find_one({"email": email})


# 🆕 Create user
def create_user(user_info):
    existing = find_user(user_info.get("email"))

    if existing:
        return existing

    user = {
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "password": user_info.get("password"),
        "provider": user_info.get("provider", "local"),
    }

    users_collection.insert_one(user)
    return user