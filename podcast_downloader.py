# -*- coding: utf-8 -*-
"""Podcast_downloader

# Download, search & transcribe podcasts automatically

## Analyzing and downloading podcasts.

First, find the RSS feed of the podcast you're interested in.
"""

from bs4 import BeautifulSoup
import requests
import lxml
import os
import re
import shutil
import subprocess
package_name = 'assemblyai'
subprocess.check_call(['pip', 'install', package_name])
import assemblyai as aai

rss_feed = input("Enter the RSS feed of your podcast (e.g., https://feeds.megaphone.fm/hubermanlab):  ")

"""Get the XML content of the rss feed"""

page = requests.get(rss_feed)
soup = BeautifulSoup(page.content, 'xml')

podcast_name = soup.find("title").text
print("Podcast:",podcast_name)
try:
  os.makedirs(podcast_name)
except FileExistsError:
  pass

"""## working with episodes"""

episodes = soup.find_all("item")

"""# Transcript the podcast using Assembli AI api

> Indented block


"""

aai.settings.api_key = os.environ["ASSEBLYAI_API_KEY"]

def transcribe_pod(link):
  transcriber = aai.Transcriber()
  audio_url = (link)

  config = aai.TranscriptionConfig(speaker_labels=True)

  transcript = transcriber.transcribe(audio_url, config)
  print(f"Transcription status: {transcript.status}")
  if in_episodes:
    episode_number = episode.find("itunes:episode").text
    with open(f"{podcast_name}/{episode_number}_{episode_title}.txt",'w') as f:
      final_text = "\n".join([f"{utterance.speaker}: {utterance.text}" for utterance in transcript.utterances])
      f.write(final_text)
  else:
    with open(f"{podcast_name}/{episode_title}.txt",'w') as f:
      final_text = "\n".join([f"{utterance.speaker}: {utterance.text}" for utterance in transcript.utterances])
      f.write(final_text)

#ask the conditions of download
print("What topics are you interested in? I can search for them. \nAfter entering all the keywords, write 'done' and press Enter.")
more_topics = True
keyword_list = []
while more_topics:
  keyword = input("keyword:  ")
  if keyword != "done":
    keyword_list.append(keyword)
  else:
    more_topics = False

regex_key = '|'.join(keyword_list)

# Downloader function

number_of_episodes = int(input("What's the maximum number of results you wnt to see?"))
download_counter = 0
for episode in episodes:
  if download_counter == number_of_episodes:
    break
  episode_description = episode.find("description").text
  episode_title = episode.find("title").text
  episode_download_link = episode.find("enclosure")["url"]
  if re.search(regex_key, episode_description, re.I):
    in_episodes = episode.find("itunes:episode")
    if in_episodes:
      episode_number = episode.find("itunes:episode").text
      print(f"Downloading episdode #{episode_number}_{episode_title}.mp3")
      episode_mp3_file = requests.get(episode_download_link)
      with open(f"{podcast_name}/{episode_number}_{episode_title}.mp3",'wb') as f:
        f.write(episode_mp3_file.content)
    else:
      print(f"Downloading {episode_title}.mp3")
      episode_mp3_file = requests.get(episode_download_link)
      with open(f"{podcast_name}/{episode_title}.mp3",'wb') as f:
        f.write(episode_mp3_file.content)
    download_counter+=1
    transcribing_check = input("Would you like for me to transcribe the file as well? (Y/N)")
    if transcribing_check.lower() == "y":
      try:
        print("Transcription started...")
        transcribe_pod(episode_download_link)
      except:
        continue
    if transcribing_check.lower() == "n":
      continue
if download_counter == 0:
  print("No episode containing the given keywords found. Sorry:(")
else:
  print(download_counter,"episodes are successfully downloaded.")