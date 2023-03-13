from datetime import datetime
from dotenv import load_dotenv
import logging
import os
import openai
import random
import telegram
import time

load_dotenv()

def summary_decorator(func): 
    async def inner(url, user_agent):
        load_dotenv()
        openai.api_key = os.environ['OPENAI_API_KEY']

        print("-----------------------------------------")
        print(f"Browsing {url}")
        print("-----------------------------------------")

        full_pages = await func(url, user_agent)

        if len(full_pages) >= 72500:
            midpoint = len(full_pages) // 2
            full_pages = (full_pages[:midpoint], full_pages[midpoint:])
        else:
            full_pages = (full_pages, )
        print(full_pages)
        segment_size = 2500
        summaries = []
        for full_page in full_pages:
            print(len(full_page))
            # Convert the transcript list object to plaintext so that we can use it with OpenAI
            transcript_segments = []
            cutoff = 0

            # If this line is more than segment_size seconds after the last cutoff, then we need to create a new segment
            while cutoff < len(full_page):
                cutoff = cutoff + segment_size
                if len(full_page) > segment_size:
                    transcript_segments.append(full_page[cutoff - segment_size:cutoff])
                else:
                    transcript_segments = full_page

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

            prompt += "Summarize the whole segments in following format\n\n 1. Key Points :\n 2. Further Studies:"
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
            summaries.append(response["choices"][0]["text"])
        return summaries
    return inner
def agent_rotation():
    with open("user-agents.txt", "r") as file:
        i = random.randint(0, 99)
        user_agent = file.readlines()[i].replace("\n", "")
    print("New user-agent: {}".format(user_agent))
    
    return user_agent
def print_n_log(msg, is_error = False):
    if not(is_error):
        print("{}  {}".format(datetime.strftime(datetime.now(), format="%Y/%m/%d %H:%M:%S"), msg))
        logging.basicConfig(filename='./dual-trading.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO)
        logging.info(msg)
    else:
        print("{}  Error: {}".format(datetime.strftime(datetime.now(), format="%Y/%m/%d %H:%M:%S"), msg))
        logging.basicConfig(filename='./dual-trading.log', filemode='a', format='%(asctime)s - %(name)s - %(message)s', level=logging.ERROR)
        logging.error(msg)
def stopwatch(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Elapsed time: {}".format(end - start))
        return result
    return inner
def parse_markdown_v2(msg):
    reserved_words = ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!')
    for reserved_word in reserved_words:
        msg = str(msg).replace(reserved_word, "\{}".format(reserved_word))
    return msg
async def send_notification(msg):
    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    msg = '__*🔔Message from {}🔔*__\n{}'.format("Dual Trading Bot", parse_markdown_v2(msg))
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='markdownv2')
async def send_message(update_info):
    # Resolve reserved characters
    update_name = parse_markdown_v2(update_info['name'])
    update_title = parse_markdown_v2(update_info['title'])
    update_link = parse_markdown_v2(update_info['link'])

    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    msg = '__*🔔{} has a new update\!🔔*__\n{}\n{}\n'.format(update_name, update_title, update_link)
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='markdownv2')
async def send_buy_sell_message(header, id, price, amount, current_price, margin_active):
    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    msg = '__*💸{}💸*__\nStrat id: {}\nOrder Price: {}\nAmount: {}\nCurrent Price: {}\nMargin Active: {}\n'.format(parse_markdown_v2(header), id, parse_markdown_v2(price), parse_markdown_v2(amount), parse_markdown_v2(current_price), parse_markdown_v2(margin_active))
    await bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='markdownv2')
async def send_error_message(work, msg):
    # Telegram bot configuration
    bot = telegram.Bot(token = os.environ['TELEGRAM_BOT_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    
    msg_2 = "__*🚫An error occurred while working on {}\!\!🚫*__\n\n{}".format(parse_markdown_v2(work), parse_markdown_v2(msg))
    await bot.sendMessage(chat_id=chat_id, text=msg_2, parse_mode='markdownv2')