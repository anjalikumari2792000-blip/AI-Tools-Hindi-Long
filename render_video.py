import os, sys, requests, json, subprocess, socket, gc, math, random
import urllib3.util.connection as urllib3_cn
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, TextClip, ColorClip, afx

# Force IPv4 to bypass strict server blocks
def allowed_gai_family():
    return socket.AF_INET
urllib3_cn.allowed_gai_family = allowed_gai_family

HINDI_FONT_FILE = "Hindi.ttf" 

# --- VARIABLES FETCHED FROM GITHUB ACTIONS ---
chat_id = os.environ.get('CHAT_ID')
pexels_key = os.environ.get('PEXELS_API_KEY')
scenes_data = json.loads(os.environ.get('SCENES_DATA', '[]'))
title = os.environ.get('TITLE', 'Mind-blowing Earning Secret')
description = os.environ.get('DESCRIPTION', 'Make money online secret tricks.')
thumbnail_prompt = os.environ.get('THUMBNAIL_PROMPT', 'Cinematic beautiful thumbnail')

print(f"Total Scenes to render: {len(scenes_data)}")

# LONG FORMAT (Landscape 1920x1080) for Earn-Smart
TARGET_W, TARGET_H = 1920, 1080
viral_colors = ['#FFD400', '#00FFFF', '#FFFFFF', '#39FF14']
headers = {"Authorization": pexels_key}

try:
    whoosh_sfx = AudioFileClip("whoosh.mp3").volumex(0.25)
    pop_sfx = AudioFileClip("pop.mp3").volumex(0.15)        
except:
    whoosh_sfx = pop_sfx = None

rendered_videos = []
rendered_audios = []
scene_durations = []

