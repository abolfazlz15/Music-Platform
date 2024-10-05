from accounts.models import User
class UserRepository:
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod   
    def get_user_by_id(user_email: str) -> User:
        try:
            return User.objects.get(email=user_email)
        except User.DoesNotExist:
            return None
    # @staticmethod
    # def create_user(*, email: str, username: str, **kwargs):
    #     try:
            
    #     pass

    # @staticmethod
    # def update_user(*, user_id: int, email: str, username: str):
    #     pass

    # @staticmethod
    # def delete_user(*, user_id: int):
    #     pass