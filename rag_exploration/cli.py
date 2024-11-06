import click
import mwparserfromhell
import xml.etree.ElementTree as ET
from rag_exploration.data.preprocess import convert_table_to_dict


@click.group()
def cli():
    pass


# TODO Refactor POC code to be cleaner and export to txt files
@cli.command()
def wiki2text():
    tree = ET.parse("data/pd2_wiki/wiki.projectdiablo2.com-wikidump/wiki.projectdiablo2.com_w-20241031-current.xml")

    for page in tree.findall("{http://www.mediawiki.org/xml/export-0.11/}page"):
        if page.find("{http://www.mediawiki.org/xml/export-0.11/}redirect") is None:
            page_text = page.find("./{http://www.mediawiki.org/xml/export-0.11/}revision/{http://www.mediawiki.org/xml/export-0.11/}text").text
            page_id = page.find("{http://www.mediawiki.org/xml/export-0.11/}id").text
            page_title = page.find("{http://www.mediawiki.org/xml/export-0.11/}title").text
            if page_id != "116":
                continue

            if page_text is not None:
                code = mwparserfromhell.parse(page_text)
                for tbl in code.filter_tags(matches='table'):
                    converted = convert_table_to_dict(tbl)
                # table =
                links = list(code.ifilter_wikilinks())
                # for l in links:
                #     code.remove(l)

                # with open(f"data/pd2_wiki/pages/{page_id}.txt", "w") as f:
                #     f.write(code.strip_code(collapse=False))


if __name__ == "__main__":
    cli()
