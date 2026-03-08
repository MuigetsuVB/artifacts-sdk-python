"""Character domain controllers -- game-oriented sub-objects.

Each domain groups related actions into a cohesive namespace::

    char.bank.deposit_gold(quantity=100)
    char.skills.craft(code="iron_sword")
    char.ge.sell(code="iron_ore", quantity=10, price=5)
"""

from .bank import BankDomain
from .equipment import EquipmentDomain
from .ge import GrandExchangeDomain
from .inventory import InventoryDomain
from .skills import SkillsDomain
from .tasks import TasksDomain
from .trading import TradingDomain

__all__ = [
    "BankDomain",
    "EquipmentDomain",
    "GrandExchangeDomain",
    "InventoryDomain",
    "SkillsDomain",
    "TasksDomain",
    "TradingDomain",
]
