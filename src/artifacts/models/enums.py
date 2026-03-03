from __future__ import annotations

from enum import Enum


class AccountStatus(str, Enum):
    STANDARD = "standard"
    FOUNDER = "founder"
    GOLD_FOUNDER = "gold_founder"
    VIP_FOUNDER = "vip_founder"


class AccountLeaderboardType(str, Enum):
    ACHIEVEMENTS_POINTS = "achievements_points"
    GOLD = "gold"


class AchievementType(str, Enum):
    COMBAT_KILL = "combat_kill"
    COMBAT_DROP = "combat_drop"
    COMBAT_LEVEL = "combat_level"
    GATHERING = "gathering"
    CRAFTING = "crafting"
    RECYCLING = "recycling"
    TASK = "task"
    OTHER = "other"
    USE = "use"
    NPC_BUY = "npc_buy"
    NPC_SELL = "npc_sell"


class ActionType(str, Enum):
    MOVEMENT = "movement"
    FIGHT = "fight"
    MULTI_FIGHT = "multi_fight"
    CRAFTING = "crafting"
    GATHERING = "gathering"
    BUY_GE = "buy_ge"
    SELL_GE = "sell_ge"
    CREATE_BUY_ORDER_GE = "create_buy_order_ge"
    FILL_BUY_ORDER_GE = "fill_buy_order_ge"
    BUY_NPC = "buy_npc"
    SELL_NPC = "sell_npc"
    CANCEL_GE = "cancel_ge"
    DELETE_ITEM = "delete_item"
    DEPOSIT_ITEM = "deposit_item"
    WITHDRAW_ITEM = "withdraw_item"
    DEPOSIT_GOLD = "deposit_gold"
    WITHDRAW_GOLD = "withdraw_gold"
    EQUIP = "equip"
    UNEQUIP = "unequip"
    TASK = "task"
    RECYCLING = "recycling"
    REST = "rest"
    USE = "use"
    BUY_BANK_EXPANSION = "buy_bank_expansion"
    GIVE_ITEM = "give_item"
    GIVE_GOLD = "give_gold"
    CHANGE_SKIN = "change_skin"
    RENAME = "rename"
    TRANSITION = "transition"
    CLAIM_ITEM = "claim_item"
    SANDBOX_GIVE_GOLD = "sandbox_give_gold"
    SANDBOX_GIVE_ITEM = "sandbox_give_item"
    SANDBOX_GIVE_XP = "sandbox_give_xp"


class CharacterLeaderboardType(str, Enum):
    COMBAT = "combat"
    WOODCUTTING = "woodcutting"
    MINING = "mining"
    FISHING = "fishing"
    WEAPONCRAFTING = "weaponcrafting"
    GEARCRAFTING = "gearcrafting"
    JEWELRYCRAFTING = "jewelrycrafting"
    COOKING = "cooking"
    ALCHEMY = "alchemy"


class CharacterSkin(str, Enum):
    MEN1 = "men1"
    MEN2 = "men2"
    MEN3 = "men3"
    WOMEN1 = "women1"
    WOMEN2 = "women2"
    WOMEN3 = "women3"
    CORRUPTED1 = "corrupted1"
    ZOMBIE1 = "zombie1"
    MARAUDER1 = "marauder1"
    GOBLIN1 = "goblin1"


