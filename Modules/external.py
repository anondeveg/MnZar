from Runner import run_command,install
from funks import dedupe
import sys,os


class ReverseSearch():
    def __init__(self):
        pass
        

        
    @staticmethod
    def username(username:str,tools:list[str]=["sherlock","naminter"],extract_urls:bool=True,verbose:bool=True,timeout:int=10):
          # Windows
        hits = [] 
        pkgs = {"naminter":"naminter",
                "sherlock":"sherlock-project"} # because some tools have different pkg names
        naminter_bin = os.path.join(sys.prefix, "Scripts", "naminter.exe")
        config = {"naminter":f"{naminter_bin} {username}",
                  'sherlock':f"sherlock {username}"} # because each tool might need different configuration (ie options)
        for tool in tools:
            try:
                install(pkgs.get(tool))
            except:
                raise
            try:
                hits.extend(run_command(command=config.get(tool),extract_urls=extract_urls,verbose=True)) # adding tool results to hits list
            except Exception as e:
                raise
        return dedupe(hits)
    

if __name__ == "__main__":
    print(ReverseSearch.username("user",tools=["naminter"]))