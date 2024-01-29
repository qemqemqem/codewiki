from pathlib import Path

from writing.code_wiki_manager import CodeWikiManager
from writing.wiki_manager import WikiManager
from writing.write_articles import add_articles_to_wiki

def load_wiki(wiki_name: str = "testing", code_path: Path = Path("/home/keenan/Dev/mtgrandom")) -> WikiManager:
    wiki_path = Path(f"multiverse/{wiki_name}/wiki/docs")

    # Load all articles
    wiki = CodeWikiManager(wiki_name, wiki_path, code_path=code_path)

    # Get all links
    links = wiki.get_all_links()

    # Sort links by count
    links = {k: v for k, v in sorted(links.items(), key=lambda item: item[1], reverse=False)}

    # Print all links
    print("All links:")
    for link, count in links.items():
        print(f"{link} ({count})")

    return wiki


if __name__ == "__main__":
    load_wiki(wiki_name="wiki_mtgrandom", code_path=Path("/home/keenan/Dev/mtgrandom"))
    # add_articles_to_wiki("world1", num_new_articles=1000)
