import os, requests, json, subprocess, socket, gc, math, random
import moviepy.editor as mpe
import urllib3.util.connection as urllib3_cn
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, TextClip, ColorClip, afx

# 🛡️ Force IPv4 to bypass Hostinger block
def allowed_gai_family():
    return socket.AF_INET
urllib3_cn.allowed_gai_family = allowed_gai_family

# 🔥 PREMIUM FONT: Ultra-Bold Cinematic Font (Montserrat-Black.ttf zaroor upload rakhein)
HINDI_FONT_FILE = "Montserrat-Black.ttf" 

# 🌟 SMART REVERSE-PHONETIC CLEAN-UP ENGINE
def clean_phonetic_text(text):
    replacements = {
        "sey": "se", "key": "ke", "ney": "ne", "dey": "de", "kaisey": "kaise", "aisey": "aise",
        "hotey": "hote", "kartey": "karte", "apney": "apne", "samajhtey": "samajhte", 
        "pehley": "pehle", "karkey": "karke", "chaley": "chale", "puraaney": "purane", 
        "bachchey": "bachche", "kiyaa": "kiya", "diyaa": "diya", "liyaa": "liya",
        "sikhaatee": "sikhati", "dikhaatey": "dikhate", "chaahatey": "chahte", 
        "banaatey": "banate", "kamaal": "kamal", "aasaan": "asan", "bund": "band", 
        "mut": "mat", "jub": "jab", "pul": "pal", "humaarey": "hamare", "humein": "hamein", 
        "abhee": "abhi", "huaa": "hua", "jamey": "jame", "sunney": "sunne", "sbb": "sab",
        "bachti": "bachati", "bachta": "bachata", "tarikay": "tarika"
    }
    words = text.split()
    cleaned_words = []
    for w in words:
        p_left = ""
        p_right = ""
        while w and w[0] in ',.?!।()[]{}*"\'':
            p_left += w[0]
            w = w[1:]
        while w and w[-1] in ',.?!।()[]{}*"\'':
            p_right = w[-1] + p_right
            w = w[:-1]
        
        w_lower = w.lower()
        if w_lower in replacements:
            rep = replacements[w_lower]
            if w.isupper(): w = rep.upper()
            elif w and w[0].isupper(): w = rep.capitalize()
            else: w = rep
        cleaned_words.append(p_left + w + p_right)
    return " ".join(cleaned_words)

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

# 🔥 VIRAL NEON HIGHLIGHT PALETTE
viral_colors = ['#00E5FF', '#39FF14', '#FFEA00']
TARGET_W, TARGET_H = 1920, 1080

