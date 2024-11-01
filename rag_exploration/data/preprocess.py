import click
import mwparserfromhell
import xml.etree.ElementTree as ET

@click.group()
def cli():
    pass


test_val = """{| class="wikitable"
! # !! Rune !! Name !! Level !! Weapon !! Chest/Helm !! Shield !! Group
|-
| 1 || [[File:runeEl.png]] || <span class="d2-orange">'''El'''</span> || 11 || +50 to Attack Rating, <br> +1 to Light Radius || +15 Defense, <br> +1 to Light Radius || +15 Defense, <br> +1 to Light Radius || Low
|-
| 2 || [[File:runeEld.png]] || <span class="d2-orange">'''Eld'''</span> || 11 || +75% Damage to Undead, <br> +50 to Attack Rating against Undead || 15% Slower Stamina Drain || 7% Increased Chance of Blocking || Low
|-
| 3 || [[File:runeTir.png]] || <span class="d2-orange">'''Tir'''</span> || 13 || +2 to Mana after each Kill || +2 to Mana after each Kill || +2 to Mana after each Kill || Low
|-
| 4 || [[File:runeNef.png]] || <span class="d2-orange">'''Nef'''</span> || 13 || Knockback || +30 Defense vs. Missile || +30 Defense vs. Missile || Low
|-
| 5 || [[File:runeEth.png]] || <span class="d2-orange">'''Eth'''</span> || 15 || -25% Target Defense || Regenerate Mana 15% || Regenerate Mana 15% || Low
|-
| 6 || [[File:runeIth.png]] || <span class="d2-orange">'''Ith'''</span> || 15 || +9 to Maximum Damage || 15% Damage Taken Gained as Mana when Hit || 15% Damage Taken Gained as Mana when Hit || Low
|-
| 7 || [[File:runeTal.png]] || <span class="d2-orange">'''Tal'''</span> || 17 || +75 Poison Damage over 5 Seconds || Poison Resist +30% || Poison Resist +35% || Low
|-
| 8 || [[File:runeRal.png]] || <span class="d2-orange">'''Ral'''</span> || 19 || Adds 5-30 Fire Damage || Fire Resist +30% || Fire Resist +35% || Low
|-
| 9 || [[File:runeOrt.png]] || <span class="d2-orange">'''Ort'''</span> || 21 || Adds 1-50 Lightning Damage || Lightning Resist +30% || Lightning Resist +35% || Low
|-
| 10 || [[File:runeThul.png]] || <span class="d2-orange">'''Thul'''</span> || 23 || Adds 3-14 Cold Damage || Cold Resist +30% || Cold Resist +35% || Low
|-
| 11 || [[File:runeAmn.png]] || <span class="d2-orange">'''Amn'''</span> || 25 || 7% Life Stolen per Hit || Attacker Takes Damage of 14 || Attacker Takes Damage of 14 || Low
|-
| 12 || [[File:runeSol.png]] || <span class="d2-orange">'''Sol'''</span> || 27 || +9 to Minimum Damage || Physical Damage Taken Reduced by 7 || Physical Damage Taken Reduced by 7 || Low
|-
| 13 || [[File:runeShael.png]] || <span class="d2-orange">'''Shael'''</span> || 29 || +20% Increased Attack Speed || +20% Faster Hit Recovery || +20% Faster Block Rate || Low
|-
| 14 || [[File:runeDol.png]] || <span class="d2-orange">'''Dol'''</span> || 31 || <span class="nmod">20% Enhanced Damage</span><br><span class="omod">Hit Causes Monster to Flee 25%</span> || Replenish Life <span class="nmod">+10</span><br><span class="omod">Replenish Life +7</span> || Replenish Life <span class="nmod">+10</span><br><span class="omod">Replenish Life +7</span> || Low
|-
| 15 || [[File:runeHel.png]] || <span class="d2-orange">'''Hel'''</span> || -- || Requirements -20% || Requirements -15% || Requirements -15% || Mid
|-
| 16 || [[File:runeIo.png]] || <span class="d2-orange">'''Io'''</span> || 35 || +10 to Vitality || +10 to Vitality || +10 to Vitality || Mid
|-
| 17 || [[File:runeLum.png]] || <span class="d2-orange">'''Lum'''</span> || 37 || +10 to Energy || +10 to Energy || +10 to Energy || Mid
|-
| 18 || [[File:runeKo.png]] || <span class="d2-orange">'''Ko'''</span> || 39 || +10 to Dexterity || +10 to Dexterity || +10 to Dexterity || Mid
|-
| 19 || [[File:runeFal.png]] || <span class="d2-orange">'''Fal'''</span> || 41 || +10 to Strength || +10 to Strength || +10 to Strength || Mid
|-
| 20 || [[File:runeLem.png]] || <span class="d2-orange">'''Lem'''</span> || 43 || 75% Extra Gold From Monsters || 50% Extra Gold From Monsters || 50% Extra Gold From Monsters || Mid
|-
| 21 || [[File:runePul.png]] || <span class="d2-orange">'''Pul'''</span> || 45 || +75% Damage to Demons, <br> +100 to Attack Rating against Demons || +30% Enhanced Defense || +30% Enhanced Defense || Mid
|-
| 22 || [[File:runeUm.png]] || <span class="d2-orange">'''Um'''</span> || 47 || <span class="nmod">10%</span> Chance of Open Wounds,<br><span class="nmod">+120 Open Wounds Damage per Second</span><br><span class="omod">25% Chance of Open Wounds</span> || All Resistances +15 || All Resistances +22 || Mid
|-
| 23 || [[File:runeMal.png]] || <span class="d2-orange">'''Mal'''</span> || 49 || Prevent Monster Heal || Magic Damage Taken Reduced by 7 || Magic Damage Taken Reduced by 7 || Mid
|-
| 24 || [[File:runeIst.png]] || <span class="d2-orange">'''Ist'''</span> || 51 || 30% Better Chance of Getting Magic Items || <span class="nmod">30%</span> Better Chance of Getting Magic Items<br><span class="omod">25% Better Chance of Getting Magic Items</span> || <span class="nmod">30%</span> Better Chance of Getting Magic Items<br><span class="omod">25% Better Chance of Getting Magic Items</span> || Mid
|-
| 25 || [[File:runeGul.png]] || <span class="d2-orange">'''Gul'''</span> || 53 || 20% Bonus to Attack Rating || <span class="nmod">+4%</span> to Maximum Poison Resist<br><span class="omod">+5% to Maximum Poison Resist</span> || <span class="nmod">+4%</span> to Maximum Poison Resist<br><span class="omod">+5% to Maximum Poison Resist</span> || Mid
|-
| 26 || [[File:runeVex.png]] || <span class="d2-orange">'''Vex'''</span> || 55 || 7% Mana Stolen per Hit || <span class="nmod">+4%</span> to Maximum Fire Resist<br><span class="omod">+5% to Maximum Fire Resist</span> || <span class="nmod">+4%</span> to Maximum Fire Resist<br><span class="omod">+5% to Maximum Fire Resist</span> || High
|-
| 27 || [[File:runeOhm.png]] || <span class="d2-orange">'''Ohm'''</span> || 57 || <span class="nmod">+45%</span> Enhanced Damage<br><span class="omod">+50% Enhanced Damage</span> || <span class="nmod">+4%</span> to Maximum Cold Resist<br><span class="omod">+5% to Maximum Cold Resist</span> || <span class="nmod">+4%</span> to Maximum Cold Resist<br><span class="omod">+5% to Maximum Cold Resist</span> || High
|-
| 28 || [[File:runeLo.png]] || <span class="d2-orange">'''Lo'''</span> || 59 || 20% Deadly Strike || <span class="nmod">+4%</span> to Maximum Lightning Resist<br><span class="omod">+5% to Maximum Lightning Resist</span> || <span class="nmod">+4%</span> to Maximum Lightning Resist<br><span class="omod">+5% to Maximum Lightning Resist</span> || High
|-
| 29 || [[File:runeSur.png]] || <span class="d2-orange">'''Sur'''</span> || 61 || <span class="nmod">+4 Life after each Kill</span><br><span class="omod">Hit Blinds Target</span> || Increase Maximum Mana 5% || +50 to Mana || High
|-
| 30 || [[File:runeBer.png]] || <span class="d2-orange">'''Ber'''</span> || 63 || 20% Chance of Crushing Blow || Physical Damage Taken Reduced by <span class="nmod">5%</span><br><span class="omod">Physical Damage Taken Reduced by 8%</span> || Physical Damage Taken Reduced by <span class="nmod">5%</span><br><span class="omod">Physical Damage Taken Reduced by 8%</span> || High
|-
| 31 || [[File:runeJah.png]] || <span class="d2-orange">'''Jah'''</span> || 65 || Ignore Target's Defense || Increase Maximum Life 5% || <span class="nmod">+75</span> to Life<br><span class="omod">+50 to Life</span> || High
|-
| 32 || [[File:runeCham.png]] || <span class="d2-orange">'''Cham'''</span> || 67 || Freezes Target +3 || Cannot Be Frozen || Cannot Be Frozen || High
|-
| 33 || [[File:runeZod.png]] || <span class="d2-orange">'''Zod'''</span> || 69 || Indestructible || Indestructible || Indestructible || High
|}"""


