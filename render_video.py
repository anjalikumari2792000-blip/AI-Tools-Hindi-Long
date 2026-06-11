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

subprocess.run(['edge-tts', '--voice', 'hi-IN-MadhurNeural', '--text', full_text, '--write-media', 'voiceover.mp3'])
voiceover = AudioFileClip("voiceover.mp3")

total_chars = sum(len(s['text']) for s in scenes_data)
rendered_files = [] 
audio_clips = [voiceover]
headers = {"Authorization": pexels_key}
current_time = 0.0

try:
    whoosh_sfx = AudioFileClip("whoosh.mp3").volumex(0.25)
    pop_sfx = AudioFileClip("pop.mp3").volumex(0.15)        
except:
    whoosh_sfx = pop_sfx = None

viral_colors = ['#00E5FF', '#FFFFFF', '#39FF14', '#FFEA00']
TARGET_W, TARGET_H = 1920, 1080

for i, scene in enumerate(scenes_data):
    keyword = scene.get('keyword', 'nature')
    text_line = scene.get('text', '')
    scene_duration = voiceover.duration * (len(text_line) / max(total_chars, 1))
    if scene_duration < 1.0: scene_duration = 1.0
    
    try:
        res = requests.get(f"https://api.pexels.com/videos/search?query={keyword}&per_page=1&orientation=landscape", headers=headers).json()
        video_url = res['videos'][0]['video_files'][0]['link']
        
        vid_path = f"vid_{i}.mp4"
        with open(vid_path, "wb") as f:
            f.write(requests.get(video_url).content)
            
        clip = VideoFileClip(vid_path).subclip(0, scene_duration)
        clip = clip.resize(height=TARGET_H)
        if clip.w < TARGET_W:
            clip = clip.resize(width=TARGET_W)
        clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=TARGET_W, height=TARGET_H)
        
        zoomed_clip = clip.resize(lambda t: 1.0 + 0.04 * (t / scene_duration)).set_position(('center', 'center'))
        
        # 🔥 ADVANCED KINETIC TEXT ENGINE (Perfect Sync & Animations) 🔥
        def advanced_punch_anim(t):
            if t < 0.06: return 1.6 - 10.0 * t  
            elif t < 0.15: return 1.0 + 1.2 * (t - 0.06) 
            return 1.0

        def get_kinetic_pos(base_y, is_shaking, word_idx):
            def pos(t):
                idle_y = 7 * math.sin(t * 8 + word_idx)
                idle_x = 4 * math.cos(t * 6 + word_idx)
                if is_shaking and t > 0.06:
                    return (TARGET_W/2 + 5 * math.sin(t * 75) + idle_x, base_y + 5 * math.cos(t * 85) + idle_y)
                return (TARGET_W/2 + idle_x, base_y + idle_y)
            return pos

        words = text_line.split()
        word_clips = []

        if words:
            # 🚀 SMART SUBTITLE SYNCHRONIZATION 🚀
            word_weights = []
            for w in words:
                wt = len(w)
                if w.endswith(','): wt += 4 
                elif w[-1] in '.?!।': wt += 8 
                word_weights.append(wt)
            
            total_weight = sum(word_weights) if sum(word_weights) > 0 else 1
            current_time_pos = 0.0

            for w_i, word in enumerate(words):
                word_lower = word.lower()
                is_danger = any(kw in word_lower for kw in ['secret', 'trick', 'hidden', 'scam', 'khatarnaak', 'danger', 'alert', 'mat', 'tool', 'ai'])
                is_highlight = not is_danger and len(word) > 4
                
                duration_per_word = (word_weights[w_i] / total_weight) * scene_duration

                current_color = '#FF003C' if is_danger else ('#000000' if is_highlight else '#FFFFFF')
                bg_color = 'transparent' if is_danger else (random.choice(['#FFD400', '#39FF14', '#00FFFF']) if is_highlight else 'transparent')
                base_size = 155 if is_danger else (140 if is_highlight else 95)

                try:
                    text_y_pos = TARGET_H * 0.75 
                    position_filter = get_kinetic_pos(text_y_pos, is_danger, w_i)

                    if bg_color == 'transparent':
                        shadow_txt = TextClip(word, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(1500, None)).resize(advanced_punch_anim).set_position(get_kinetic_pos(text_y_pos + 15, is_danger, w_i)).set_duration(duration_per_word).set_start(current_time_pos)
                        bg_txt = TextClip(word, fontsize=base_size, color='black', font=HINDI_FONT_FILE, stroke_color='black', stroke_width=16, method='caption', size=(1500, None)).resize(advanced_punch_anim).set_position(position_filter).set_duration(duration_per_word).set_start(current_time_pos)
                        inner_border_txt = TextClip(word, fontsize=base_size, color='black', font=HINDI_FONT_FILE, stroke_color='white', stroke_width=4, method='caption', size=(1500, None)).resize(advanced_punch_anim).set_position(position_filter).set_duration(duration_per_word).set_start(current_time_pos)
                        main_txt = TextClip(word, fontsize=base_size, color=current_color, font=HINDI_FONT_FILE, method='caption', size=(1500, None)).resize(advanced_punch_anim).set_position(position_filter).set_duration(duration_per_word).set_start(current_time_pos)
                        word_clips.extend([shadow_txt, bg_txt, inner_border_txt, main_txt])
                    else:
                        main_txt = TextClip(word, fontsize=base_size, color=current_color, bg_color=bg_color, font=HINDI_FONT_FILE, method='caption', size=(None, None)).resize(advanced_punch_anim).set_position(position_filter).set_duration(duration_per_word).set_start(current_time_pos)
                        word_clips.append(main_txt)
                except: pass
                
                current_time_pos += duration_per_word

        dark_overlay = ColorClip(size=(TARGET_W, TARGET_H), color=(0,0,0)).set_opacity(0.45).set_position(('center', 'center')).set_duration(scene_duration)

        final_scene = CompositeVideoClip([zoomed_clip, dark_overlay] + word_clips, size=(TARGET_W, TARGET_H)).set_duration(scene_duration)
        
        # --- MEMORY FIX START ---
        scene_filename = f"scene_rendered_{i}.mp4"
        final_scene.write_videofile(scene_filename, fps=24, codec="libx264", preset="ultrafast", audio=False, logger=None)
        rendered_files.append(scene_filename)
        
        final_scene.close()
        clip.close()
        del final_scene, clip, zoomed_clip, word_clips, dark_overlay
        gc.collect()
        # --- MEMORY FIX END ---
        
        if whoosh_sfx: audio_clips.append(whoosh_sfx.set_start(current_time))
        if pop_sfx: audio_clips.append(pop_sfx.set_start(current_time + 0.1))
                
        current_time += scene_duration
        print(f"Scene {i+1} Ready: {keyword}")
    except Exception as e:
        print(f"Error on scene {i}: {e}")