for i, scene in enumerate(scenes_data):
    keyword = scene.get('keyword', 'nature')
    text_line = scene.get('text', '')
    
    # 🚀 PERFECT AUDIO SYNC: TTS receives original phonetic string for perfect accent
    scene_audio_path = f"scene_audio_{i}.mp3"
    subprocess.run(['edge-tts', '--voice', 'hi-IN-MadhurNeural', '--text', text_line, '--write-media', scene_audio_path])
    
    try:
        scene_audio = AudioFileClip(scene_audio_path)
        scene_duration = scene_audio.duration
        audio_clips.append(scene_audio.set_start(current_time))
    except Exception as e:
        print(f"Audio error for scene {i}: {e}")
        scene_duration = 2.0 
        
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
        
        # TRUE DAMPED SPRING PHYSICS ANIMATION
        def anim_fluid_spring(t):
            if t < 0.45:
                return 1.0 + 0.55 * math.exp(-11 * t) * math.cos(22 * t)
            return 1.0

        def anim_smooth_swell(t):
            if t < 0.18: return 0.75 + 1.4 * t
            return 1.0

        def anim_snap_focus(t):
            if t < 0.05: return 1.35
            return 1.0

        # SLIDE ENTRANCE + KINETIC DRIFT
        def get_kinetic_pos(base_y, is_shaking, word_idx):
            def pos(t):
                slide_y = 70 * math.exp(-24 * t) if t < 0.22 else 0
                idle_y = 8 * math.sin(t * 10 + word_idx) 
                idle_x = 4 * math.cos(t * 8 + word_idx)
                if is_shaking and t > 0.06:
                    return (TARGET_W/2 + 7 * math.sin(t * 85) + idle_x, base_y + slide_y + 7 * math.cos(t * 95) + idle_y)
                return (TARGET_W/2 + idle_x, base_y + slide_y + idle_y)
            return pos

        def get_shadow_pos_matrix(base_y, is_shaking, word_idx, ox, oy):
            def pos(t):
                base_pos = get_kinetic_pos(base_y, is_shaking, word_idx)(t)
                return (base_pos[0] + ox, base_pos[1] + oy) 
            return pos

        # 🚀 CLEAN TEXT FOR SCREEN DISPLAY: Converts phonetic engine leaks to standard text
        clean_text_line = clean_phonetic_text(text_line)
        raw_words = clean_text_line.split()
        
        phrases_data_list = []
        current_chunk = []
        current_len = 0
        for w in raw_words:
            current_chunk.append(w)
            current_len += len(w)
            if current_len >= 13 or w[-1] in ',.?!।':
                phrases_data_list.append(current_chunk)
                current_chunk = []
                current_len = 0
        if current_chunk:
            if phrases_data_list: phrases_data_list[-1].extend(current_chunk)
            else: phrases_data_list.append(current_chunk)

        word_clips = []

        if phrases_data_list:
            phrase_weights = [sum(len(w) for w in p) for p in phrases_data_list]
            total_phrase_weight = sum(phrase_weights) if sum(phrase_weights) > 0 else 1
            current_phrase_start = 0.0

            for p_i, phrase_words in enumerate(phrases_data_list):
                phrase_duration = (phrase_weights[p_i] / total_phrase_weight) * scene_duration
                
                mid_point = len(phrase_words) // 2
                if len(phrase_words) > 3:
                    line_1 = " ".join(phrase_words[:mid_point]).upper()
                    line_2 = " ".join(phrase_words[mid_point:]).upper()
                    wrapped_phrase_str = f"{line_1}\n{line_2}"
                    base_size = 95
                else:
                    wrapped_phrase_str = " ".join(phrase_words).upper()
                    base_size = 115

                phrase_lower = wrapped_phrase_str.lower()
                is_danger = any(kw in phrase_lower for kw in ['secret', 'trick', 'hidden', 'scam', 'khatarnaak', 'danger', 'alert', 'mat', 'tool', 'ai'])
                
                text_y_pos = TARGET_H * 0.75
                position_filter = get_kinetic_pos(text_y_pos, is_danger, p_i)
                
                if p_i % 3 == 0: current_anim = anim_fluid_spring
                elif p_i % 3 == 1: current_anim = anim_smooth_swell
                else: current_anim = anim_snap_focus
                
                word_rotation = random.choice([-2, -1, 0, 1, 2])
                
                sub_word_weights = [len(w) for w in phrase_words]
                total_sub_weight = sum(sub_word_weights) if sum(sub_word_weights) > 0 else 1
                internal_time = 0.0
                
                # ACTIVE DUAL-LINE WORD TRACKING MATRIX
                for w_idx, active_word in enumerate(phrase_words):
                    sub_duration = (sub_word_weights[w_idx] / total_sub_weight) * phrase_duration
                    word_lower_act = active_word.lower()
                    
                    tracked_components = []
                    for inner_idx, inner_word in enumerate(phrase_words):
                        inner_display = inner_word.upper()
                        if inner_idx == w_idx:
                            if any(kw in word_lower_act for kw in ['secret', 'trick', 'hidden', 'rahasya']): inner_display += " 🤫"
                            elif any(kw in word_lower_act for kw in ['danger', 'khatarnaak', 'alert', 'savdhan']): inner_display += " 🚨"
                            elif any(kw in word_lower_act for kw in ['tool', 'website', 'software', 'app']): inner_display += " 🛠️"
                            elif any(kw in word_lower_act for kw in ['ai', 'bot', 'chatgpt', 'intelligence', 'robot']): inner_display += " 🤖"
                            elif any(kw in word_lower_act for kw in ['money', 'kama', 'earn', 'paisa', 'rich']): inner_display += " 💰"
                        tracked_components.append(inner_display)
                    
                    if len(phrase_words) > 3:
                        f_line1 = " ".join(tracked_components[:mid_point])
                        f_line2 = " ".join(tracked_components[mid_point:])
                        frame_text = f"{f_line1}\n{f_line2}"
                    else:
                        frame_text = " ".join(tracked_components)
                        
                    current_color = '#FF003C' if is_danger else random.choice(viral_colors)
                    
                    try:
                        # 6-LAYERED GAUSSIAN AMBIENT FOG AURA STACK
                        shadow_6 = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(1500, None)).set_opacity(0.15).rotate(word_rotation).resize(current_anim).set_position(get_shadow_pos_matrix(text_y_pos, is_danger, p_i, 24, 28)).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        shadow_5 = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(1500, None)).set_opacity(0.30).rotate(word_rotation).resize(current_anim).set_position(get_shadow_pos_matrix(text_y_pos, is_danger, p_i, 18, 22)).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        shadow_4 = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(1500, None)).set_opacity(0.45).rotate(word_rotation).resize(current_anim).set_position(get_shadow_pos_matrix(text_y_pos, is_danger, p_i, 14, 17)).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        shadow_3 = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(1500, None)).set_opacity(0.60).rotate(word_rotation).resize(current_anim).set_position(get_shadow_pos_matrix(text_y_pos, is_danger, p_i, 10, 12)).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        shadow_2 = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(1500, None)).set_opacity(0.75).rotate(word_rotation).resize(current_anim).set_position(get_shadow_pos_matrix(text_y_pos, is_danger, p_i, 6, 8)).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        shadow_1 = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(1500, None)).set_opacity(0.95).rotate(word_rotation).resize(current_anim).set_position(get_shadow_pos_matrix(text_y_pos, is_danger, p_i, 3, 4)).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        
                        bg_txt = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, stroke_color='black', stroke_width=24, method='caption', size=(1500, None)).rotate(word_rotation).resize(current_anim).set_position(position_filter).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        inner_border_txt = TextClip(frame_text, fontsize=base_size, color='black', font=HINDI_FONT_FILE, stroke_color='white', stroke_width=5, method='caption', size=(1500, None)).rotate(word_rotation).resize(current_anim).set_position(position_filter).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        main_txt = TextClip(frame_text, fontsize=base_size, color=current_color, font=HINDI_FONT_FILE, method='caption', size=(1500, None)).rotate(word_rotation).resize(current_anim).set_position(position_filter).set_duration(sub_duration).set_start(current_phrase_start + internal_time)
                        
                        word_clips.extend([shadow_6, shadow_5, shadow_4, shadow_3, shadow_2, shadow_1, bg_txt, inner_border_txt, main_txt])
                    except: pass
                    
                    internal_time += sub_duration
                
                current_phrase_start += phrase_duration

        dark_overlay = ColorClip(size=(TARGET_W, TARGET_H), color=(0,0,0)).set_opacity(0.40).set_position(('center', 'center')).set_duration(scene_duration)

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

final_duration = final_video.duration
progress_bar = ColorClip(size=(TARGET_W, 15), color=(255, 0, 0))
progress_bar = progress_bar.set_position(lambda t: (-TARGET_W + int(TARGET_W * (t / max(final_duration, 1))), 'bottom'))
progress_bar = progress_bar.set_duration(final_duration)

watermark = TextClip("AIToolKitHub", fontsize=55, color='white', font=HINDI_FONT_FILE, stroke_color='black', stroke_width=2)
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

BOT_TOKEN = "8687740956:AAFwnDe9pNXdHtmAjlLZix3ebQxslTytUwY" 
message_text = f"READY_TO_UPLOAD|{video_link}|{title}|{thumbnail_prompt}|{description}"

try:
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message_text}
    response = requests.post(telegram_url, json=payload)
    print(f"✅ Webhook bypassed! Sent video details directly to Telegram! Status: {response.status_code}")
except Exception as e:
    print(f"❌ Failed to send Telegram alert: {e}")
