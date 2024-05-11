from typing import cast

from models import User
from uowed import DataMapper, UnitOfWork, UoWModel


class UserMapper(DataMapper[User]):
    def insert(self, model: User) -> None:
        print(f"insert {model}")

    def delete(self, model: User) -> None:
        print(f"delete {model}")

    def update(self, model: User) -> None:
        print(f"update {model}")


class UserGateway:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        uow.mappers[User] = UserMapper()

    def get_user(self, id) -> User:
        user = User(id, f"Name {id}")
        return cast(User, UoWModel(user, self.uow))
