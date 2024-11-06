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


# TODO Handle no-header tables (which exist)
def convert_table_to_dict(wiki_tbl: mwparserfromhell.nodes.Tag) -> List[Dict[str, str]]:
    """
    mwparserfromhell iterates through the headers and then through the rows

    :param wiki_tbl:
    :return:
    """
    if wiki_tbl.contents.nodes[-1].contents.nodes[0].tag == "th":
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
    else:
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
