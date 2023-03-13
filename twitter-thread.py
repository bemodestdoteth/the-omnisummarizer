from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from dotenv import load_dotenv
import math
import openai
import os
import time
import random
import pandas as pd
import twint

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

def agent_rotation():
    with open("user-agents.txt", "r") as file:
        i = random.randint(0, 9999)
        user_agent = file.readlines()[i].replace("\n", "")
    print("New user-agent: {}".format(user_agent))
    
    return user_agent
def twitter_thread_summary(url, selector, user_agent):

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent = user_agent)
        page.goto(url)
        page.wait_for_selector(selector=selector)  # wait for content to load
        full_pages = page.query_selector(selector).inner_text().replace("\n", "")

    print(len(full_pages))

    # Segment size for sub-summarization. Default is 5 minutes. For videos with a lot of people speaking at once, or videos where the speaker(s) speak especially fast, you may want to reduce this.
    segment_size = 2500

    # Convert the transcript list object to plaintext so that we can use it with OpenAI
    transcript_segments = []
    cutoff = 0

    # If this line is more than segment_size seconds after the last cutoff, then we need to create a new segment
    while cutoff < len(full_pages):
        cutoff = cutoff + segment_size
        if len(full_pages) > segment_size:
            transcript_segments.append(full_pages[cutoff - segment_size:cutoff])
        else:
            transcript_segments = full_pages

    # For each segment of the transcript, summarize
    transcript_segment_summaries = []
    for i in range(len(transcript_segments)):
        start = time.time()
        transcript_segment = transcript_segments[i]

        # Use the OpenAI Completion endpoint to summarize the transcript
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=transcript_segment+"\n\nSummarize segment "+str(i)+". Be as descriptive as possible. Less than 500 characters. Write in a full paragraph.",
            temperature=0.3,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        end = time.time()
        print(end - start)
        print(response["choices"][0]["finish_reason"])
        transcript_segment_summaries.append(response["choices"][0]["text"].strip())

    # Combine the summaries of each segment into a single summary
    prompt = "Summaries of {} segments in this post:\n\n".format(len(transcript_segment_summaries))
    for i in range(len(transcript_segment_summaries)):
        prompt += "Segment #"+str(i)+":\n"+transcript_segment_summaries[i]+"\n\n"
    no_paragraphs = math.floor(len(transcript_segments) / 4)

    prompt += "Summarize the whole segments. The summary must be written in following format:\n\n 1. Summary :\n 2. Key insights: \n 3. Further studies in regards to the post: ".format(no_paragraphs)
    print(prompt)
    # Use the OpenAI Completion endpoint to summarize the transcript
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=450,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    summary = response["choices"][0]["text"]
    print(response)
    print(summary)

if __name__ == "__main__":

    c = twint.Config()
    c.Username = "2lambro"
    c.Liimt = 20
    c.Filter_retweets = True
    c.Retweets = False
    c.Count = True
    c.Store_csv=True
    c.Output='test.csv'
    twint.run.Search(c)

    # url = "https://twitter.com/AureliusValue/status/1608512320678035456" # Tesing Url
    # selector = "div[class=\"\"]"
    # user_agent = agent_rotation()
    # twitter_thread_summary(url, selector, user_agent)