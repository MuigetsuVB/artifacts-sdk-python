# Artifacts MMO - Python SDK

Python SDK for the [Artifacts MMO](https://artifactsmmo.com/) API. Control up to 5 characters simultaneously with full type safety, automatic cooldowns, and retry.

**Compatible with Artifacts MMO API v7**

- **65 endpoints** covered (every single one)
- **Sync & async** -- beginners use `ArtifactsClient`, advanced users use `AsyncArtifactsClient` with `asyncio`
- **Auto-cooldown** -- the SDK waits automatically after each action (opt-out globally, per-character, or per-call)
- **Auto-retry** -- exponential backoff on rate limits, server errors, and cooldown conflicts
- **Game-oriented** -- `char.skills.craft()`, `char.bank.deposit_gold()`, `char.ge.sell()`
- **Typed** with Pydantic models -- full IDE autocompletion

## Installation

```bash
pip install artifacts-mmo
```

**Requirements:** Python 3.10+

## Quick Start (Sync)

No `async`/`await` needed -- every call blocks until complete:

```python
from artifacts import ArtifactsClient

with ArtifactsClient(token="your_token_here") as client:
    char = client.character("MyCharacter")

    info = char.get()
    print(f"{info.name} lv{info.level} HP={info.hp}/{info.max_hp}")

    char.move(x=0, y=1)           # auto-waits cooldown
    result = char.fight()          # auto-waits cooldown
    print(f"Result: {result.fight.result.value}")

    char.skills.gather()           # gather resource
    char.bank.deposit_gold(quantity=100)
```

## Quick Start (Async)

```python
import asyncio
from artifacts import AsyncArtifactsClient

async def main():
    async with AsyncArtifactsClient(token="your_token_here") as client:
        char = client.character("MyCharacter")

        info = await char.get()
        print(f"{info.name} lv{info.level} HP={info.hp}/{info.max_hp}")

        await char.move(x=0, y=1)       # auto-waits cooldown
        result = await char.fight()      # auto-waits cooldown
        print(f"Result: {result.fight.result.value}")

asyncio.run(main())
```

## Getting a Token

You need a JWT token to authenticate. Generate one from your account credentials:

```python
async with AsyncArtifactsClient() as client:
    token = await client.token.generate("your_username", "your_password")
    print(token)  # Use this token from now on
```

Or use a token you already have from the Artifacts website.

## Custom API URL

By default the SDK connects to `https://api.artifactsmmo.com/`. To use a different server (e.g. sandbox):

```python
client = ArtifactsClient(
    token="your_token",
    base_url="https://api.sandbox.artifactsmmo.com",
)
```

---

## Architecture Overview

```
ArtifactsClient / AsyncArtifactsClient
├── .character("name")     -> Character
│   ├── .move(), .fight(), .rest(), .transition()    (direct)
│   ├── .get(), .get_logs()                          (info)
│   ├── .inventory         -> use(), delete()
│   ├── .bank              -> deposit_gold(), withdraw_gold(), deposit_items(), withdraw_items(), buy_expansion()
│   ├── .equipment         -> equip(), unequip()
│   ├── .skills            -> gather(), craft(), recycle()
│   ├── .tasks             -> new(), complete(), exchange(), trade(), cancel()
│   ├── .ge                -> buy(), sell(), create_buy_order(), fill(), cancel()
│   ├── .trading           -> npc_buy(), npc_sell(), give_gold(), give_items()
│   └── .claim_item(), .change_skin()                (misc)
├── .server                -> ServerAPI
├── .token                 -> TokenAPI
├── .accounts              -> AccountsAPI
├── .my_account            -> MyAccountAPI
├── .characters            -> CharactersAPI
├── .items                 -> ItemsAPI
├── .monsters              -> MonstersAPI
├── .maps                  -> MapsAPI
├── .resources             -> ResourcesAPI
├── .npcs                  -> NPCsAPI
├── .events                -> EventsAPI
├── .achievements          -> AchievementsAPI
├── .badges                -> BadgesAPI
├── .effects               -> EffectsAPI
├── .grand_exchange        -> GrandExchangeAPI
├── .leaderboard           -> LeaderboardAPI
├── .tasks                 -> TasksAPI
├── .simulation            -> SimulationAPI
└── .sandbox               -> SandboxAPI
```

---

## Character Actions

Create a character controller, then call action methods. The SDK **automatically waits** for cooldowns after each action.

```python
char = client.character("MyCharacter")
```

### Movement

```python
# Move by coordinates
char.move(x=2, y=3)

# Move by map ID
char.move(map_id=42)

# Layer transition (e.g. enter a building)
char.transition()
```

### Combat

```python
# Solo fight
result = char.fight()
fight = result.fight
print(f"{fight.result.value} in {fight.turns} turns")
for cr in fight.characters:
    print(f"  +{cr.xp}xp +{cr.gold}g, drops={[d.code for d in cr.drops]}")

# Boss fight with other characters (up to 3 total)
result = char.fight(participants=["Char2", "Char3"])

# Rest to recover HP
result = char.rest()
print(f"Restored {result.hp_restored} HP")
```

### Equipment

```python
from artifacts.models.enums import ItemSlot

char.equipment.equip(code="iron_sword", slot=ItemSlot.WEAPON)
char.equipment.unequip(slot=ItemSlot.WEAPON)
```

### Skills (Gathering, Crafting, Recycling)

```python
# Gather (character must be on a resource tile)
result = char.skills.gather()
print(f"+{result.details.xp}xp, got: {[d.code for d in result.details.items]}")

# Craft (character must be at a workshop)
char.skills.craft(code="iron_sword", quantity=1)

# Recycle equipment into materials
char.skills.recycle(code="iron_sword", quantity=1)
```

### Inventory

```python
# Use a consumable
char.inventory.use(code="healing_potion", quantity=1)

# Delete an item from inventory
char.inventory.delete(code="junk_item", quantity=5)
```

### Bank

```python
# Character must be on a bank tile

# Gold
char.bank.deposit_gold(quantity=500)
char.bank.withdraw_gold(quantity=200)

# Items
from artifacts.models.common import SimpleItemSchema
items = [SimpleItemSchema(code="copper_ore", quantity=50)]
char.bank.deposit_items(items)
char.bank.withdraw_items(items)

# Buy a bank expansion (+20 slots)
char.bank.buy_expansion()
```

### NPC Trading

```python
# Character must be on an NPC tile
char.trading.npc_buy(code="wooden_staff", quantity=1)
char.trading.npc_sell(code="wooden_staff", quantity=1)
```

### Grand Exchange

```python
# Character must be on a GE tile

# Create a sell order
char.ge.sell(code="copper_ore", quantity=100, price=5)

# Buy from an existing sell order
char.ge.buy(id="order_id_here", quantity=10)

# Create a buy order (gold is locked upfront)
char.ge.create_buy_order(code="copper_ore", quantity=100, price=5)

# Fill someone's buy order
char.ge.fill(id="order_id_here", quantity=50)

# Cancel your order
char.ge.cancel(id="order_id_here")
```

### Tasks

```python
# Character must be at a tasks master

# Accept a new task
result = char.tasks.new()
print(f"Task: {result.task.code} ({result.task.type.value}) x{result.task.total}")

# Trade items for the task
char.tasks.trade(code="copper_ore", quantity=10)

# Complete the task
char.tasks.complete()

# Exchange 6 task coins for a random reward
char.tasks.exchange()

# Cancel current task (costs 1 task coin)
char.tasks.cancel()
```

### Give Items/Gold to Another Character

```python
# Characters must be on the same map tile

char.trading.give_gold(quantity=100, character="OtherChar")

from artifacts.models.common import SimpleItemSchema
items = [SimpleItemSchema(code="copper_ore", quantity=20)]
char.trading.give_items(items=items, character="OtherChar")
```

### Other

```python
# Claim a pending item
char.claim_item(id=123)

# Change character skin
from artifacts.models.enums import CharacterSkin
char.change_skin(skin=CharacterSkin.MEN2)

# View action logs
logs = char.get_logs(page=1, size=20)
for log in logs.data:
    print(f"  [{log.type.value}] {log.description}")
```

---

## Cooldown Handling

By default, the SDK **automatically waits** for cooldowns after each action. You never need to call `wait_for_cooldown()` unless you disable auto-wait.

### Override per call

```python
# Skip the auto-wait for this specific call
result = char.fight(wait=False)
# Do something while the cooldown runs...
```

### Override per character

```python
char = client.character("SpeedRunner", auto_wait=False)
# All actions on this character return immediately
```

### Override globally

Set `auto_wait=False` at construction time to default all characters to no-wait:

```python
client = ArtifactsClient(token="...", auto_wait=False)
# All characters created from here return immediately
```

Or toggle it at any point **after** construction -- all characters that were created without an explicit per-character override are affected instantly:

```python
client = ArtifactsClient(token="...")
char1 = client.character("Alice")   # follows client setting
char2 = client.character("Bob")     # follows client setting
char3 = client.character("Carol", auto_wait=False)  # isolated, unaffected by global toggle

# Later in the program:
client.auto_wait = False  # char1 and char2 stop waiting; char3 unchanged
client.auto_wait = True   # char1 and char2 resume waiting; char3 unchanged
```

### Manual cooldown handling (when auto_wait is disabled)

```python
from artifacts import wait_for_cooldown, cooldown_seconds

result = char.fight(wait=False)

# Option 1: Helper that sleeps for the remaining duration
await wait_for_cooldown(result.cooldown)

# Option 2: Read the value
seconds = cooldown_seconds(result.cooldown)
print(f"Cooldown: {seconds}s remaining")

# Option 3: Access the raw CooldownSchema
cd = result.cooldown
print(f"Total: {cd.total_seconds}s, Reason: {cd.reason.value}")
```

---

## Retry & Rate Limiting

The SDK automatically retries on transient errors with exponential backoff:

- **429** (rate limit) -- waits and retries
- **499** (cooldown active) -- waits for remaining cooldown, then retries
- **500, 502, 503, 504** (server errors) -- exponential backoff with jitter

### Default configuration

```python
# These are the defaults -- no configuration needed
client = ArtifactsClient(token="...")
# max_retries=3, base_delay=1.0s, max_delay=30.0s
```

### Custom configuration

```python
from artifacts import ArtifactsClient, RetryConfig

client = ArtifactsClient(
    token="...",
    retry=RetryConfig(
        max_retries=5,
        base_delay=0.5,
        max_delay=60.0,
        retry_on_cooldown=False,  # don't auto-retry on cooldown
    ),
)
```

---

## Logging

Enable SDK logging with a single call:

```python
import logging
import artifacts

artifacts.setup_logging()                  # INFO level
artifacts.setup_logging(logging.DEBUG)     # verbose (request/response details)
```

---

## Fetching Game Data

All game data endpoints are read-only and return typed Pydantic models. Paginated results come wrapped in `DataPage[T]`.

### Items

```python
# Get a single item by code
item = client.items.get("copper_ore")
print(f"{item.name} (lv{item.level}, type={item.type.value})")

# List items with filters
# Parameters: min_level, max_level, name, type, craft_skill, craft_material, page, size
page = client.items.get_all(min_level=1, max_level=10, type="resource", size=20)
for item in page.data:
    print(f"  {item.code}: {item.name}")
```

### Monsters

```python
monster = client.monsters.get("chicken")
print(f"{monster.name} lv{monster.level} HP={monster.hp}")

# Parameters: min_level, max_level, name, drop, page, size
page = client.monsters.get_all(min_level=1, max_level=5)
```

### Maps

```python
# Find maps containing a specific monster
# Parameters: layer, content_type, content_code, hide_blocked_maps, page, size
maps = client.maps.get_all(content_type="monster", content_code="chicken")
for m in maps.data:
    print(f"  ({m.x},{m.y}) layer={m.layer.value}")

# Get a specific map tile
tile = client.maps.get_by_position("overworld", 0, 1)
```

### Resources

```python
# Parameters: min_level, max_level, skill, drop, page, size
page = client.resources.get_all(skill="mining", min_level=1)
for r in page.data:
    print(f"  {r.code} (lv{r.level}) drops: {[d.code for d in r.drops]}")
```

### NPCs

```python
# Parameters: name, type, currency, item, page, size
npcs = client.npcs.get_all()
items = client.npcs.get_items("merchant_1")
for i in items.data:
    print(f"  {i.code} buy={i.buy_price} sell={i.sell_price}")
```

### Other game data

```python
# Achievements, Badges, Effects
# Achievement parameters: type, page, size
# Badge/Effect parameters: page, size
all_achievements = client.achievements.get_all()
badges = client.badges.get_all()
effects = client.effects.get_all()

# Events
# Parameters: page, size
active = client.events.get_all_active()

# Tasks
# Parameters: min_level, max_level, skill, type, page, size
tasks = client.tasks.get_all(type="monsters", min_level=1)
# Parameters: page, size
rewards = client.tasks.get_all_rewards()

# Leaderboard
# Character/Account parameters: sort, name, page, size
top_chars = client.leaderboard.get_characters(sort="combat")
top_accounts = client.leaderboard.get_accounts(sort="gold")

# Grand Exchange
# Order parameters: code, account, type, page, size
orders = client.grand_exchange.get_orders(code="copper_ore")
# History parameters: account, page, size
history = client.grand_exchange.get_history("copper_ore")
```

### Pagination

All list endpoints return a `DataPage[T]`:

```python
page = client.items.get_all(page=1, size=50)
page.data    # list[ItemSchema] -- the items on this page
page.total   # int -- total number of items across all pages
page.page    # int -- current page number
page.pages   # int -- total number of pages
page.size    # int -- page size
```

---

## Account & Bank

```python
account = client.my_account.get_details()
print(f"{account.username} -- gems={account.gems}")

bank = client.my_account.get_bank()
print(f"Gold: {bank.gold}")

bank_items = client.my_account.get_bank_items()
for item in bank_items.data:
    print(f"  {item.code} x{item.quantity}")

chars = client.my_account.get_characters()
orders = client.my_account.get_ge_orders()
pending = client.my_account.get_pending_items()
```

---

## Error Handling

The SDK raises typed exceptions mapped to API error codes:

```python
from artifacts.errors import (
    ArtifactsAPIError,       # Base class for all API errors
    RetryExhaustedError,     # All retry attempts exhausted
    CooldownActiveError,     # 499 -- character is in cooldown
    ActionInProgressError,   # 486 -- action already running
    InventoryFullError,      # 497 -- inventory full
    InsufficientGoldError,   # 492 -- not enough gold
    NotFoundError,           # 404 -- resource not found
    ContentNotOnMapError,    # 598 -- no monster/resource here
    AlreadyAtDestinationError, # 490 -- already at target
    SkillLevelTooLowError,   # 493 -- skill level too low
    EquipmentSlotError,      # 491 -- equipment slot issue
    MapBlockedError,         # 596 -- map is blocked
    NoPathError,             # 595 -- no path to destination
    MemberRequiredError,     # 451 -- member/founder required
    ConditionsNotMetError,   # 496 -- conditions not met
    TaskError,               # 474-489 -- task-related errors
    GrandExchangeError,      # 433-438 -- GE errors
    ValidationError,         # 422 -- invalid request
)
```

Example:

```python
try:
    result = char.fight()
except InventoryFullError:
    print("Inventory full! Go deposit at the bank.")
except ContentNotOnMapError:
    print("No monster on this tile.")
except RetryExhaustedError as e:
    print(f"Failed after all retries: {e.last_exception}")
except ArtifactsAPIError as e:
    print(f"API error [{e.code}]: {e.message}")
```

Note: `CooldownActiveError` is usually handled automatically by the retry system. You only need to catch it if you disabled `retry_on_cooldown`.

---

## Running Multiple Characters in Parallel

Use `asyncio.gather()` with the async client:

```python
import asyncio
from artifacts import AsyncArtifactsClient

async def combat_loop(char):
    for _ in range(10):
        info = await char.get()
        if info.hp < info.max_hp * 0.3:
            await char.rest()
            continue
        result = await char.fight()
        print(f"[{char.name}] {result.fight.result.value}")

async def main():
    async with AsyncArtifactsClient(token="your_token") as client:
        names = ["Char1", "Char2", "Char3", "Char4", "Char5"]
        chars = [client.character(n) for n in names]
        await asyncio.gather(*[combat_loop(c) for c in chars])

asyncio.run(main())
```

See `examples/combat_loop_5chars.py` for a complete example.

---

## Character Management

```python
from artifacts.models.enums import CharacterSkin

# Create a character (max 5 per account)
new_char = client.characters.create("NewHero", CharacterSkin.MEN1)

# Delete a character
deleted = client.characters.delete("NewHero")

# List all active characters on the server
active = client.characters.get_active()

# Get any character's public info
info = client.characters.get("SomePlayer")
```

---

## Simulation (Members Only)

```python
from artifacts.models.sandbox import FakeCharacterSchema

fake = FakeCharacterSchema(
    level=20,
    weapon_slot="iron_sword",
    body_armor_slot="iron_armor",
)
result = client.simulation.fight(
    characters=[fake],
    monster="ogre",
    iterations=100,
)
print(f"Winrate: {result.winrate:.1%} ({result.wins}W / {result.losses}L)")
```

---

## Sandbox (Sandbox Server Only)

When using the sandbox server (`base_url="https://api.sandbox.artifactsmmo.com"`):

```python
client.sandbox.give_gold("MyChar", 10000)
client.sandbox.give_item("MyChar", "iron_sword", 5)
client.sandbox.give_xp("MyChar", "combat", 5000)
client.sandbox.spawn_event("event_code")
client.sandbox.reset_account()
```

---

## Complete API Reference

### Client Sub-Accessors

| Accessor | Methods |
|---|---|
| `client.server` | `get_status()` |
| `client.token` | `generate(username, password)` |
| `client.accounts` | `create()`, `forgot_password()`, `reset_password()`, `get()`, `get_achievements()`, `get_characters()` |
| `client.my_account` | `get_details()`, `get_bank()`, `get_bank_items()`, `get_ge_orders()`, `get_ge_history()`, `get_pending_items()`, `change_password()`, `get_characters()`, `get_all_logs()` |
| `client.characters` | `create()`, `delete()`, `get_active()`, `get()` |
| `client.items` | `get_all()`, `get()` |
| `client.monsters` | `get_all()`, `get()` |
| `client.maps` | `get_all()`, `get_layer()`, `get_by_position()`, `get_by_id()` |
| `client.resources` | `get_all()`, `get()` |
| `client.npcs` | `get_all()`, `get()`, `get_all_items()`, `get_items()` |
| `client.events` | `get_all_active()`, `get_all()`, `spawn()` |
| `client.achievements` | `get_all()`, `get()` |
| `client.badges` | `get_all()`, `get()` |
| `client.effects` | `get_all()`, `get()` |
| `client.grand_exchange` | `get_history()`, `get_orders()`, `get_order()` |
| `client.leaderboard` | `get_characters()`, `get_accounts()` |
| `client.tasks` | `get_all()`, `get()`, `get_all_rewards()`, `get_reward()` |
| `client.simulation` | `fight()` |
| `client.sandbox` | `give_gold()`, `give_item()`, `give_xp()`, `spawn_event()`, `reset_account()` |

### Character Methods (direct)

| Category | Methods |
|---|---|
| Info | `get()`, `get_logs()` |
| Movement | `move(x, y)`, `move(map_id)`, `transition()` |
| Combat | `fight()`, `rest()` |
| Misc | `claim_item(id)`, `change_skin(skin)` |

### Character Domain Sub-Objects

| Domain | Methods |
|---|---|
| `char.inventory` | `use(code, qty)`, `delete(code, qty)` |
| `char.bank` | `deposit_gold(qty)`, `withdraw_gold(qty)`, `deposit_items(items)`, `withdraw_items(items)`, `buy_expansion()` |
| `char.equipment` | `equip(code, slot)`, `unequip(slot)` |
| `char.skills` | `gather()`, `craft(code, qty)`, `recycle(code, qty)` |
| `char.tasks` | `new()`, `complete()`, `exchange()`, `trade(code, qty)`, `cancel()` |
| `char.ge` | `buy(id, qty)`, `sell(code, qty, price)`, `create_buy_order(code, qty, price)`, `fill(id, qty)`, `cancel(id)` |
| `char.trading` | `npc_buy(code, qty)`, `npc_sell(code, qty)`, `give_gold(qty, character)`, `give_items(items, character)` |