lol = [
    {
        "Name": "Chipped Sapphire",
        "Level": 1,
        "Weapon": "Adds 1-3 Cold Damage",
        "Chest/Helm": "+10 to Mana",
        "Shield": "Cold Resist +12%",
    },
    {
        "Name": "Chipped Emerald",
        "Level": 1,
        "Weapon": "+10 Poison Damage over 3 Seconds",
        "Chest/Helm": "+3 to Dexterity",
        "Shield": "Poison Resist +12%",
    },
    {
        "Name": "Chipped Topaz",
        "Level": 1,
        "Weapon": "Adds 1-8 Lightning Damage",
        "Chest/Helm": "+9% Better Chance of Getting Magic Items",
        "Shield": "Lightning Resist +12%",
    },
]

lol2 = [
    {
        "Hard Level": 0,
        "Arrows": 1
    },
    {
        "Hard Level": 1,
        "Arrows": 1
    },
    {
        "Hard Level": 2,
        "Arrows": 1
    },
    {
        "Hard Level": 3,
        "Arrows": 1
    },
    {
        "Hard Level": 4,
        "Arrows": 1
    },
    {
        "Hard Level": 5,
        "Arrows": 2
    },
    {
        "Hard Level": 6,
        "Arrows": 2
    },
]

lol3 = [
    {
        "Level": 1,
        "Arrows": 2,
        "Attack Rating +%": 10,
        "Fire Damage (min)": 8,
        "Fire Damage (max)": 12,
        "Mana Cost": 1.5
    },
    {
        "Level": 2,
        "Arrows": 2,
        "Attack Rating +%": 20,
        "Fire Damage (min)": 12,
        "Fire Damage (max)": 16,
        "Mana Cost": 1.6
    },
]

