from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    name: str
    posts: list[str] = field(default_factory=list)
