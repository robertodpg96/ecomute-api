from typing import List, Dict, Any, Optional

USERS: List[Dict[str, Any]] = []

class UsersDataSource:
    # ==========================
    # USER OPERATIONS
    # ==========================

    def get_all_users(self) -> List[Dict[str, Any]]:
        return USERS

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        for user in USERS:
            if user["id"] == user_id:
                return user
        return None

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        new_id = 1
        if USERS:
            new_id = max(user["id"] for user in USERS) + 1
            
        new_user = {**user_data, "id": new_id, "is_active": True}
        USERS.append(new_user)
        return new_user

    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        user = self.get_user(user_id)
        if user:
            user.update(update_data)
            return user
        return None

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if user:
            USERS.remove(user)
            return True
        return False

def get_users_datasource():
    return UsersDataSource()