# --- DISK CONCATENATION FIX START ---
print("Merging scenes without RAM...")
with open("concat_list.txt", "w") as f:
    for file in rendered_files:
        f.write(f"file '{file}'\n")

subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c', 'copy', 'merged_scenes.mp4'])
final_video = VideoFileClip("merged_scenes.mp4")
# --- DISK CONCATENATION FIX END ---

final_duration = final_video.duration
progress_bar = ColorClip(size=(TARGET_W, 15), color=(255, 0, 0))
progress_bar = progress_bar.set_position(lambda t: (-TARGET_W + int(TARGET_W * (t / max(final_duration, 1))), 'bottom'))
progress_bar = progress_bar.set_duration(final_duration)

# 🔥 AIToolKitHub Watermark Implementation 🔥
watermark = TextClip("AIToolKitHub", fontsize=55, color='white', font=HINDI_FONT_FILE, stroke_color='black', stroke_width=2)
# Opacity 0.5 (semi-transparent) and positioned perfectly in the bottom-right corner
watermark = watermark.set_opacity(0.5).set_position((0.78, 0.88), relative=True).set_duration(final_duration)

final_video = CompositeVideoClip([final_video, progress_bar, watermark])

try:
    bgm = AudioFileClip("bgm.mp3").volumex(0.10)
    if bgm.duration < final_video.duration: bgm = afx.audio_loop(bgm, duration=final_video.duration)
    else: bgm = bgm.subclip(0, final_video.duration)
    audio_clips.append(bgm)
except: pass

final_audio = CompositeAudioClip(audio_clips)
final_video = final_video.set_audio(final_audio)

print("Rendering Final COMPRESSED LONG Video...")
final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac", threads=2, bitrate="1000k", preset="ultrafast")

print("Starting 5-Layer Indestructible Upload System...")
video_link = "Upload Failed"

if not video_link.startswith("http"):
    try:
        print("Trying 0x0.st API...")
        res = requests.post("https://0x0.st", files={'file': open('final_video.mp4', 'rb')}, timeout=600)
        if res.text.startswith("http"): video_link = res.text.strip()
    except Exception as e: print(f"0x0.st failed: {e}")

if not video_link.startswith("http"):
    try:
        print("Trying Uguu.se API...")
        res = requests.post("https://uguu.se/upload.php", files={'files[]': open('final_video.mp4', 'rb')}, timeout=600)
        if res.status_code == 200: video_link = res.json()['files'][0]['url']
    except Exception as e: print(f"Uguu.se failed: {e}")

if not video_link.startswith("http"):
    try:
        print("Trying Tmpfiles API...")
        res = requests.post("https://tmpfiles.org/api/v1/upload", files={'file': open('final_video.mp4', 'rb')}, timeout=600)
        if res.status_code == 200: video_link = res.json()['data']['url'].replace('tmpfiles.org/', 'tmpfiles.org/dl/')
    except Exception as e: print(f"Tmpfiles failed: {e}")

if not video_link.startswith("http"):
    try:
        print("Trying Catbox API...")
        res = requests.post("https://catbox.moe/user/api.php", data={'reqtype': 'fileupload'}, files={'fileToUpload': open('final_video.mp4', 'rb')}, timeout=600)
        if res.text.startswith("http"): video_link = res.text.strip()
    except Exception as e: print(f"Catbox failed: {e}")

print(f"🔥 FINAL YOUTUBE LINK: {video_link} 🔥")

# 🌟 TELEGRAM BRIDGE - WITH PIPE (|) SEPARATOR FOR SAFETY
BOT_TOKEN = "8687740956:AAFwnDe9pNXdHtmAjlLZix3ebQxslTytUwY" 

# Pipe separator ensures multi-line descriptions don't break the n8n logic
message_text = f"READY_TO_UPLOAD|{video_link}|{title}|{thumbnail_prompt}|{description}"

try:
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message_text}
    response = requests.post(telegram_url, json=payload)
    print(f"✅ Webhook bypassed! Sent video details directly to Telegram! Status: {response.status_code}")
except Exception as e:
    print(f"❌ Failed to send Telegram alert: {e}")
