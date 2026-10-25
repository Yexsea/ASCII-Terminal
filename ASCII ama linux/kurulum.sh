#!/usr/bin/env bash
# Ubuntu/Debian tabanlı sistemler için kurulum
set -e
cd "$(dirname "$0")"

echo "Sistem gereksinimleri kontrol ediliyor..."

# Python 3.8 veya üstü yeterli; sistemde yoksa paket yöneticisiyle kurulur
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 bulunamadı, kuruluyor..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "Python 3.8 veya üstü gerekli. Sistemdeki sürüm: $(python3 --version)"
    exit 1
fi
echo "Harika, $(python3 --version) kullanılacak."

# Sanal ortam modülü bazı dağıtımlarda ayrı paket olarak geliyor
if ! python3 -c 'import ensurepip' >/dev/null 2>&1; then
    echo "venv modülü eksik, kuruluyor..."
    sudo apt-get update
    sudo apt-get install -y python3-venv
fi

echo "Sanal ortam (venv) oluşturuluyor..."
python3 -m venv venv

echo "Gerekli kütüphaneler kuruluyor..."
./venv/bin/python -m pip install --upgrade pip
# Görüntü terminale çizildiği için pencere desteği olmayan (headless) OpenCV yeterli
./venv/bin/python -m pip install opencv-python-headless pygame imageio-ffmpeg

mkdir -p Medya

echo "------------------------------------------------------"
echo "Kurulum tamamlandı!"
echo "Lütfen 'Medya' klasörüne videolarını veya fotoğraflarını ekle."
echo "Ardından 'bash baslat.sh' komutuyla programı çalıştırabilirsin."
echo "------------------------------------------------------"
