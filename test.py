from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import openai
import os
import time

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

video_id = "CfDZHhsby3s"
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Segment size for sub-summarization. Default is 5 minutes. For videos with a lot of people speaking at once, or videos where the speaker(s) speak especially fast, you may want to reduce this.
segment_size = 5 * 60

# Convert the transcript list object to plaintext so that we can use it with OpenAI
transcript_segments = [[]]
transcript_index = 0
last_cutoff = 0

for line in transcript:
    # Add this line's text to the current transcript segment
    transcript_segments[transcript_index].append(line["text"])

    # If this line is more than segment_size seconds after the last cutoff, then we need to create a new segment
    if line["start"] - last_cutoff > segment_size:
        transcript_index += 1
        transcript_segments.append([])
        last_cutoff = line["start"]

for i in range(len(transcript_segments)):
    transcript_segments[i] = " ".join(transcript_segments[i])

# For each segment of the transcript, summarize
transcript_segment_summaries = []
for i in range(len(transcript_segments)):
    transcript_segment = transcript_segments[i]
    print(transcript_segment+"\n\nSummarize segment "+str(i)+" of this video:")

    # Use the OpenAI Completion endpoint to summarize the transcript
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=transcript_segment+"\n\nSummarize segment "+str(i)+" of this video:",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    time.sleep(3)
    transcript_segment_summaries.append(response["choices"][0]["text"].strip())

# Combine the summaries of each segment into a single summary
prompt = "There are "+str(len(transcript_segment_summaries))+" segments in this video. Here are the summaries of each segment:\n\n"
for i in range(len(transcript_segment_summaries)):
    prompt += "Segment #"+str(i)+":\n"+transcript_segment_summaries[i]+"\n\n"
prompt += "Summarize this video in its entirety:"
print(prompt)

# Use the OpenAI Completion endpoint to summarize the transcript
response = openai.Completion.create(
    model="text-curie-001",
    prompt=prompt,
    temperature=0.5,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)
summary = response["choices"][0]["text"]
print(summary)