from writing.article import Article
from writing.code_wiki_manager import CodeWikiManager


def post_process_add_info(wiki: CodeWikiManager, article: Article):
    # Get the file
    try:
        file_type, file_contents = wiki.get_article_type_and_contents(article.title)
        article_path = wiki.get_article_file_path(article.title)
    except Exception as e:
        print(f"{article.title} does not appear to be code, no structured data added.")
        return

    file_len = len(file_contents.split("\n"))
    # TODO Add some more info here like github info
    # TODO Format this better somehow
    structured_data = f"File: [{article.title}]({article_path})\n\nNum lines: {file_len}\n\nGithub history: TODO\n\n"

    updated_contents = article.content_markdown
    if updated_contents.startswith("# ") and "\n" in updated_contents:
        # Insert structured data after the first line
        updated_contents = updated_contents.split("\n", 1)[0] + "\n\n" + structured_data + "\n\n" + updated_contents.split("\n", 1)[1]
    else:
        # Insert structured data at the top
        updated_contents = structured_data + updated_contents

    article.content_markdown = updated_contents
