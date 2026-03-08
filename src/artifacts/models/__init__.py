"""Artifacts MMO API models."""

# Enums
from .enums import (
    AccountLeaderboardType,
    AccountStatus,
    AchievementType,
    ActionType,
    CharacterLeaderboardType,
    CharacterSkin,
    ConditionOperator,
    CraftSkill,
    EffectSubtype,
    EffectType,
    FightResult,
    GatheringSkill,
    GEOrderType,
    ItemSlot,
    ItemType,
    LogType,
    MapAccessType,
    MapContentType,
    MapLayer,
    MonsterType,
    NPCType,
    PendingItemSource,
    Skill,
    TaskType,
    XPType,
)

# Common
from .common import (
    ConditionSchema,
    CooldownSchema,
    DestinationSchema,
    DropSchema,
    GoldSchema,
    InventorySlot,
    RewardItemSchema,
    RewardsSchema,
    SimpleEffectSchema,
    SimpleItemSchema,
    StorageEffectSchema,
)

# Pagination
from .pagination import DataPage

# Domain models
from .account import AccountDetails, MyAccountDetails
from .achievements import (
    AccountAchievementObjectiveSchema,
    AccountAchievementSchema,
    AchievementObjectiveSchema,
    AchievementRewardsSchema,
    AchievementSchema,
)
from .badges import (
    BadgeConditionSchema,
    BadgeSchema,
    SeasonBadgeSchema,
    SeasonSchema,
    SeasonSkinSchema,
)
from .bank import BankExtensionSchema, BankSchema
from .character import ActiveCharacterSchema, CharacterSchema
from .combat import (
    CharacterFightSchema,
    CharacterMultiFightResultSchema,
    CombatResultSchema,
    CombatSimulationDataSchema,
    FakeCharacterSchema,
)
from .effects import EffectSchema
from .events import ActiveEventSchema, EventContentSchema, EventMapSchema, EventSchema
from .grand_exchange import (
    GEOrderCreatedSchema,
    GEOrderSchema,
    GETransactionSchema,
    GeOrderHistorySchema,
)
from .items import CraftSchema, ItemSchema
from .leaderboard import AccountLeaderboardSchema, CharacterLeaderboardSchema
from .logs import LogSchema, PendingItemSchema
from .maps import (
    AccessSchema,
    InteractionSchema,
    MapContentSchema,
    MapSchema,
    TransitionSchema,
)
from .monsters import DropRateSchema, MonsterSchema
from .npcs import NPCSchema, NpcItemTransactionSchema, SimpleNPCItem
from .resources import ResourceSchema
from .responses import (
    BankExtensionTransactionSchema,
    BankGoldTransactionSchema,
    BankItemTransactionSchema,
    ChangeSkinCharacterDataSchema,
    CharacterFightDataSchema,
    CharacterMovementDataSchema,
    CharacterRestDataSchema,
    CharacterTransitionDataSchema,
    ClaimPendingItemDataSchema,
    DeleteItemSchema,
    EquipRequestSchema,
    GEOrderTransactionSchema,
    GETransactionListSchema,
    GiveGoldDataSchema,
    GiveItemDataSchema,
    NpcMerchantTransactionSchema,
    RecyclingDataSchema,
    RecyclingItemsSchema,
    RewardDataSchema,
    SkillDataSchema,
    SkillInfoSchema,
    TaskCancelledSchema,
    TaskDataSchema,
    TaskTradeDataSchema,
    UseItemSchema,
)
from .sandbox import (
    SandboxGiveGoldDataSchema,
    SandboxGiveItemDataSchema,
    SandboxGiveXPDataSchema,
)
from .server import RateLimitSchema, StatusSchema
from .simulation import CombatSimulationRequestSchema
from .tasks import TaskFullSchema, TaskSchema, TaskTradeSchema
from .errors import ErrorSchema

__all__ = [
    # Enums
    "AccountLeaderboardType",
    "AccountStatus",
    "AchievementType",
    "ActionType",
    "CharacterLeaderboardType",
    "CharacterSkin",
    "ConditionOperator",
    "CraftSkill",
    "EffectSubtype",
    "EffectType",
    "FightResult",
    "GatheringSkill",
    "GEOrderType",
    "ItemSlot",
    "ItemType",
    "LogType",
    "MapAccessType",
    "MapContentType",
    "MapLayer",
    "MonsterType",
    "NPCType",
    "PendingItemSource",
    "Skill",
    "TaskType",
    "XPType",
    # Common
    "ConditionSchema",
    "CooldownSchema",
    "DestinationSchema",
    "DropSchema",
    "GoldSchema",
    "InventorySlot",
    "RewardItemSchema",
    "RewardsSchema",
    "SimpleEffectSchema",
    "SimpleItemSchema",
    "StorageEffectSchema",
    # Pagination
    "DataPage",
    # Domain
    "AccountDetails",
    "MyAccountDetails",
    "AccountAchievementObjectiveSchema",
    "AccountAchievementSchema",
    "AchievementObjectiveSchema",
    "AchievementRewardsSchema",
    "AchievementSchema",
    "BadgeConditionSchema",
    "BadgeSchema",
    "SeasonBadgeSchema",
    "SeasonSchema",
    "SeasonSkinSchema",
    "BankExtensionSchema",
    "BankSchema",
    "ActiveCharacterSchema",
    "CharacterSchema",
    "CharacterFightSchema",
    "CharacterMultiFightResultSchema",
    "CombatResultSchema",
    "CombatSimulationDataSchema",
    "FakeCharacterSchema",
    "EffectSchema",
    "ActiveEventSchema",
    "EventContentSchema",
    "EventMapSchema",
    "EventSchema",
    "GEOrderCreatedSchema",
    "GEOrderSchema",
    "GETransactionSchema",
    "GeOrderHistorySchema",
    "CraftSchema",
    "ItemSchema",
    "AccountLeaderboardSchema",
    "CharacterLeaderboardSchema",
    "LogSchema",
    "PendingItemSchema",
    "AccessSchema",
    "InteractionSchema",
    "MapContentSchema",
    "MapSchema",
    "TransitionSchema",
    "DropRateSchema",
    "MonsterSchema",
    "SimpleNPCItem",
    "NPCSchema",
    "NpcItemTransactionSchema",
    "ResourceSchema",
    # Responses
    "BankExtensionTransactionSchema",
    "BankGoldTransactionSchema",
    "BankItemTransactionSchema",
    "ChangeSkinCharacterDataSchema",
    "CharacterFightDataSchema",
    "CharacterMovementDataSchema",
    "CharacterRestDataSchema",
    "CharacterTransitionDataSchema",
    "ClaimPendingItemDataSchema",
    "DeleteItemSchema",
    "EquipRequestSchema",
    "GEOrderTransactionSchema",
    "GETransactionListSchema",
    "GiveGoldDataSchema",
    "GiveItemDataSchema",
    "NpcMerchantTransactionSchema",
    "RecyclingDataSchema",
    "RecyclingItemsSchema",
    "RewardDataSchema",
    "SkillDataSchema",
    "SkillInfoSchema",
    "TaskCancelledSchema",
    "TaskDataSchema",
    "TaskTradeDataSchema",
    "UseItemSchema",
    # Sandbox
    "SandboxGiveGoldDataSchema",
    "SandboxGiveItemDataSchema",
    "SandboxGiveXPDataSchema",
    # Server
    "RateLimitSchema",
    "StatusSchema",
    # Simulation
    "CombatSimulationRequestSchema",
    # Tasks
    "TaskFullSchema",
    "TaskSchema",
    "TaskTradeSchema",
    # Errors
    "ErrorSchema",
]
