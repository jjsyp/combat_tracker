from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Character:
    name: str
    initiative: int = 0
    health: int = 0
    ac: int = 0
    custom_fields: Dict[str, str] = field(default_factory=dict)
    
    def modify_health(self, amount: int) -> None:
        """Modify the character's health by the given amount (positive or negative)"""
        self.health = max(0, self.health + amount)