lol4 = [
    {
        "Level": 1,
        "Arrows": 2,
        "Attack Rating +%": 10,
        "Cold Damage (min)": 8,
        "Cold Damage (max)": 12,
        "Mana Cost": 1.5
    },
    {
        "Level": 2,
        "Arrows": 2,
        "Attack Rating +%": 20,
        "Cold Damage (min)": 12,
        "Cold Damage (max)": 16,
        "Mana Cost": 1.6
    },
]

# def convert_table

@cli.command()
def wiki2text():
    tree = ET.parse("data/pd2_wiki/wiki.projectdiablo2.com_w-20241031-current.xml")

    for page in tree.findall("{http://www.mediawiki.org/xml/export-0.11/}page"):
        if page.find("{http://www.mediawiki.org/xml/export-0.11/}redirect") is None:
            page_text = page.find("./{http://www.mediawiki.org/xml/export-0.11/}revision/{http://www.mediawiki.org/xml/export-0.11/}text").text
            page_id = page.find("{http://www.mediawiki.org/xml/export-0.11/}id").text
            page_title = page.find("{http://www.mediawiki.org/xml/export-0.11/}title").text

            if page_text is not None:
                code = mwparserfromhell.parse(page_text)
                links = list(code.ifilter_wikilinks())
                # for l in links:
                #     code.remove(l)

                with open(f"data/pd2_wiki/pages/{page_id}.txt", "w") as f:
                    f.write(code.strip_code(collapse=False))


if __name__ == "__main__":
    cli()
