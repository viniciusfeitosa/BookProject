namespace py user_service.client
namespace go user_service.server

struct User {
  1: i32 ID = 0,
  2: string name,
  3: string email,
}

service GetUserData {
    User getUser(1:i32 id)
}