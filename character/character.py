from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Character:
    name: str
    initiative: int = 0
    initiative_bonus: int = field(default=0)  # Bonus for initiative ties
    health: int = 0
    ac: int = 0
    custom_fields: Dict[str, str] = field(default_factory=dict)
    
    def modify_health(self, amount: int) -> None:
        """Modify the character's health by the given amount (positive or negative)"""
        self.health = max(0, self.health + amount)

    def to_dict(self) -> dict:
        """Convert character to dictionary for saving"""
        return {
            'name': self.name,
            'initiative': self.initiative,
            'initiative_bonus': self.initiative_bonus,
            'health': self.health,
            'ac': self.ac,
            'custom_fields': self.custom_fields
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        """Create character from dictionary data"""
        return cls(
            name=data['name'],
            initiative=data['initiative'],
            initiative_bonus=data.get('initiative_bonus', 0),  # Handle older saves
            health=data['health'],
            ac=data['ac'],
            custom_fields=data['custom_fields']
        )
