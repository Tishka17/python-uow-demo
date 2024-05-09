from gw import UserGw
from models import User
from uowed import UoW


def interactor(uow: UoW, gw: UserGw) -> None:
    user = gw.get_user(1)
    user.name = "Tishka17"

    user2 = uow.register_new(User(2, "User2"))
    user2.name = "Mock User"

    user3 = gw.get_user(3)
    uow.register_deleted(user3)
    uow.commit()


def main():
    uow = UoW()
    gw = UserGw(uow)
    interactor(uow, gw)


if __name__ == '__main__':
    main()
