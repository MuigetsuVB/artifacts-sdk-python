"""Validation script -- test every model against the live API."""

import asyncio
import sys

from artifacts import AsyncArtifactsClient

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im11aWdldHN1QGhvdG1haWwuY29tIiwicGFzc3dvcmRfY2hhbmdlZCI6IjIwMjUtMDctMDFUMDI6NTI6NTQuMTYwWiJ9.PmNgx1e7Hb2Xm_4M_ypObuDHvKpy0eK52rRGz5ms390"

passed = 0
failed = 0
errors = []


async def test(name, coro):
    global passed, failed
    try:
        result = await coro
        passed += 1
        print(f"  OK  {name}")
        return result
    except Exception as e:
        failed += 1
        err = f"  FAIL {name}: {type(e).__name__}: {e}"
        errors.append(err)
        print(err)
        return None


async def main():
    global passed, failed

    async with AsyncArtifactsClient(token=TOKEN) as client:
        print("=== Model Validation Against Live API ===\n")

        # ---- Server ----
        print("[Server]")
        await test("server.get_status()", client.server.get_status())

        # ---- Accounts ----
        print("\n[Accounts]")
        await test("accounts.get('muigetsu')", client.accounts.get("muigetsu"))
        await test("accounts.get_achievements('muigetsu')", client.accounts.get_achievements("muigetsu", size=2))
        await test("accounts.get_characters('muigetsu')", client.accounts.get_characters("muigetsu"))

        # ---- My Account ----
        print("\n[My Account]")
        await test("my_account.get_details()", client.my_account.get_details())
        await test("my_account.get_bank()", client.my_account.get_bank())
        await test("my_account.get_bank_items()", client.my_account.get_bank_items(size=2))
        await test("my_account.get_ge_orders()", client.my_account.get_ge_orders(size=2))
        await test("my_account.get_ge_history()", client.my_account.get_ge_history(size=2))
        await test("my_account.get_pending_items()", client.my_account.get_pending_items(size=2))
        await test("my_account.get_characters()", client.my_account.get_characters())
        await test("my_account.get_all_logs()", client.my_account.get_all_logs(size=2))

        # ---- Characters ----
        print("\n[Characters]")
        await test("characters.get_active()", client.characters.get_active(size=2))
        char_info = await test("characters.get('Carlos')", client.characters.get("Carlos"))

        # ---- Items ----
        print("\n[Items]")
        await test("items.get_all(size=2)", client.items.get_all(size=2))
        await test("items.get('copper_ore')", client.items.get("copper_ore"))

        # ---- Monsters ----
        print("\n[Monsters]")
        await test("monsters.get_all(size=2)", client.monsters.get_all(size=2))
        await test("monsters.get('chicken')", client.monsters.get("chicken"))

        # ---- Maps ----
        print("\n[Maps]")
        await test("maps.get_all(size=2)", client.maps.get_all(size=2))
        await test("maps.get_by_position('overworld',0,1)", client.maps.get_by_position("overworld", 0, 1))
        await test("maps.get_by_id(1)", client.maps.get_by_id(1))

        # ---- Resources ----
        print("\n[Resources]")
        await test("resources.get_all(size=2)", client.resources.get_all(size=2))
        await test("resources.get('copper_rocks')", client.resources.get("copper_rocks"))

        # ---- NPCs ----
        print("\n[NPCs]")
        await test("npcs.get_all(size=2)", client.npcs.get_all(size=2))

        # ---- Achievements ----
        print("\n[Achievements]")
        await test("achievements.get_all(size=2)", client.achievements.get_all(size=2))

        # ---- Badges ----
        print("\n[Badges]")
        await test("badges.get_all(size=2)", client.badges.get_all(size=2))

        # ---- Effects ----
        print("\n[Effects]")
        await test("effects.get_all(size=2)", client.effects.get_all(size=2))

        # ---- Events ----
        print("\n[Events]")
        await test("events.get_all(size=2)", client.events.get_all(size=2))
        await test("events.get_all_active(size=2)", client.events.get_all_active(size=2))

        # ---- Grand Exchange ----
        print("\n[Grand Exchange]")
        await test("grand_exchange.get_orders(size=2)", client.grand_exchange.get_orders(size=2))

        # ---- Leaderboard ----
        print("\n[Leaderboard]")
        await test("leaderboard.get_characters(size=2)", client.leaderboard.get_characters(size=2))
        await test("leaderboard.get_accounts(size=2)", client.leaderboard.get_accounts(size=2))

        # ---- Tasks ----
        print("\n[Tasks]")
        await test("tasks.get_all(size=2)", client.tasks.get_all(size=2))
        await test("tasks.get_all_rewards(size=2)", client.tasks.get_all_rewards(size=2))

        # ---- Character Actions (read-only safe ones) ----
        print("\n[Character: Carlos]")
        char = client.character("Carlos")
        await test("char.get()", char.get())
        await test("char.get_logs(size=2)", char.get_logs(size=2))

        # ---- Summary ----
        print(f"\n{'='*50}")
        print(f"PASSED: {passed}")
        print(f"FAILED: {failed}")
        if errors:
            print(f"\nFailed tests:")
            for e in errors:
                print(e)
        print()

    return failed


if __name__ == "__main__":
    code = asyncio.run(main())
    sys.exit(code)
