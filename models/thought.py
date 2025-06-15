from datetime import datetime

class Thought:
    def __init__(self, id: str, nickname: str, content: str, created_at: datetime = None):
        self.id = id
        self.nickname = nickname
        self.content = content
        self.created_at = created_at if created_at else datetime.now()

    def edit_content(self, new_content: str) -> None:
        if not new_content or not isinstance(new_content, str) or len(new_content.strip()) < 5:
            raise ValueError("새로운 생각 내용은 최소 5자 이상이어야 합니다.")
        print(f"[수정됨] 이전 내용: '{self.content[:30]}...' → 새로운 내용: '{new_content[:30]}...'")
        self.content = new_content.strip()

    def __repr__(self) -> str:
        return f"<Thought id={self.id}, nickname={self.nickname}, created_at={self.created_at}, content='{self.content[:30]}...'>"
