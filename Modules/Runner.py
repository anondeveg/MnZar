import subprocess
import sys
from funks import url_extractor


def run_command(command:str,extract_urls:bool=False,verbose:bool=True) -> str | list[str]:
    splitted_command = command.split(" ")
    try:
        
        #result = subprocess.check_call(command)
        result = subprocess.run(
                splitted_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                check=False
            )
    except subprocess.CalledProcessError as e:
        print("🔴 Command failed!")
        print(f"🧠 Command: {e.cmd}")
        print(f"📦 Exit code: {e.returncode}")
        print(f"📤 STDOUT:\n{e.stdout}")
        #print(f"📥 STDERR:\n{e.stderr}")
        raise
    if verbose:
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    result = result.stdout
    if extract_urls:
        result = url_extractor(result)
    return result


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])