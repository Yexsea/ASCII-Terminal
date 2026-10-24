import cv2
import time
import os
import sys
import random
import subprocess
import shutil
import imageio_ffmpeg

# Pygame başlangıcındaki karşılama mesajını gizlemek için
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

TEMP_AUDIO_PATH = os.path.join("Medya", "temp_audio.mp3")

def cleanup_temp_audio():
    if os.path.exists(TEMP_AUDIO_PATH):
        try:
            os.remove(TEMP_AUDIO_PATH)
        except Exception:
            pass

def extract_audio(video_path):
    print("Sesi hazırlıyorum, biraz bekle lütfen...")
    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        command = [
            ffmpeg_exe,
            '-i', video_path,
            '-q:a', '0',
            '-map', 'a',
            TEMP_AUDIO_PATH,
            '-y', 
            '-loglevel', 'error'
        ]
        subprocess.run(command, check=True)
        return True
    except Exception as e:
        print(f"Ses çıkarılırken bir hata oluştu (Belki videonun sesi yoktur?): {e}")
        return False

def select_media():
    media_dir = "Medya"
    
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
        print(f"Bulunduğum dizine '{media_dir}' adında bir klasör oluşturdum.")
        print("Lütfen içine birkaç video (.mp4) veya fotoğraf (.jpg, .png) atıp beni tekrar çalıştır!")
        sys.exit()

    valid_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.jpg', '.jpeg', '.png')
    files = [f for f in os.listdir(media_dir) if f.lower().endswith(valid_extensions)]

    if not files:
        print(f"'{media_dir}' klasöründe hiç medya bulamadım. Birkaç şey ekleyip tekrar dene!")
        sys.exit()

    print("\n--- MEDYA SEÇİMİ ---")
    for i, file in enumerate(files):
        print(f"[{i + 1}] {file}")
    
    while True:
        try:
            choice = int(input(f"\nHangi dosyayı açmak istersin? (1-{len(files)}): "))
            if 1 <= choice <= len(files):
                return os.path.join(media_dir, files[choice - 1])
            else:
                print("Lütfen listedeki numaralardan birini gir.")
        except ValueError:
            print("Sadece sayı girmelisin!")

