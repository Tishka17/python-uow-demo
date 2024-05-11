from gateway import UserGateway
from models import User
from uowed import UnitOfWork


def interactor(uow: UnitOfWork, gw: UserGateway) -> None:
    user = gw.get_user(1)
    user.name = "Tishka17"

    user2 = uow.register_new(User(2, "User2"))
    user2.name = "Mock User"

    user3 = gw.get_user(3)
    uow.register_deleted(user3)
    uow.commit()


def main():
    uow = UnitOfWork()
    gw = UserGateway(uow)
    interactor(uow, gw)


if __name__ == '__main__':
    main()
