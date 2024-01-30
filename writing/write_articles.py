from pathlib import Path

from config.globals import LLM_MODEL
from strategy.next_article_selection import select_next_article
from utils.gpt import prompt_completion_chat
from writing.article import Article
from writing.code_wiki_manager import CodeWikiManager
from writing.postprocess import post_process_add_info
from writing.wiki_manager import WikiManager


def get_article_text(next_article_name: str, wiki: WikiManager) -> str:
    snippets = wiki.get_snippets_that_mention(next_article_name)
    snippets_text = ""
    for article_name, article_snippets in snippets.items():
        for snippet in article_snippets:
            snippets_text += f"The \"{article_name}\" article says: "
            snippets_text += f"{snippet}\n\n"

    # TODO: Somehow get the most relevant links here
    other_article_titles = wiki.get_existing_links(max_num_links=40, alphabetize=True)

    if isinstance(wiki, CodeWikiManager) and wiki.is_article_code(next_article_name):
        with open("prompts/write_new_article_about_code.txt", 'r') as f:
            prompt = f.read()
        file_type, file_contents = wiki.get_article_type_and_contents(next_article_name)
        prompt = prompt.format(
            topic=next_article_name,
            snippets=snippets_text.strip(),
            other_articles="\n".join([f"* [[{article_title}]]" for article_title in other_article_titles]),
            file_type=file_type,
            code=file_contents,
        )
    else:
        with open("prompts/write_new_article.txt", 'r') as f:
            prompt = f.read()
        prompt = prompt.format(topic=next_article_name, snippets=snippets_text.strip(), other_articles="\n".join([f"* [[{article_title}]]" for article_title in other_article_titles]))

    response = prompt_completion_chat(prompt, max_tokens=2048, model=LLM_MODEL)

    return response


def add_articles_to_wiki(wiki_name: str = "testing", code_path: Path = "", num_new_articles: int = 1):
    wiki_path = Path(f"multiverse/{wiki_name}/wiki/docs")

    for i in range(num_new_articles):
        # Load all articles, regenerating every time
        wiki = CodeWikiManager(wiki_name, wiki_path, code_path=code_path)

        # Select next article
        next_article = select_next_article(wiki)
        print(f"Next article: {next_article}")

        # Get article text
        article_text = get_article_text(next_article, wiki)
        article = Article(next_article, content_wikitext=article_text)

        # Add some structured info to the article
        post_process_add_info(wiki, article)

        # Write article file
        with open(f"{wiki_path}/{next_article}.md", 'w') as f:
            f.write(article.content_markdown)
        print(f"Wrote article {next_article}!")
