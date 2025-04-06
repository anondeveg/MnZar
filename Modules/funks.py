import re

def url_extractor(s:str) -> list[str]:
    pattern = r'https?://[^\s]+'
    urls = re.findall(pattern, s)
    return urls

def dedupe(l:list) -> list:
    return list(set(l))
