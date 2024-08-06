def format_title_for_storage(title):
    if title.lower().startswith('the '):
        title = f"{title[4:]}, The"
    return title

def normalize_title_for_search(title):
    return title.lower().replace('the ', '')