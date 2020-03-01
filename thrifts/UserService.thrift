namespace py user_service

struct User {
    1: i32 id
    2: string name
    3: string gender='male'
    4: optional string desc
}

exception InvaildOperation {
    1: i32 code
    2: string msg
}

service UserService {
    InvaildOperation Ping()
    User CreateUser(1: User user)
    list<User> GetUsers()
    User GetUserById(1: i32 user_id)
    bool DeleteUserById(1: i32 user_id)
}