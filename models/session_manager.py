from __future__ import annotations
from typing import Optional

class SessionManager:
    """
    현재 로그인된 사용자를 관리하는 클래스이다.
    로그인 시점의 User 객체를 저장하고, 필요 시 조회하거나 초기화하는 기능을 제공한다.
    """
    _current_user: Optional[User] = None

    @classmethod
    def get_current_user(cls) -> Optional[User]:
        return cls._current_user

    @classmethod
    def set_current_user(cls, user: User) -> None:
        if not isinstance(user, User):
            raise TypeError("Cannot set current user with non-User object.")
        cls._current_user = user
        print(f"Session set for user: {user.username}")

    @classmethod
    def clear(cls) -> None:
        cls._current_user = None
        print("Session cleared.")