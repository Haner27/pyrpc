from handlers import RegisterService
from thrifts.user_service import UserService


class UserServiceDispatcher(metaclass=RegisterService):
    REGISTER_NAME = 'User'
    SERVICE = UserService

    def __init__(self):
        self.users = []

    def Ping(self) -> UserService.InvaildOperation:
        return UserService.InvaildOperation(200, 'good')

    def CreateUser(self, user: UserService.User):
        self.users.append(user)
        return user

    def GetUsers(self) -> [UserService.User]:
        return self.users

    def GetUserById(self, user_id: int) -> UserService.User or None:
        for user in self.users:
            if user_id == user.id:
                return user
        return None

    def DeleteUserById(self, user_id: int) -> bool:
        users = []
        is_removed = False
        for user in self.users:
            if user.id != user_id:
                users.append(user)
            else:
                is_removed = True
        self.users = users
        return is_removed
