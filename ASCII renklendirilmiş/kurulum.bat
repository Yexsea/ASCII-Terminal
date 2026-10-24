@echo off
title Terminal Medya Oynaticisi Kurulum Araci
color 0A

echo ===================================================
echo     TERMINAL MEDYA OYNATICISI KURULUM ARACI
echo ===================================================
echo.
echo Merhaba! Gerekli kutuphaneleri kurmaya basliyorum...
echo Lutfen islemler bitene kadar bu pencereyi kapatmayin.
echo.

:: Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo HATA: Bilgisayarinda Python kurulu degil veya PATH'e eklenmemis!
    echo Lutfen python.org adresinden Python'u indirip kurarken 
    echo "Add Python to PATH" secenegini isaretlediginden emin ol.
    echo.
    pause
    exit /b
)

echo [1/5] OpenCV kuruluyor (Goruntu isleme icin)...
pip install opencv-python
echo.

echo [2/5] Pygame kuruluyor (Ses senkronizasyonu icin)...
pip install pygame
echo.

echo [3/5] ImageIO-FFMPEG kuruluyor (Sesi videodan ayirmak icin)...
pip install imageio-ffmpeg
echo.

echo [4/5] Numpy kuruluyor (Piksel hesaplamalarini hizlandirmak icin)...
pip install numpy
echo.

echo [5/5] YT-DLP kuruluyor (YouTube videolari indirebilmek icin)...
pip install yt-dlp
echo.

color 0B
echo ===================================================
echo HARIKA! Tum kurulumlar basariyla tamamlandi.
echo Artik ana Python dosyani sorunsuz calistirabilirsin.
echo Iyi eglenceler! 🤓
echo ===================================================
echo.
pause