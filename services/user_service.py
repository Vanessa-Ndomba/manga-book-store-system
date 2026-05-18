from services.exceptions import AlreadyExistsError, NotFoundError


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def list_users(self):
        return self.user_repo.find_all()

    def get_user(self, user_id: str):
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User '{user_id}' not found")
        return user

    def create_user(self, user):
        existing = self.user_repo.find_by_id(user.user_id)
        if existing is not None:
            raise AlreadyExistsError(f"User '{user.user_id}' already exists")

        self.user_repo.save(user)
        return user

    def delete_user(self, user_id: str):
        self.get_user(user_id)
        self.user_repo.delete(user_id)