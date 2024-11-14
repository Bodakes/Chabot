import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.urls import get_resolver
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import service
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import random
import traceback
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from selenium.webdriver.common.keys import Keys
import urllib3
urls = []
# The provided list of texts
texts=service
STOPWORDS = set([
    'a', 'an', 'the', 'and', 'or', 'of', 'to', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'that', 'is', 
    'was', 'were', 'be', 'has', 'have', 'had', 'not', 'are', 'will', 'can', 'but', 'nashik', '?', 'about', 'help', 
    'me', 'you', 'your', 'please', 'tell', 'show', 'give', 'find', 'how', 'do', 'does', 'it', 'this', 'need', 'want', 
    'know', 'could', 'would', 'which', 'what', 'who', 'when', 'where', 'why', 'can', 'may', 'get', 'more', 'provide', 
    'looking', 'like', 'inform', 'details', 'information', 'required'
])

import io, os
from django.conf import settings
import speech_recognition as sr
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders
import tempfile
from django.conf import settings 
import moviepy.editor as mp
import logging
import certifi


UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploaded_audios')

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@csrf_exempt
def voiceconverter(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            # Save the uploaded video/audio file temporarily
            media_file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

            try:
                with open(media_file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
            except Exception as e:
                print(f"Error saving file: {e}")
                return None  # Return None on error

            # Prepare to extract audio from the file
            audio_file_path = os.path.splitext(media_file_path)[0] + '.wav'

            try:
                # Check if the uploaded file is an audio or video file
                if media_file_path.lower().endswith(('.mp4', '.avi', '.mov')):  # Video files
                    with mp.VideoFileClip(media_file_path) as media:
                        media.audio.write_audiofile(audio_file_path)
                elif media_file_path.lower().endswith(('.mp3', '.wav')):  # Audio files
                    # If it's an audio file, just copy it to the new path
                    os.rename(media_file_path, audio_file_path)
                else:
                    print("Unsupported file type")
                    return None  # Return None on unsupported file type
            except Exception as e:
                print(f"Error extracting audio: {e}")
                return None  # Return None on error

            recognizer = sr.Recognizer()
            try:
                # Use the audio file for speech recognition
                with sr.AudioFile(audio_file_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None  # Return None on error
            except sr.RequestError as e:
                print(f'Service unavailable; {e}')
                return None  # Return None on error
            except Exception as e:
                print(f"Error recognizing speech: {e}")
                return None  # Return None on error
            finally:
                # Clean up temporary files
                try:
                    if os.path.exists(media_file_path):
                        os.remove(media_file_path)
                    if os.path.exists(audio_file_path):
                        os.remove(audio_file_path)
                except Exception as e:
                    print(f"Error deleting temporary files: {e}")

    return None  # Return None if the request method is not POST
def translate_to_marathi(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='mr')
    return translated.text
def preprocess_input(query):
    query = query.lower()
    # Remove "Nashik" and stopwords
    query = re.sub(r'\bnashik\b', '', query)
    words = re.findall(r'\b\w+\b', query)
    filtered_words = [word for word in words if word not in STOPWORDS]
    return set(filtered_words)

def extract_keywords(text):
    # Tokenize the text and filter out stopwords
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word not in STOPWORDS]
    return set(filtered_words)

def find_matching_texts(user_query, texts, min_keywords_match=2):
    # Preprocess user input to remove unwanted words and stopwords
    query_keywords = preprocess_input(user_query)
    
    matching_texts = []
    for item in texts:
        text = item.get('text', '')
        text_keywords = extract_keywords(text)
        # Count the number of query keywords present in the text
        matched_keywords_count = sum(1 for keyword in query_keywords if keyword in text_keywords)
        
        # Check if the number of matched keywords meets the threshold
        if matched_keywords_count >= min_keywords_match:
            matching_texts.append(item)
    
    return matching_texts




def get_video_links():
    channel_url = 'https://www.youtube.com/@mynmc/videos'
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get(channel_url)

    # Scroll down to load more videos
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)  # Wait for more videos to load
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Save the full page source
    page_source = driver.page_source
    # with open('page_source.html', 'w', encoding='utf-8') as file:
    #     file.write(page_source)
    
    driver.quit()
    print("Page source saved successfully")
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extract video titles and links
    video_info = []
    for video in soup.find_all('a', id='video-title-link'):
        title = video.get('title', 'No title')
        video_id = re.search(r'/watch\?v=([a-zA-Z0-9_-]+)', video.get('href', ''))
        video_url = f"https://www.youtube.com/watch?v={video_id.group(1)}" if video_id else "No video URL"
        video_info.append({
            'title': title,
            'link': video_url
        })

    # Save the video information to a JSON file
    with open('/home/bodakes/Chatbot/Chabot/video_info.json', 'w', encoding='utf-8') as file:
        json.dump(video_info, file, ensure_ascii=False, indent=4)
    
    return video_info

    


def search_videos(videoss, search_term,marathi_text):
    try:
        matching_videos = [video for video in videoss if search_term.lower() in video['title'].lower() or marathi_text.strip() in video['title'].lower().strip()]
    except:
        matching_videos = [video for video in videoss if search_term.lower() in video['title'].lower() ]

    return matching_videos




        
@csrf_exempt
def upload_data(request):
    try:

        if request.method == 'POST':
            input_txt = request.POST.get('searchInput')
            print("input_txt",input_txt)
            if input_txt=="re:raise complaint":
                return JsonResponse({'message': 'Data processed successfully!','complaint':True, 'result': [],'desc':'','contact':[],'youtube_data':[]})
            try:
                input_data=voiceconverter(request)
                if (input_data):
                    input_txt=input_data
                
            except:
                pass
            reply=False
            with open('/home/bodakes/Chatbot/Chabot/video_info.json', 'r', encoding='utf-8') as file:
                video_info = json.load(file)
            if input_txt.startswith("Re:") or input_txt.startswith("re:"):
                input_txt = input_txt[3:].strip()
                reply=True
            data=get_all_urls() if urls==[] else urls
            marathi_text = translate_to_marathi(input_txt)
            # print("marathi_text = translate_to_marathi(english_text)",marathi_text)
            yt=search_videos(video_info,input_txt,marathi_text)
            url=find_first_url_for_text(input_txt,marathi_text)
            print("url",url,reply)
            if url or  reply:
                page_heading,strong_text,links_info=get_page_details(url)
                random_number = random.randint(1, 9)
                yt=search_videos(video_info,page_heading,marathi_text)
                # Define the contact information with the random number inserted
                contact = f'''<div style="
                                font-size: 14px;
                                color: #333;
                                margin-top: 20px;
                                padding-top: 10px;
                                border-top: 1px solid #dee2e6;
                            ">
                                <p style="
                                    margin: 0;
                                    font-weight: 500;
                                ">Contact Information:</p>
                                <p style="
                                    margin: 0;
                                ">नाशिक महानगर पालिका<br>
                                राजीव गांधी भवन,<br>
                                शरणपूर रोड,<br>
                                नाशिक<br>
                                टेलिफोन (पीबीएक्स) : 0253 - 257563{random_number}</p>
                            </div>'''
                fb_links='https://www.facebook.com/mynashikmc'
                youtube_data=""
                if yt:
                    youtube=f'''<ul style="
                                                    list-style-type: decimal;
                                                    padding: 0;
                                                   margin-left: 25px;;
                                                ">'''
                    for data in yt:
                        title = data.get('title', 'No title')
                        link = data.get('link', 'No link')
                        
                        youtube+=f'''  <li>                      <a href="{link}" style="
                                    color: #007bff;
                                    text-decoration: none;
                                    font-size: 14px;
                                " target="_blank">{title}</a></li>  '''
                                                
                    youtube+=f''' </ul>''' 
                        
                    youtube_data = f'''
                                <div style="
                                    font-size: 14px;
                                    color: #333;
                                    margin-top: 20px;
                                    padding-top: 10px;
                                    border-top: 1px solid #dee2e6;
                                    padding: 10px;
                                    background-color: #f9f9f9;
                                    border-radius: 5px;
                                ">
                                    <p style="
                                        margin: 0;
                                        font-weight: 500;
                                        font-size: 16px;
                                        color: #555;
                                    ">Social Media Suggetions:</p>
                                    
                                    <div style="
                                        display: flex;
                                        flex-direction: column;
                                        margin-top: 10px;
                                    ">
                                        <!-- YouTube Links -->
                                        <div style="
                                            margin-bottom: 15px;
                                        ">
                                            <p style="
                                                margin: 0;
                                                font-weight: 500;
                                                font-size: 14px;
                                               
                                            ">YouTube:</p>
                                            {youtube}
                                        </div>
                                        
                                        <!-- Facebook Links -->
                                        <div>
                                            <p style="
                                                margin: 0;
                                                font-weight: 500;
                                                font-size: 14px;
                                               
                                            ">Facebook:</p>
                                            <ul style="
                                                list-style-type: decimal;
                                                padding: 0;
                                               margin-left: 25px;;
                                            ">
                                             <a href={fb_links} style="
                                    color: #007bff;
                                    text-decoration: none;
                                    font-size: 14px;
                                " target="_blank">NMC News</a>
                                                </ul>
                                                
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                '''
                return JsonResponse({'message': 'Data processed successfully!', 'result': links_info,'desc':"<B>"+str(page_heading)+"</B>"+"<br>"+"<small>"+str(strong_text)+"</small>",'contact':contact,'youtube_data':youtube_data})
            else:
                min_keywords_match= len(input_txt.split(" "))
                matching_dict = find_matching_texts(input_txt, data,min_keywords_match = min_keywords_match)

                random_number = random.randint(1, 9)

                # Define the contact information with the random number inserted
                contact = f'''<div style="
                                font-size: 14px;
                                color: #333;
                                margin-top: 20px;
                                padding-top: 10px;
                                border-top: 1px solid #dee2e6;
                            ">
                                <p style="
                                    margin: 0;
                                    font-weight: 500;
                                ">Contact Information:</p>
                                <p style="
                                    margin: 0;
                                ">नाशिक महानगर पालिका<br>
                                राजीव गांधी भवन,<br>
                                शरणपूर रोड,<br>
                                नाशिक<br>
                                टेलिफोन (पीबीएक्स) : 0253 - 257563{random_number}</p>
                            </div>'''
                fb_links='https://www.facebook.com/mynashikmc'
                youtube_data=""
                if yt:
                    
                    youtube=f'''<ul style="
                                                    list-style-type: decimal;
                                                    padding: 0;
                                                   margin-left: 25px;;
                                                ">'''
                    for data in yt:
                        title = data.get('title', 'No title')
                        link = data.get('link', 'No link')
                        
                        youtube+=f'''  <li>                      <a href="{link}" style="
                                    color: #007bff;
                                    text-decoration: none;
                                    font-size: 14px;
                                " target="_blank">{title}</a></li>  '''
                                                
                    youtube+=f''' </ul>'''   
                
                    youtube_data = f'''
                                <div style="
                                    font-size: 14px;
                                    color: #333;
                                    margin-top: 20px;
                                    padding-top: 10px;
                                    border-top: 1px solid #dee2e6;
                                    padding: 10px;
                                    background-color: #f9f9f9;
                                    border-radius: 5px;
                                ">
                                    <p style="
                                        margin: 0;
                                        font-weight: 500;
                                        font-size: 16px;
                                        color: #555;
                                    ">Social Media Suggetions:</p>
                                    
                                    <div style="
                                        display: flex;
                                        flex-direction: column;
                                        margin-top: 10px;
                                    ">
                                        <!-- YouTube Links -->
                                        <div style="
                                            margin-bottom: 15px;
                                        ">
                                            <p style="
                                                margin: 0;
                                                font-weight: 500;
                                                font-size: 14px;
                                               
                                            ">YouTube:</p>
                                            {youtube}
                                        </div>
                                        
                                        <!-- Facebook Links -->
                                        <div>
                                            <p style="
                                                margin: 0;
                                                font-weight: 500;
                                                font-size: 14px;
                                               
                                            ">Facebook:</p>
                                            <ul style="
                                                list-style-type: decimal;
                                                padding: 0;
                                               margin-left: 25px;;
                                            ">
                                               <a href={fb_links} style="
                                    color: #007bff;
                                    text-decoration: none;
                                    font-size: 14px;
                                " target="_blank">NMC News</a>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                '''
                return JsonResponse({'message': 'Data processed successfully!', 'result': matching_dict,'desc':'','contact':contact,'youtube_data':youtube_data})
        return JsonResponse({'error': 'Invalid request' ,'result': [],'desc':''}, status=400)
    except:
        print(traceback.print_exc())
        return JsonResponse({'error': 'Invalid request' ,'result': [],'desc':'Please Visit Service'}, status=400)


def find_first_url_for_text(search_text, marathi):
    # Load URL data from JSON file
    urls = get_all_urls()

    # Search for the URL based on the provided text or Marathi text
    for entry in urls:
        if (search_text.lower() == entry['text'].lower() or
            marathi.strip() == entry['text'].strip() ):
            return entry['url']

    return None


URL_JSON_FILE = '/home/bodakes/Chatbot/Chabot/urls.json'

def get_all_urls():
    # Check if the JSON file already exists and read from it
    if os.path.exists(URL_JSON_FILE):
        with open(URL_JSON_FILE, 'r', encoding='utf-8') as file:
            urls = json.load(file)
        return urls

    # Fetch the data from the website if the JSON file does not exist
    urls = []
    url = 'https://nmc.gov.in/home/atozindex'
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    soup = soup.find(class_='list')

    for a in soup.find_all('a', href=True):
        link_text = a.text.strip()
        link_url = a.get('href')
        if not link_text:
            continue
        if link_url:
            # Ensure complete URL
            if not link_url.startswith('http'):
                link_url = 'https://nmc.gov.in' + link_url
            urls.append({'text': link_text, 'url': link_url})

    # Save the fetched URLs to JSON
    with open(URL_JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(urls, file, ensure_ascii=False, indent=4)

    return urls


def get_page_details(url):
    urls=[]
    url = url
    response = requests.get(url,verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    
    # Find the div with class 'right-pannel'
    right_pannel_div = soup.find('div', class_='right-pannel')

    # Extract the page heading
    try:
        page_heading = right_pannel_div.find( class_='page_heading').text.strip()
    except:
        page_heading



    # Extract links and URLs
    for a_tag in right_pannel_div.find_all('a'):
        link_text = a_tag.text.strip()
        link_url = a_tag['href'].strip()
        urls.append({'text': link_text, 'url': link_url})

    # Extract the strong text
    try:
        strong_text = right_pannel_div.find('strong').text.strip()
    except:
        strong_text=None
    return page_heading,strong_text,urls
def home(request):
    
    urls = get_all_urls()
    return render(request,"home.html",{"urls":urls})


def chatbot(request):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    return render(request,'chatbot.html')

# list
def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the first link from search results
    first_link = soup.find('a')['href']
    
    # Ensure the link is complete (including scheme and domain)
    full_link = urljoin("https://www.google.com", first_link)
    # Fetch the content from the full link
    page_response = requests.get(full_link, headers=headers)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    
    # Extract headers and descriptions
    headers = [header.text for header in page_soup.find_all(['h1', 'h2', 'h3'])]
    descriptions = [p.text for p in page_soup.find_all('p')]
    
    return headers, descriptions

def google_chatbot(user_input):
    search_query = f"Nashik Municipal Corporation + {user_input}"
    
    # Perform Google search
    search_url = f"https://www.google.com/search?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(search_url, headers=headers)
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
   

    target_div = soup.find('div', class_='WaaZC')


    if not target_div:
        target_div = soup.find('div', class_='g wF4fFd JnwWd g-blk')
    
    
    
    # RJPOee EIJn2
    
    # Extract <span> elements within this div
    if target_div:
        span_elements = target_div.find('span')
        
        # Extract text from each <span> element
        span_texts = [span.get_text(strip=True) for span in span_elements][0]
    else:
        span_texts = []
    return  span_texts
  



# task_thread = threading.Thread(target=get_video_links)
# task_thread.start()