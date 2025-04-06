from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
from browser_use.controller.service import Controller
from pydantic import BaseModel
import json
import re
import subprocess
load_dotenv()




class UserName(BaseModel):
    username:str
class Data(BaseModel):
    gathered_data: str


controller = Controller()
@controller.action('Save data', param_model=Data)
def save_data(params: Data):
    try:
        with open('data.json', 'a', encoding='utf-8') as f:
            f.write("\n " + str(params.gathered_data.replace("'",'"')))
    except UnicodeEncodeError as e:
        print(f"Unicode encoding error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")




key = os.getenv("GEMINI_API_KEY")

username = "iqthegoat"



async def username_searcher(username:str):
   


   #sites = search_username(username)

   
   TASK = f"""
    this is the username of the target {username} go to https://whatsmyname.app/ search the username.
    then For each website that is accessible, perform the following steps:

    Visit and Analyze: Navigate to the website and thoroughly examine all available content.

    Verify Relevance: Ensure that the content you are analyzing is actually related to the same individual. Look for matching usernames, consistent writing styles, recurring profile pictures, similar bios, or cross-linked social accounts to confirm the identity across sites.

    Extract Information: If the site is verified to be associated with the user, extract all relevant data, including:

        Full name, usernames, or known aliases

        ** REALLY IMPORTANT, PROFILE PICTURES DIRECT URL **

        Pictures 

        Contact details (e.g., email addresses, phone numbers, locations)

        Biographical info or "About Me" sections

        Social media accounts or external links

        Professional roles, resumes, portfolios, or work history

        Personal interests, hobbies, and affiliations

        Published content (e.g., blog posts, articles, comments, forum activity)

        Media files (profile photos, banners, images, videos)

        Writing style, tone, or personality indicators

        Any other identifying or notable open-source information
        
        if the page dosen't work skip it

        ** !IMPORTANT if you see captcha,cloudflare,hcaptcha ETC Skip that Site **
        compile info from the website about the user and save it using""" + """the save data action like this {website_name:'{output of extract_content as a python dict}' so a dict as a value in a dict PUT AS MUCH DATA AS POSSIBLE

    Cross-reference Across Sites: After visiting all websites, compare the gathered data to identify consistencies, contradictions, or patterns that further confirm the user's identity or reveal more insights."""

   agent = Agent(
        task=TASK,
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite",api_key=key),
        controller=controller,
    )

   await agent.run(max_steps=1000)


def search_username(username=""):
    if not username:
        return []

    # Check if the file {USERNAME}.txt exists
    filename = f"{username}.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            # Load the contents from the file
            file_contents = file.read()
            # Replace Reddit URLs with old Reddit URLs
            pattern = r'https?://[^\s]+'
            urls = re.findall(pattern, file_contents)
            urls = [url.replace('reddit.com', 'old.reddit.com').replace("www.","") if 'reddit.com' in url else url for url in urls]
            return urls

    # Run Sherlock using subprocess to find the username on different platforms
    try:
        result = subprocess.run(
            ['sherlock', username, '--nsfw'],  # Use the --json flag to get results in JSON format
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        # Parse the output from Sherlock (which is in plain text format)
        search_results = result.stdout

        # Find all URLs in the output
        pattern = r'https?://[^\s]+'
        urls = re.findall(pattern, search_results)

        # Replace Reddit URLs with old Reddit counterparts
        urls = [url.replace('reddit.com', 'old.reddit.com').replace("www.","") if 'reddit.com' in url else url for url in urls]

        # Save the results to a file for future use
        with open(filename, 'w') as file:
            file.write("\n".join(urls))

        return urls

    except subprocess.CalledProcessError as e:
        return []



asyncio.run(username_searcher(username=username))