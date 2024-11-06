import re
import mwparserfromhell
import pandas as pd
from typing import Dict, List
from collections import defaultdict, OrderedDict


__TAG_REGEX = re.compile(r"<[^>]+>")


def clean_cell_content(mixed_content: mwparserfromhell.wikicode.Wikicode) -> str:
    cell_text = mixed_content.strip_code().replace("\u00a0", " ").strip()
    cell_text = __TAG_REGEX.sub("", cell_text)
    return cell_text


def convert_table_to_dict(wiki_tbl: mwparserfromhell.nodes.Tag) -> List[Dict[str, str]]:
    """
    Tabular data does not work well with LLM since the positional data is crucial, which can't be used by models in a reliable
    way. Repeating the headers for each data in a table is more LLM-friendly because we remove the positional requirements and
    the model can focus on the column header appropriately.

    TODO: Complex cross-tables like the ones in https://wiki.projectdiablo2.com/wiki/Breakpoints are not trivial to convert to this formet.

    mwparserfromhell iterates through the headers and then through the rows

    :param wiki_tbl:
    :return:
    """
    if wiki_tbl.contents.nodes[0].tag == "th" and wiki_tbl.contents.nodes[-1].contents.nodes[0].tag == "th":
        # Cross-table style of table
        table_data = defaultdict(list)
        current_header = ""
        for row_i, row_or_header in enumerate(wiki_tbl.contents.nodes):
            if row_or_header.tag == "th":
                if row_i == 0:
                    current_header = clean_cell_content(row_or_header.contents)
                else:
                    table_data[current_header].append(clean_cell_content(row_or_header.contents))
            elif row_or_header.tag == "tr":
                for cell in row_or_header.contents.nodes:
                    if cell.tag == "th":
                        current_header = clean_cell_content(cell.contents)
                    else:
                        table_data[current_header].append(clean_cell_content(cell.contents))
        return pd.DataFrame.from_dict(table_data).to_dict(orient="records", into=OrderedDict)
    elif wiki_tbl.contents.nodes[0].tag == "tr" and wiki_tbl.contents.nodes[-1].tag == "tr":
        # "Flipped table, i.e first row used as column headers
        table_data = defaultdict(list)
        current_header = ""
        for row in wiki_tbl.contents.nodes:
            for cell_i, cell in enumerate(row.contents.nodes):
                if cell_i == 0:
                    current_header = clean_cell_content(cell.contents)
                else:
                    table_data[current_header].append(clean_cell_content(cell.contents))
        return pd.DataFrame.from_dict(table_data).to_dict(orient="records", into=OrderedDict)
    elif "wikitable" in str(wiki_tbl.attributes):
        # Classic table
        table_elements = []
        headers = []
        for row_i, row_or_header in enumerate(wiki_tbl.contents.nodes):
            if row_or_header.tag == "th":
                headers.append(clean_cell_content(row_or_header.contents))
            elif row_or_header.tag == "tr":
                current_element = OrderedDict()
                for cell_i, cell in enumerate(row_or_header.contents.nodes):
                    current_element[headers[cell_i]] = clean_cell_content(cell.contents)
                table_elements.append(current_element)

        return table_elements
    else:
        # PD2's wiki uses "tables" for collapsible changelogs.
        return wiki_tbl.contents.strip_code(collapse=False)