def frame_to_ascii_colored_centered(frame, term_cols, term_lines):
    """Renkli kareyi RGB ANSI kodlarıyla ASCII'ye çevirir ve ortalar."""
    density_buckets = [
        [" "],                                      
        [".", ",", "`", "'"],                        
        ["-", "~", ":", ";", "_"],                  
        ["+", "=", "*", "!", "^", '"'],              
        ["r", "c", "l", "z", "o", "s", "x"],        
        ["?", "v", "u", "a", "k", "h", "d"],        
        ["#", "&", "%", "$", "W", "M", "8", "@", "Q", "0"] 
    ]
    
    height, orig_width, _ = frame.shape
    aspect_ratio = height / orig_width
    
    max_w = term_cols - 2
    max_h = term_lines - 2
    
    aw = max_w
    ah = int(aspect_ratio * aw * 0.45)
    
    if ah > max_h:
        ah = max_h
        aw = int(ah / (aspect_ratio * 0.45))
        
    aw = max(10, aw)
    ah = max(10, ah)

    resized_frame = cv2.resize(frame, (aw, ah))
    
    ascii_lines = []
    for row in resized_frame:
        line_str = ""
        for pixel in row:
            # OpenCV BGR formatında okur, RGB'ye ayırıyoruz
            b, g, r = int(pixel[0]), int(pixel[1]), int(pixel[2])
            
            # Karakter seçimi için insan gözüne uygun parlaklık formülü
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            char_idx = int((brightness / 255) * (len(density_buckets) - 1))
            char = random.choice(density_buckets[char_idx])
            
            # Her karaktere kendi RGB rengini ver (\033[38;2;R;G;Bm)
            line_str += f"\033[38;2;{r};{g};{b}m{char}"
            
        # Satır sonunda rengi sıfırla ki sağdaki boşluklar renkli kalmasın
        line_str += "\033[0m"
        ascii_lines.append(line_str)
        
    pad_y = max(0, (term_lines - ah) // 2)
    pad_x = max(0, (term_cols - aw) // 2)
    
    # Arkaplanın temiz kalması için boşlukları ekle
    output = "\n" * pad_y
    for line in ascii_lines:
        output += (" " * pad_x) + line + "\n"
        
    return output

def play_media_in_terminal(media_path):
    is_image = media_path.lower().endswith(('.jpg', '.jpeg', '.png'))
    
    if os.name == 'nt':
        os.system('')

    sys.stdout.write('\033[?25l')
    sys.stdout.flush()

    try:
        if is_image:
            show_image(media_path)
        else:
            show_video(media_path)
    finally:
        sys.stdout.write('\033[?25h')
        os.system('cls' if os.name == 'nt' else 'clear')
        cleanup_temp_audio()
        print("\nGösteri sona erdi! Görüşmek üzere.")

def show_image(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Hata: {image_path} okunamadı.")
        return
        
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Fotoğraf yüklendi! Çıkmak için terminalde 'Ctrl + C' yapabilirsin.")
    time.sleep(1.5)
    
    prev_term_size = None
    
    try:
        while True:
            term_size = shutil.get_terminal_size()
            
            if prev_term_size != term_size:
                sys.stdout.write('\033[2J') 
                prev_term_size = term_size
                
            ascii_frame = frame_to_ascii_colored_centered(frame, term_size.columns, term_size.lines)
            
            sys.stdout.write('\033[H') 
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()
            time.sleep(0.1) 
    except KeyboardInterrupt:
        pass

def show_video(video_path):
    has_audio = extract_audio(video_path)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Hata: {video_path} okunamadı.")
        return

    if has_audio:
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(TEMP_AUDIO_PATH)
        except pygame.error:
            has_audio = False

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1.0 / fps if fps > 0 else 1.0 / 30.0

    print("İşlemleri tamamladım... Terminali tam ekran (F11) yapabilirsin!")
    time.sleep(2)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if has_audio:
        pygame.mixer.music.play()
    
    prev_term_size = None
    
    start_time = time.time()
    frame_count = 0
    
    try:
        while cap.isOpened():
            if has_audio and not pygame.mixer.music.get_busy():
                break
                
            ret, frame = cap.read()
            
            if not ret:
                break
                
            frame_count += 1

            term_size = shutil.get_terminal_size()
            
            if prev_term_size != term_size:
                sys.stdout.write('\033[2J')
                prev_term_size = term_size
                
            ascii_frame = frame_to_ascii_colored_centered(frame, term_size.columns, term_size.lines)
            
            sys.stdout.write('\033[H')
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()
            
            expected_time = frame_count * frame_duration 
            elapsed_time = time.time() - start_time      
            sleep_time = expected_time - elapsed_time    
            
            if sleep_time > 0:
                time.sleep(sleep_time) 
            else:
                # KARE ATLAMA (FRAME DROP) MANTIĞI:
                # Terminal sese yetişemeyip geride kalırsa, aradaki bazı kareleri okuyup hiç çizmeden çöpe atıyoruz.
                while expected_time < elapsed_time:
                    # grab() fonksiyonu read()'den daha hızlıdır, sadece kareyi geçer, decode etmez.
                    ret = cap.grab() 
                    if not ret:
                        break
                    frame_count += 1
                    expected_time = frame_count * frame_duration
                
    except KeyboardInterrupt:
        pass 
    finally:
        if has_audio:
            pygame.mixer.music.stop()
            pygame.mixer.quit() 
        cap.release()

if __name__ == "__main__":
    cleanup_temp_audio()
    secilen_medya = select_media()
    play_media_in_terminal(secilen_medya)