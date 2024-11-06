import pytest
import mwparserfromhell
from rag_exploration.data.preprocess import convert_table_to_dict


# TODO Handle no-header tables (which exist)
# TODO Handle cross-table edge cases
@pytest.mark.parametrize(
    "raw_tbl,expected",
    [
        (
            '{| class="wikitable"\n! Rune !! Name\n|-\n|r1 || n1\n|-\n|r2 || n2\n|}',
            [{"Rune": "r1", "Name": "n1"}, {"Rune": "r2", "Name": "n2"}]
        ),
        (
            '{| class="wikitable"\n! Rune !! Name\n|-\n|r1 || n1\n|}',
            [{"Rune": "r1", "Name": "n1"},]
        ),
        (
            '{| class="wikitable"\n! Rune\n|-\n|r1 \n|-\n|r2\n|}',
            [{"Rune": "r1"}, {"Rune": "r2"}]
        ),
        (
            '{| class="wikitable"\n! Rune \n|-\n|r1\n|}',
            [{"Rune": "r1"}, ]
        ),
        (
            '{| class="wikitable"\n! Lvl !! 1 !! 2\n|-\n!Dmg\n|d1||d2\n|-\n!Mana\n|m1||m2\n|}',
            [{"Lvl": "1", "Dmg": "d1", "Mana": "m1"}, {"Lvl": "2", "Dmg": "d2", "Mana": "m2"}]
        ),
    ],
    ids=[
        "Table with multiple columns and multiple rows",
        "Table with multiple columns and a single row",
        "Table with a single column and multiple rows",
        "Table with a single column and a single row",
        "Cross-table with multiple columns and multiple rows"
    ]
)
def test_convert_table_to_dict(raw_tbl, expected):
    parsed_table = mwparserfromhell.parse(raw_tbl)
    converted_table = convert_table_to_dict(parsed_table.nodes[0])
    assert converted_table == expected