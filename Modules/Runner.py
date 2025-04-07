import subprocess
import sys
from Modules.funks import url_extractor,is_package_installed    


def run_command(command:str,extract_urls:bool=False,verbose:bool=True) -> str | list[str]:
    splitted_command = command.split(" ")
    try:   
        result = ""        
        with subprocess.Popen(
                splitted_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
            ) as proc:
                if verbose:
                    for line in proc.stdout:
                        result += f"\n{line}"
                        print("\033[32m"+str(line)+"\033[0m")
                    proc.wait()
    except subprocess.CalledProcessError as e:
        print("🔴 Command failed!")
        print(f"🧠 Command: {e.cmd}")
        print(f"📦 Exit code: {e.returncode}")
        print(f"📤 STDOUT:\n{e.stdout}")
            #print(f"📥 STDERR:\n{e.stderr}")
        raise
    
    if extract_urls:
        result = url_extractor(result)
    return result


def install(package):
    if not is_package_installed(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])