# ==========================================
# Process Each Scene (NO AUDIO OVERLAP BUG)
# ==========================================
for i, scene in enumerate(scenes_data):
    keyword = scene.get('keyword', 'finance')
    text_line = scene.get('text', '').strip()
    
    if not text_line: continue
    
    temp_txt_path = f"temp_scene_{i}.txt"
    raw_audio = f"raw_audio_{i}.mp3"
    trimmed_audio = f"trimmed_audio_{i}.wav" # WAV ensures perfect frame timing
    
    with open(temp_txt_path, "w", encoding="utf-8") as f:
        f.write(text_line)
        
    try:
        # 1. Native Speedup: MoviePy ki jagah Edge-TTS mein rate badha diya
        subprocess.run([sys.executable, '-m', 'edge_tts', '--voice', 'hi-IN-SwaraNeural', '--rate=+10%', '-f', temp_txt_path, '--write-media', raw_audio], check=True)
        
        # 2. Perfect Trim: FFmpeg se exact 0.2s hataya aur WAV mein convert kiya
        subprocess.run(['ffmpeg', '-y', '-i', raw_audio, '-ss', '0.2', '-c:a', 'pcm_s16le', trimmed_audio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 3. Get exact duration
        clip_audio = AudioFileClip(trimmed_audio)
        scene_duration = clip_audio.duration
        clip_audio.close()
        
        scene_durations.append(scene_duration)
        
    except Exception as e:
        print(f"Audio failed for scene {i}: {e}")
        continue
        
    # 🚀 OPTIMIZED TOPIC-BASED VIDEO FETCHING (Matches exactly what TTS says) 🚀
    try:
        kw_lower = keyword.lower()
        # Checks if context belongs to AI, Software, Web, Traffic or SEO
        if any(k in kw_lower for k in ['ai', 'tech', 'robot', 'bot', 'website', 'crypto', 'chatgpt', 'software', 'seo', 'traffic', 'internet', 'computer']):
            search_query = f"{keyword} technology abstract"
        elif any(k in kw_lower for k in ['money', 'earn', 'finance', 'wealth', 'cash', 'rich', 'income', 'profit', 'business', 'sale']):
            search_query = f"{keyword} finance wealth"
        else:
            search_query = keyword
            
        res = requests.get(f"https://api.pexels.com/videos/search?query={search_query}&per_page=1&orientation=landscape", headers=headers, timeout=15).json()
        
        if 'videos' in res and len(res['videos']) > 0:
            video_url = res['videos'][0]['video_files'][0]['link']
        else:
            res = requests.get("https://api.pexels.com/videos/search?query=abstract technology money&per_page=1&orientation=landscape", headers=headers, timeout=15).json()
            video_url = res['videos'][0]['video_files'][0]['link']
        
        vid_path = f"vid_{i}.mp4"
        with open(vid_path, "wb") as f:
            f.write(requests.get(video_url, timeout=30).content)
            
        clip = VideoFileClip(vid_path).subclip(0, min(scene_duration, VideoFileClip(vid_path).duration))
        if clip.duration < scene_duration:
            clip = afx.vfx.loop(clip, duration=scene_duration)
            
        clip = clip.resize(height=TARGET_H)
        if clip.w < TARGET_W: clip = clip.resize(width=TARGET_W)
        clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=TARGET_W, height=TARGET_H)
        
        # Zoom Effect & Overlay
        zoomed_clip = clip.resize(lambda t: 1.0 + 0.04 * (t / scene_duration)).set_position(('center', 'center'))
        dark_overlay = ColorClip(size=(TARGET_W, TARGET_H), color=(0,0,0)).set_opacity(0.40).set_duration(scene_duration).set_position(('center', 'center'))
        
        # 🔥 ULTRA-PREMIUM KINETIC TEXT ENGINE (Directional 3D Projection Mastery) 🔥
        def premium_elastic_pop(t):
            if t == 0: return 0.3
            if t < 0.05:
                return 0.3 + 0.7 * (t / 0.05)
            t_norm = min((t - 0.05) / 0.20, 1.0)
            val = 1.0 + 0.15 * math.sin(t_norm * math.pi * 3.0) * math.exp(-t_norm * 4.0)
            return val

        def get_kinetic_pos(clip_w, clip_h, base_y, is_shaking, phrase_idx, x_offset=0, y_offset=0):
            def pos(t):
                # Smooth organic floating wave
                idle_y = 3.0 * math.sin(t * 4.5 + phrase_idx)
                idle_x = 1.5 * math.cos(t * 3.5 + phrase_idx)
                
                # Center the bounding box horizontally and vertically on screen
                final_x = (TARGET_W - clip_w) / 2 + idle_x + x_offset
                final_y = base_y - (clip_h / 2) + idle_y + y_offset

                if is_shaking and t > 0.04:
                    return (final_x + 5.5 * math.sin(t * 88), final_y + 5.5 * math.cos(t * 93))
                return (final_x, final_y)
            return pos

        raw_words = text_line.split()
        
        # 🚀 SMART PHRASE GROUPING SYSTEM (2-3 Words Display) 🚀
        phrases = []
        temp_phrase = []
        for w in raw_words:
            temp_phrase.append(w)
            if len(temp_phrase) >= 2 or w.endswith(',') or w[-1] in '.?!।':
                phrases.append(" ".join(temp_phrase))
                temp_phrase = []
        if temp_phrase:
            phrases.append(" ".join(temp_phrase))

        word_clips = []

        if phrases:
            phrase_weights = []
            for p in phrases:
                wt = len(p)
                if p.endswith(','): wt += 3  
                elif p[-1] in '.?!।': wt += 6 
                phrase_weights.append(wt)
            
            total_weight = sum(phrase_weights) if sum(phrase_weights) > 0 else 1
            current_time_pos = 0.0

            for p_i, phrase_text in enumerate(phrases):
                phrase_clean = phrase_text.upper()
                phrase_lower = phrase_text.lower()
                
                # Highlight & Danger keyword triggers
                is_danger = any(kw in phrase_lower for kw in ['secret', 'trick', 'hidden', 'scam', 'khatarnaak', 'danger', 'alert', 'mat', 'paisa', 'paise', 'income', 'profit', 'earn'])
                is_highlight = not is_danger and any(len(w) > 4 for w in phrase_text.split())
                
                duration_per_phrase = (phrase_weights[p_i] / total_weight) * scene_duration

                # Curated High-Vibrancy Modern Color Palette
                current_color = '#FF0044' if is_danger else ('#0D0D0D' if is_highlight else '#FFFFFF')
                
                # Intelligent Semantic Color Engine based on scene context keyword
                if is_danger:
                    bg_color = 'transparent'
                elif is_highlight:
                    if any(k in kw_lower for k in ['ai', 'tech', 'robot', 'bot', 'website', 'crypto', 'chatgpt', 'software', 'seo', 'traffic']):
                        bg_color = '#00FFFF'  # Cyber Neon Cyan
                    elif any(k in kw_lower for k in ['money', 'earn', 'finance', 'wealth', 'rich', 'cash', 'income', 'profit', 'business']):
                        bg_color = '#00FF55'  # Premium Neon Green
                    else:
                        bg_color = '#FFEA00'  # High-Contrast Vibrant Yellow
                else:
                    bg_color = 'transparent'
                
                # 🚀 SMART DISPLAY REPLACEMENT ENGINE (TTS filter back to premium clean text) 🚀
                display_phrase = phrase_clean
                replacements = {
                    "SEY": "SE", "KEY": "KE", "NEY": "NE", "DEY": "DE", "KAISEY": "KAISE", "AISEY": "AISE",
                    "HOTEY": "HOTE", "KARTEY": "KARTE", "APNEY": "APNE", "SAMAJHTEY": "SAMAJHTE", 
                    "PEHLEY": "PEHLE", "KARKEY": "KARKE", "CHALEY": "CHALE", "PURAANEY": "PURANE", "BACHCHEY": "BACHCHE",
                    "KIYAA": "KIYA", "DIYAA": "DIYA", "LIYAA": "LIYA", "SIKHAATEE": "SIKHATI", 
                    "DIKHAATEY": "DIKHATE", "CHAAHATEY": "CHAHTE", "BANAATEY": "BANATE", 
                    "SBB": "SAB", "ABB": "AB", "THEY": "THE", "TARIKAY": "TARIKA", "BUND": "BAND", "MUT": "MAT", "JUB": "JAB", "PUL": "PAL"
                }
                for k, v in replacements.items():
                    display_phrase = display_phrase.replace(f" {k} ", f" {v} ")
                    if display_phrase.startswith(k + " "): display_phrase = display_phrase.replace(k + " ", v + " ", 1)
                    if display_phrase.endswith(" " + k): display_phrase = display_phrase.replace(" " + k, " " + v, 1)
                    if display_phrase == k: display_phrase = v

                # Continuous Proportional Font Scaling based on visual string character length
                char_count = len(display_phrase.strip())
                if char_count > 14:
                    base_size = max(125, 165 - (char_count - 11) * 3)
                elif char_count > 7:
                    base_size = 155
                else:
                    base_size = 170
                    
                if is_danger: base_size += 10
                
                # Dynamic Adaptive Spacing (Smart Tracking metrics calculation)
                adaptive_kerning = 4 if char_count <= 8 else (3 if char_count <= 14 else 1.5)
                
                # Add micro space padding horizontally for premium sticker badge spacing
                if bg_color != 'transparent':
                    display_phrase = f"  {display_phrase}  "
                
                phrase_tilt = random.choice([-2.5, -1, 1, 2.5]) if (is_danger or is_highlight) else random.choice([-1, 0, 1])

                try:
                    text_y_pos = TARGET_H * 0.76  # Safe zone position
                    
                    if bg_color == 'transparent':
                        box_width = 1600 
                        
                        # Pre-generate layers to extract exact post-rotation dimensions
                        main_txt_layer = TextClip(display_phrase, fontsize=base_size, color=current_color, font=HINDI_FONT_FILE, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning).rotate(phrase_tilt)
                        rotated_w = main_txt_layer.w
                        rotated_h = main_txt_layer.h
                        main_txt_layer.close()
                        
                        # Ambient Neon Radiance Glow Aura Layer
                        glow_color = '#FF0044' if is_danger else '#FFFFFF'
                        glow_txt = TextClip(display_phrase, fontsize=base_size, color=glow_color, font=HINDI_FONT_FILE, stroke_color=glow_color, stroke_width=45, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_opacity(0.18) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        # True Directional 3D Projection Math Engine based on Rotation Angle
                        rad_tilt = math.radians(phrase_tilt)
                        cos_t = math.cos(rad_tilt)
                        sin_t = math.sin(rad_tilt)
                        
                        # Generates gapless geometric projection stack vector points mapping
                        dx4, dy4 = int(14 * cos_t + 16 * sin_t), int(-14 * sin_t + 16 * cos_t)
                        dx3, dy3 = int(9 * cos_t + 11 * sin_t), int(-9 * sin_t + 11 * cos_t)
                        dx2, dy2 = int(5 * cos_t + 6 * sin_t), int(-5 * sin_t + 6 * cos_t)
                        
                        # 4-Stage Progressive Projected Shadow Layers
                        shadow_4 = TextClip(display_phrase, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i, x_offset=dx4, y_offset=dy4)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        shadow_3 = TextClip(display_phrase, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i, x_offset=dx3, y_offset=dy3)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)

                        shadow_2 = TextClip(phrase_clean, fontsize=base_size, color='black', font=HINDI_FONT_FILE, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i, x_offset=dx2, y_offset=dy2)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        # Master Heavy Background Stroke
                        bg_txt = TextClip(display_phrase, fontsize=base_size, color='black', font=HINDI_FONT_FILE, stroke_color='black', stroke_width=24, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        # Inner Clean Crisp Outline
                        inner_border_txt = TextClip(display_phrase, fontsize=base_size, color='black', font=HINDI_FONT_FILE, stroke_color='white', stroke_width=6, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        # Primary Front Text Layer
                        main_txt = TextClip(display_phrase, fontsize=base_size, color=current_color, font=HINDI_FONT_FILE, method='caption', size=(box_width, None), align='Center', interline=-6, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        word_clips.extend([glow_txt, shadow_4, shadow_3, shadow_2, bg_txt, inner_border_txt, main_txt])
                    else:
                        # Extract exact post-rotation layout dimensions for badge highlights
                        temp_badge = TextClip(display_phrase, fontsize=base_size, color=current_color, bg_color=bg_color, font=HINDI_FONT_FILE, kerning=adaptive_kerning).rotate(phrase_tilt)
                        rotated_w = temp_badge.w
                        rotated_h = temp_badge.h
                        temp_badge.close()
                        
                        # Soft Neon Glow backing for premium badge highlights
                        glow_txt = TextClip(display_phrase, fontsize=base_size, color=bg_color, font=HINDI_FONT_FILE, stroke_color=bg_color, stroke_width=35, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_opacity(0.15) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        rad_tilt = math.radians(phrase_tilt)
                        bx_off, by_off = int(11 * math.cos(rad_tilt) + 13 * math.sin(rad_tilt)), int(-11 * math.sin(rad_tilt) + 13 * math.cos(rad_tilt))
                        
                        bg_shadow = TextClip(display_phrase, fontsize=base_size, color='black', bg_color='black', font=HINDI_FONT_FILE, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i, x_offset=bx_off, y_offset=by_off)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                            
                        main_txt = TextClip(display_phrase, fontsize=base_size, color=current_color, bg_color=bg_color, font=HINDI_FONT_FILE, kerning=adaptive_kerning) \
                            .resize(premium_elastic_pop).rotate(phrase_tilt) \
                            .set_position(get_kinetic_pos(rotated_w, rotated_h, text_y_pos, is_danger, p_i)) \
                            .set_duration(duration_per_phrase).set_start(current_time_pos)
                        
                        word_clips.extend([glow_txt, bg_shadow, main_txt])
                except: pass
                
                current_time_pos += duration_per_phrase

        final_scene = CompositeVideoClip([zoomed_clip, dark_overlay] + word_clips, size=(TARGET_W, TARGET_H)).set_duration(scene_duration)
        
        # Render Scene using "superfast" for sharp intermediate text compression quality
        scene_filename = f"scene_rendered_{i}.mp4"
        final_scene.write_videofile(scene_filename, fps=24, codec="libx264", preset="superfast", audio=False, logger=None)
        
        rendered_videos.append(scene_filename)
        rendered_audios.append(trimmed_audio)
        
        final_scene.close()
        clip.close()
        del final_scene, clip, zoomed_clip, word_clips
        gc.collect()
        
        print(f"Scene {i+1} Ready: {keyword}")
        
        if os.path.exists(temp_txt_path): os.remove(temp_txt_path)
        if os.path.exists(raw_audio): os.remove(raw_audio)
        
    except Exception as e:
        print(f"Error on scene {i} video processing: {e}")

# ==========================================
# DISK CONCATENATION (Merging Safely)
# ==========================================
print("Merging Video scenes safely...")
with open("vid_concat.txt", "w") as f:
    for file in rendered_videos:
        f.write(f"file '{file}'\n")

subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'vid_concat.txt', '-c', 'copy', 'merged_video.mp4'])

print("Merging Audio scenes safely...")
with open("aud_concat.txt", "w") as f:
    for file in rendered_audios:
        f.write(f"file '{file}'\n")

subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'aud_concat.txt', '-c', 'pcm_s16le', 'merged_audio.wav'])

final_video = VideoFileClip("merged_video.mp4")
final_audio = AudioFileClip("merged_audio.wav")

master_audio_clips = [final_audio]
current_time = 0.0

# Add SFX strictly aligned with exact scene timings
for dur in scene_durations:
    if whoosh_sfx:
        master_audio_clips.append(whoosh_sfx.set_start(current_time))
    current_time += dur

# PROGRESS BAR
progress_bar = ColorClip(size=(TARGET_W, 15), color=(255, 0, 0))
progress_bar = progress_bar.set_position(lambda t: (-TARGET_W + int(TARGET_W * (t / max(final_video.duration, 1))), 'bottom'))
progress_bar = progress_bar.set_duration(final_video.duration)

# 🔥 Earn Smart Hindi Watermark Implementation 🔥
watermark = TextClip("Earn Smart Hindi", fontsize=55, color='white', font=HINDI_FONT_FILE, stroke_color='black', stroke_width=2)
watermark = watermark.set_opacity(0.5).set_position((0.75, 0.88), relative=True).set_duration(final_video.duration)

final_video = CompositeVideoClip([final_video, progress_bar, watermark])

# BACKGROUND MUSIC
try:
    bgm = AudioFileClip("bgm.mp3").volumex(0.08)
    if bgm.duration < final_video.duration: bgm = afx.audio_loop(bgm, duration=final_video.duration)
    else: bgm = bgm.subclip(0, final_video.duration)
    master_audio_clips.append(bgm)
except: pass

final_combined_audio = CompositeAudioClip(master_audio_clips)
final_video = final_video.set_audio(final_combined_audio)

# Increased bitrate to 3000k and optimized preset to "superfast" for premium quality compression bounds
print("Rendering Final COMPRESSED LONG Video...")
final_video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac", threads=2, bitrate="3000k", preset="superfast")

# ==========================================
# UPLOAD SYSTEM
# ==========================================
print("Starting Core Indestructible Upload System...")
video_link = "Upload Failed"

endpoints = [
    ("File.io", "https://file.io", "file", lambda r: r.json()['link']),
    ("0x0.st", "https://0x0.st", "file", lambda r: r.text.strip()),
    ("Uguu.se", "https://uguu.se/upload.php", "files[]", lambda r: r.json()['files'][0]['url']),
    ("Catbox.moe", "https://catbox.moe/user/api.php", "reqtype", lambda r: r.text.strip())
]

for name, url, field, get_link in endpoints:
    if video_link != "Upload Failed" and video_link.startswith("http"): break
    try:
        print(f"Trying upload to {name}...")
        files = {field: open("final_video.mp4", 'rb')}
        data = {'reqtype': 'fileupload'} if "catbox" in url else {}
        res = requests.post(url, files=files, data=data, timeout=300)
        
        if res.status_code == 200:
            link = get_link(res)
            if "http" in link: 
                video_link = link
                print(f"✅ Upload Success: {video_link}")
    except Exception as e: 
        print(f"❌ {name} failed: {e}")

# ==========================================
# TELEGRAM BRIDGE
# ==========================================
BOT_TOKEN = "8519514437:AAGt391NG3FPuciBLtCAt0XHIbEqwDef0vU" 

safe_description = str(description).replace('\n', '  ')
safe_title = str(title).replace('|', '')

if not chat_id or chat_id == "None":
    print("❌ Error: CHAT_ID is missing. Cannot send Telegram message.")
else:
    message_text = f"READY_TO_UPLOAD|{video_link}|{safe_title}|{thumbnail_prompt}|{safe_description}"
    
    if len(message_text) > 4000:
        message_text = message_text[:3990] + "...[TRUNC]"

    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": str(chat_id).strip(), "text": message_text}
        response = requests.post(telegram_url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Webhook bypassed! Sent video details directly to Telegram! Status: {response.status_code}")
        else:
            print(f"❌ Telegram alert failed! Status: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
