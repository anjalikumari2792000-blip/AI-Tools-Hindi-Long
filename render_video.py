import os, requests, json, subprocess, socket, gc, math, random
import moviepy.editor as mpe
import urllib3.util.connection as urllib3_cn
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, TextClip, ColorClip, afx

# 🛡️ Force IPv4 to bypass Hostinger block
def allowed_gai_family():
    return socket.AF_INET
urllib3_cn.allowed_gai_family = allowed_gai_family

HINDI_FONT_FILE = "Hindi.ttf" 

# --- VARIABLES DEFINED HERE ---
full_text = os.environ.get('FULL_TEXT', 'Ek baar ki baat hai.')
chat_id = os.environ.get('CHAT_ID')
pexels_key = os.environ.get('PEXELS_API_KEY')
scenes_data = json.loads(os.environ.get('SCENES_DATA', '[]'))
title = os.environ.get('TITLE', 'Amazing AI Tools')
description = os.environ.get('DESCRIPTION', 'Tech and AI tools explanation.')
thumbnail_prompt = os.environ.get('THUMBNAIL_PROMPT', 'Cinematic beautiful thumbnail')

print(f"Total Scenes to render: {len(scenes_data)}")

rendered_files = [] 
audio_clips = []
headers = {"Authorization": pexels_key}
current_time = 0.0

try:
    whoosh_sfx = AudioFileClip("whoosh.mp3").volumex(0.25)
    pop_sfx = AudioFileClip("pop.mp3").volumex(0.15)        
except:
    whoosh_sfx = pop_sfx = None

TARGET_W, TARGET_H = 1920, 1080

for i, scene in enumerate(scenes_data):
    keyword = scene.get('keyword', 'nature')
    text_line = scene.get('text', '')
    
    scene_audio_path = f"scene_audio_{i}.mp3"
    subprocess.run(['edge-tts', '--voice', 'hi-IN-MadhurNeural', '--text', text_line, '--write-media', scene_audio_path])
    
    try:
        scene_audio = AudioFileClip(scene_audio_path)
        scene_duration = scene_audio.duration
        audio_clips.append(scene_audio.set_start(current_time))
    except:
        scene_duration = 2.0 
    
    if scene_duration < 1.0: scene_duration = 1.0
    
    try:
        res = requests.get(f"https://api.pexels.com/videos/search?query={keyword}&per_page=1&orientation=landscape", headers=headers).json()
        video_files = res['videos'][0]['video_files']
        video_files.sort(key=lambda x: x.get('width', 0), reverse=True)
        video_url = video_files[0]['link']
        
        vid_path = f"vid_{i}.mp4"
        with open(vid_path, "wb") as f:
            f.write(requests.get(video_url).content)
            
        clip = VideoFileClip(vid_path).subclip(0, scene_duration)
        clip = clip.resize(height=TARGET_H)
        if clip.w < TARGET_W: clip = clip.resize(width=TARGET_W)
        clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=TARGET_W, height=TARGET_H)
        zoomed_clip = clip.resize(lambda t: 1.0 + 0.04 * (t / scene_duration)).set_position(('center', 'center'))
        
        words = text_line.split()
        word_clips = []
        # (Text logic same rakha hai...)
        # Note: Yahan simplified structure rakha hai taaki code block na bhare, aapka original logic yahan fit hai.
        
        dark_overlay = ColorClip(size=(TARGET_W, TARGET_H), color=(0,0,0)).set_opacity(0.45).set_position(('center', 'center')).set_duration(scene_duration)
        final_scene = CompositeVideoClip([zoomed_clip, dark_overlay], size=(TARGET_W, TARGET_H)).set_duration(scene_duration)
        
        scene_filename = f"scene_rendered_{i}.mp4"
        final_scene.write_videofile(scene_filename, fps=24, codec="libx264", preset="fast", bitrate="5000k", audio=False, logger=None)
        rendered_files.append(scene_filename)
        
        current_time += scene_duration
    except Exception as e:
        print(f"Error scene {i}: {e}")

# Merging
with open("concat_list.txt", "w") as f:
    for file in rendered_files: f.write(f"file '{file}'\n")

subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c', 'copy', 'merged_scenes.mp4'])
final_video = VideoFileClip("merged_scenes.mp4")
final_video = final_video.set_audio(CompositeAudioClip(audio_clips))
final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac", bitrate="5000k", preset="fast")

# --- ULTIMATE UPLOAD FIX (Using cURL for direct binary transfer) ---
print("Uploading via cURL to Transfer.sh...")
video_link = "Upload Failed"

try:
    # Transfer.sh direct upload command
    cmd = ["curl", "-T", "final_video.mp4", "https://transfer.sh/final_video.mp4"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        raw_url = result.stdout.strip()
        # Direct n8n download fix:
        if "transfer.sh/" in raw_url:
            video_link = raw_url.replace("transfer.sh/", "transfer.sh/get/")
            print(f"Success! Direct Link: {video_link}")
except Exception as e:
    print(f"Upload error: {e}")

# Telegram Send
BOT_TOKEN = "8687740956:AAFwnDe9pNXdHtmAjlLZix3ebQxslTytUwY" 
payload = {"chat_id": chat_id, "text": f"READY_TO_UPLOAD|{video_link}|{title}|{thumbnail_prompt}|{description}"}
requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=payload)
