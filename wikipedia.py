from mediawiki import MediaWiki
import random
import re

wikipedia = MediaWiki()

# This function written to remove new lines and parenthesis from output.
def clean_parenthesis(dirty):
    cleaned = re.sub(r"\([^)]*\) *", "", dirty)

    return cleaned.replace("\n", "")


def random_fact():
    r_fact = wikipedia.random(pages=1)

    try:
        r_fact = wikipedia.page(r_fact).summary
        r_fact = clean_parenthesis(r_fact)
    except:
        # Sometimes wikipedia.page(r_fact) returns a disambiguation
        # error. Recursion is a lazy work around.
        return random_fact()

    return r_fact


def famous_sarah():
    fs_list = wikipedia.search("Sarah", results=500)
    fs_fact = random.choice(fs_list)

    try:
        fs_fact = wikipedia.page(fs_fact).summary
        fs_fact = clean_parenthesis(fs_fact)

    except:
        return famous_sarah()

    return fs_fact