class ConditionOperator(str, Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    LT = "lt"
    COST = "cost"
    HAS_ITEM = "has_item"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"


class CraftSkill(str, Enum):
    WEAPONCRAFTING = "weaponcrafting"
    GEARCRAFTING = "gearcrafting"
    JEWELRYCRAFTING = "jewelrycrafting"
    COOKING = "cooking"
    WOODCUTTING = "woodcutting"
    MINING = "mining"
    ALCHEMY = "alchemy"


class EffectSubtype(str, Enum):
    STAT = "stat"
    OTHER = "other"
    HEAL = "heal"
    BUFF = "buff"
    DEBUFF = "debuff"
    SPECIAL = "special"
    GATHERING = "gathering"
    TELEPORT = "teleport"
    GOLD = "gold"


class EffectType(str, Enum):
    EQUIPMENT = "equipment"
    CONSUMABLE = "consumable"
    COMBAT = "combat"


class FightResult(str, Enum):
    WIN = "win"
    LOSS = "loss"


class GatheringSkill(str, Enum):
    MINING = "mining"
    WOODCUTTING = "woodcutting"
    FISHING = "fishing"
    ALCHEMY = "alchemy"


class GEOrderType(str, Enum):
    SELL = "sell"
    BUY = "buy"


class ItemSlot(str, Enum):
    WEAPON = "weapon"
    SHIELD = "shield"
    HELMET = "helmet"
    BODY_ARMOR = "body_armor"
    LEG_ARMOR = "leg_armor"
    BOOTS = "boots"
    RING1 = "ring1"
    RING2 = "ring2"
    AMULET = "amulet"
    ARTIFACT1 = "artifact1"
    ARTIFACT2 = "artifact2"
    ARTIFACT3 = "artifact3"
    UTILITY1 = "utility1"
    UTILITY2 = "utility2"
    BAG = "bag"
    RUNE = "rune"


class ItemType(str, Enum):
    UTILITY = "utility"
    BODY_ARMOR = "body_armor"
    WEAPON = "weapon"
    RESOURCE = "resource"
    LEG_ARMOR = "leg_armor"
    HELMET = "helmet"
    BOOTS = "boots"
    SHIELD = "shield"
    AMULET = "amulet"
    RING = "ring"
    ARTIFACT = "artifact"
    CURRENCY = "currency"
    CONSUMABLE = "consumable"
    RUNE = "rune"
    BAG = "bag"


class LogType(str, Enum):
    SPAWN = "spawn"
    DELETE_CHARACTER = "delete_character"
    MOVEMENT = "movement"
    FIGHT = "fight"
    MULTI_FIGHT = "multi_fight"
    CRAFTING = "crafting"
    GATHERING = "gathering"
    BUY_GE = "buy_ge"
    SELL_GE = "sell_ge"
    CREATE_BUY_ORDER_GE = "create_buy_order_ge"
    FILL_BUY_ORDER_GE = "fill_buy_order_ge"
    BUY_NPC = "buy_npc"
    SELL_NPC = "sell_npc"
    CANCEL_GE = "cancel_ge"
    DELETE_ITEM = "delete_item"
    DEPOSIT_ITEM = "deposit_item"
    WITHDRAW_ITEM = "withdraw_item"
    DEPOSIT_GOLD = "deposit_gold"
    WITHDRAW_GOLD = "withdraw_gold"
    EQUIP = "equip"
    UNEQUIP = "unequip"
    NEW_TASK = "new_task"
    TASK_EXCHANGE = "task_exchange"
    TASK_CANCELLED = "task_cancelled"
    TASK_COMPLETED = "task_completed"
    TASK_TRADE = "task_trade"
    RECYCLING = "recycling"
    REST = "rest"
    USE = "use"
    BUY_BANK_EXPANSION = "buy_bank_expansion"
    ACHIEVEMENT = "achievement"
    GIVE_ITEM = "give_item"
    GIVE_GOLD = "give_gold"
    RECEIVE_ITEM = "receive_item"
    RECEIVE_GOLD = "receive_gold"
    CHANGE_SKIN = "change_skin"
    RENAME = "rename"
    TRANSITION = "transition"
    CLAIM_ITEM = "claim_item"
    SANDBOX_GIVE_GOLD = "sandbox_give_gold"
    SANDBOX_GIVE_ITEM = "sandbox_give_item"
    SANDBOX_GIVE_XP = "sandbox_give_xp"
    SANDBOX_RESET_ACCOUNT = "sandbox_reset_account"


class MapAccessType(str, Enum):
    STANDARD = "standard"
    TELEPORTATION = "teleportation"
    CONDITIONAL = "conditional"
    BLOCKED = "blocked"


class MapContentType(str, Enum):
    MONSTER = "monster"
    RESOURCE = "resource"
    WORKSHOP = "workshop"
    BANK = "bank"
    GRAND_EXCHANGE = "grand_exchange"
    TASKS_MASTER = "tasks_master"
    NPC = "npc"


class MapLayer(str, Enum):
    INTERIOR = "interior"
    OVERWORLD = "overworld"
    UNDERGROUND = "underground"


class MonsterType(str, Enum):
    NORMAL = "normal"
    ELITE = "elite"
    BOSS = "boss"


class NPCType(str, Enum):
    MERCHANT = "merchant"
    TRADER = "trader"


class PendingItemSource(str, Enum):
    ACHIEVEMENT = "achievement"
    GRAND_EXCHANGE = "grand_exchange"
    ADMIN = "admin"
    EVENT = "event"
    OTHER = "other"


class Skill(str, Enum):
    WEAPONCRAFTING = "weaponcrafting"
    GEARCRAFTING = "gearcrafting"
    JEWELRYCRAFTING = "jewelrycrafting"
    COOKING = "cooking"
    WOODCUTTING = "woodcutting"
    MINING = "mining"
    ALCHEMY = "alchemy"
    FISHING = "fishing"


class TaskType(str, Enum):
    MONSTERS = "monsters"
    ITEMS = "items"


class XPType(str, Enum):
    COMBAT = "combat"
    WEAPONCRAFTING = "weaponcrafting"
    GEARCRAFTING = "gearcrafting"
    JEWELRYCRAFTING = "jewelrycrafting"
    COOKING = "cooking"
    WOODCUTTING = "woodcutting"
    MINING = "mining"
    ALCHEMY = "alchemy"
    FISHING = "fishing"
