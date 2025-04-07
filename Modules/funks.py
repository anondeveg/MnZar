import re
import importlib.util
import aiohttp
import scrapy
import tomllib


class Crawler(scrapy.Spider):
    name = "crawler"

def is_package_installed(pkg_name):
    return importlib.util.find_spec(pkg_name) is not None

def url_extractor(s:str) -> list[str]:
    pattern = r'https?://[^\s]+'
    urls = re.findall(pattern, s)
    return urls

async def html_gatherer(url) -> str:
    headers = tomllib.load(open("../settings.toml","rb"))["web"]["headers"]

    async with aiohttp.ClientSession(headers=headers) as session:
        session.headers
        async with session.get(url) as resp:
                resp.content

def dedupe(l:list) -> list:
    return list(set(l))
