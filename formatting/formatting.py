import os
import re
from typing import List


# Formatting notes:
# - Names cannot have square brackets in them, because of the '[^\]]' regex pattern


def sanitize_article_name(article_name: str) -> str:
    # In standard URLs, a comma is typically encoded as %2C. Use regex to do this replacement
    # This function takes a file name and converts it to a format that's good to use as a URL within the markdown file
    article_name = re.sub(r",", "%2C", article_name)
    article_name = re.sub(r" ", "%20", article_name)

    if "/" in article_name:
        print(f"WARNING: Article name {article_name} contains a slash, which may cause problems with the wiki.")

    return article_name


def reverse_sanitize_article_name(article_name: str) -> str:
    # This needs to be kept in sync with the function above
    article_name = re.sub(r"%2C", ",", article_name)
    article_name = re.sub(r"%20", " ", article_name)
    return article_name


def convert_markdown_to_wikitext_links(markdown_text: str) -> str:
    # Use regular expressions to find all [text](link) patterns, and replace them with [[link|text]] or just [[link]] if text==link
    t = markdown_text
    t = re.sub(r"\[([^\]]*?)\]\(([^\]]*?)\.md\)", r"[[\2|\1]]", t)

    # reverse_sanitize_article_name text with in [[brackets]]
    t = re.sub(r"\[\[(.*?)\]\]", lambda m: f"[[{reverse_sanitize_article_name(m.group(1))}]]", t)

    # Find all links like [[\1|\1]] and replace them with just [[\1]], but only in cases where the text before and after the '|' are the same
    pipe_links = re.findall(r"\[\[([^\]]*?)\|([^\]]*?)\]\]", t)
    for pl in pipe_links:
        if custom_title_case(pl[0]) == pl[1]:
            t = t.replace(f"[[{pl[0]}|{pl[1]}]]", f"[[{reverse_sanitize_article_name(pl[0])}]]")

    return t


def convert_wikitext_to_markdown_links(wikitext: str) -> str:
    t = wikitext

    # Use regular expressions to convert [[link|text]] to [text](link)
    t = re.sub(r"\[\[([^\]]*?)\|([^\]]*?)\]\]", r"[\2](\1.md)", t)

    # Use regular expressions to convert [[link]] to [link](link)
    t = re.sub(r"\[\[(.*?)\]\]", r"[\1](\1.md)", t)

    # Find all article names and sanitize them, replacing them with the sanitized version
    article_names = re.findall(r"\[(.*?)\]\(.*?\)", t)
    for article_name in article_names:
        # if "," in article_name:
        #     print("Comma!")
        sanitized_name = sanitize_article_name(article_name)
        t = t.replace(f"[{article_name}]({article_name}.md)", f"[{article_name}]({sanitized_name}.md)")

    # Upper case the link portion of the Markdown link
    t = re.sub(r"\[(.*?)\]\((.*?)\)", lambda m: f"[{m.group(1)}]({custom_title_case(m.group(2))})", t)

    return t


def custom_title_case(s: str) -> str:
    #### WARNING!!!! ####

    # NOTE THAT IF YOU CHANGE THIS FUNCTION, IT MAY BREAK BACKWARDS COMPATIBILITY WITH EXISTING ARTICLES

    # This function title-cased names in the original gamewiki, but we do not want that behavior for file names

    # Skip this function for file names
    # This heuristic tries to detect file names like "file.md" or "foo/bar.md" or "foo/bar/baz". It's not perfect ¯\_(ツ)_/¯
    if "/" in s or re.match(r".*\.[a-zA-Z]+$", s):
        return s

    # Names that don't seem like file names are title-cased in this way I thought looked nice

    put_funny_spaces_back = "%20" in s
    if put_funny_spaces_back:
        s = s.replace("%20", " ")

    s = s.title()
    non_title_words: List[str] = ["a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "from", "by", "of", "in", "with", "as"]
    for word in non_title_words:
        s = s.replace(f" {word.title()} ", f" {word.lower()} ")
    # Make sure the first character is capitalized
    if len(s) > 0:
        s = s[0].upper() + s[1:]

    if put_funny_spaces_back:
        s = s.replace(" ", "%20")

    if s.endswith(".Md"):
        s = s[:-3] + ".md"

    return s
