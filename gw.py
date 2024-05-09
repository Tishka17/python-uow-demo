from models import User
from uowed import UowedGw, UoW, UowedModel


class UserGw(UowedGw):
    def __init__(self, uow: UoW):
        self.uow = uow
        uow.repos[User] = self

    def get_user(self, id) -> User:
        user = User(id, f"Name {id}")
        return UowedModel(user, self.uow)

    def insert(self, model):
        print(f"insert {model}")

    def delete(self, model):
        print(f"delete {model}")

    def update(self, model):
        print(f"update {model}")
