import cv2
import time
import os
import sys
import random

# Pygame başlangıcındaki karşılama mesajını gizlemek için
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def frame_to_ascii(frame, width=140):
    """Bir video karesini rastgele ve hareketli ASCII karakterlerine dönüştürür."""
    density_buckets = [
        [" "],                                      
        [".", ",", "`", "'"],                       
        ["-", "~", ":", ";", "_"],                  
        ["+", "=", "*", "!", "^", '"'],             
        ["r", "c", "l", "z", "o", "s", "x"],        
        ["?", "v", "u", "a", "k", "h", "d"],        
        ["#", "&", "%", "$", "W", "M", "8", "@", "Q", "0"] 
    ]
    
    height, orig_width = frame.shape
    aspect_ratio = height / orig_width
    new_height = int(aspect_ratio * width * 0.45)
    resized_frame = cv2.resize(frame, (width, new_height))
    
    ascii_str = ""
    for row in resized_frame:
        for pixel_value in row:
            bucket_index = int((pixel_value / 255) * (len(density_buckets) - 1))
            bucket = density_buckets[bucket_index]
            
            # Tamamen rastgele seçim! Her beyaz alan sürekli kaynayacak.
            ascii_str += random.choice(bucket)
            
        ascii_str += "\n"
        
    return ascii_str

def play_bad_apple(video_path, audio_path):
    """Videoyu ve sesi aynı anda terminalde oynatır."""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Hata: {video_path} bulunamadı. Lütfen videonun adını ve yerini kontrol et.")
        return

    # Windows terminallerinde ANSI renk/konum kodlarını aktif etmek için
    if os.name == 'nt':
        os.system('')

    pygame.mixer.init()
    try:
        pygame.mixer.music.load(audio_path)
    except pygame.error:
        print(f"Hata: {audio_path} bulunamadı veya yüklenemedi. MP3 dosyanı kontrol et.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1.0 / fps if fps > 0 else 1.0 / 30.0

    print("Saf kaos yükleniyor... Terminali tam ekran yap!")
    time.sleep(2)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    pygame.mixer.music.play()
    
    try:
        while cap.isOpened() and pygame.mixer.music.get_busy():
            start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ascii_frame = frame_to_ascii(gray_frame, width=140)
            
            sys.stdout.write('\033[H')
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()
            
            processing_time = time.time() - start_time
            sleep_time = frame_duration - processing_time
            if sleep_time > 0:
                time.sleep(sleep_time)
                
    except KeyboardInterrupt:
        pass 
        
    finally:
        pygame.mixer.music.stop()
        cap.release()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Gösteri sona erdi!")

if __name__ == "__main__":
    # Kodun bulunduğu klasörde bu iki dosyanın olduğundan emin ol
    video_dosyasi = "bad_apple.mp4"
    ses_dosyasi = "bad_apple.mp3" 
    
    play_bad_apple(video_dosyasi, ses_dosyasi)