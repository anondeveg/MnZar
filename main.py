from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent,BrowserConfig,Browser,BrowserContextConfig
import asyncio
from dotenv import load_dotenv,find_dotenv
import os
from browser_use.controller.service import Controller
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from pydantic import BaseModel
import json
import re
import subprocess
import tomllib
from Modules.external import ReverseSearch


browser_config = BrowserConfig(
    new_context_config=BrowserContextConfig(
        cookies_file="cookies.json"
    )
)
browser = Browser(config=browser_config)

load_dotenv(find_dotenv(),override=True)
key = os.environ.get("GEMINI_API_KEY")

prompts = tomllib.load(open("settings.toml", "rb"))



class Data(BaseModel):
    identifier: str
    gathered_data: str


controller = Controller()



@controller.action("Save data", param_model=Data)
def save_data(params: Data):
    try:
        with open(params.identifier+".json", "a", encoding="utf-8") as f:
            f.write("\n " + str(params.gathered_data.replace("'", '"')))
    except UnicodeEncodeError as e:
        print(f"Unicode encoding error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def username_searcher(username: str):
    urls = []
    for url in urls:
        print(url)
    Task = prompts["prompts"]["general"] + str(prompts["prompts"]["user_search"]) + str(urls)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=key)
    agent = Agent(task=Task,llm=llm,controller=controller,browser=browser)
    await agent.run(max_steps=2000)
asyncio.run(username_searcher(username=username))
