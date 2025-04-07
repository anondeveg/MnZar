from Modules.Runner import run_command,install
from Modules.funks import dedupe
import sys,os
from urllib.parse import urlparse

class ReverseSearch():
    def __init__(self):
        pass
        

        
    @staticmethod
    def username(usernames:list[str],tools:list[str]=["sherlock","naminter"],extract_urls:bool=True,verbose:bool=True,timeout:int=30,write_to_file:bool=True):
          # Windows
        hits = [] 
        pkgs = {"naminter":"naminter",
                "sherlock":"sherlock-project"} # because some tools have different pkg names
      
        for username in usernames:
            config = {"naminter":f"naminter {username}",'sherlock':f"sherlock {username}"} # because each tool might need different configuration (ie options)
        
            for tool in tools:
                try:
                    install(pkgs.get(tool))
                except:
                    raise
                try:
                    hits.extend(run_command(command=config.get(tool),extract_urls=extract_urls,verbose=True)) # adding tool results to hits list
                except Exception as e:
                    raise
        data = [url.replace('reddit.com', 'old.reddit.com').replace("www.","") for url in dedupe(hits)] # switch to old reddit to bypass age restrictions

        if write_to_file:
            with open(username,"w") as f:
                f.write("\n".join(data))
    
    def reddit_scraper(url:str) -> dict:
        ...

if __name__ == "__main__":
    print(ReverseSearch.username("elonmusk",tools=["naminter"]))