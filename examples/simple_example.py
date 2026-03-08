"""Beginner example -- zero async knowledge required.

Just replace TOKEN with your JWT token and run:
    python beginner_sync.py
"""

from artifacts import ArtifactsClient

TOKEN = "your_token_here"

with ArtifactsClient(token=TOKEN) as client:
    # Pick your first character
    characters = client.my_account.get_characters()
    char = client.character(characters[0].name)

    info = char.get()
    print(f"Playing as {info.name} (level {info.level})")

    # Move to a chicken spot and fight
    char.move(x=0, y=1)
    result = char.fight()
    fight = result.fight
    print(f"Fight result: {fight.result.value} in {fight.turns} turns")

    # Rest if HP is low
    updated = result.characters[0]
    if updated.hp < updated.max_hp * 0.5:
        rest = char.rest()
        print(f"Rested: +{rest.hp_restored} HP")

    print("Done!")
