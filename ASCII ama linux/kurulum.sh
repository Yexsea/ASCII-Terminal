#!/bin/bash
# Ubuntu/Debian tabanlı sistemler için kurulum

PYTHON_VERSION="3.11.8"

echo "Sistem gereksinimleri kontrol ediliyor..."

# Tam olarak 3.11.8 var mı kontrol et
if command -v python3.11 &> /dev/null && python3.11 --version 2>&1 | grep -q "$PYTHON_VERSION"; then
    echo "Harika, Python $PYTHON_VERSION sisteminde zaten kurulu!"
else
    echo "Python $PYTHON_VERSION tam olarak bulunamadı."
    echo "Baştan indirip kaynak kodundan derliyorum (Bu işlem bilgisayarının hızına göre birkaç dakika sürebilir)..."
    
    sudo apt-get update
    sudo apt-get install -y wget build-essential libncursesw5-dev libssl-dev \
        libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
    tar -xf Python-$PYTHON_VERSION.tgz
    cd Python-$PYTHON_VERSION
    
    ./configure --enable-optimizations
    sudo make altinstall
    
    cd ..
    rm -rf Python-$PYTHON_VERSION Python-$PYTHON_VERSION.tgz
    echo "Python $PYTHON_VERSION başarıyla kuruldu!"
fi

echo "Sanal ortam (venv) oluşturuluyor..."
python3.11 -m venv venv
source venv/bin/activate

echo "Gerekli kütüphaneler kuruluyor..."
pip install --upgrade pip
pip install opencv-python pygame imageio-ffmpeg

mkdir -p Medya

echo "------------------------------------------------------"
echo "Kurulum tamamlandı!"
echo "Lütfen 'Medya' klasörüne videolarını veya fotoğraflarını ekle."
echo "Ardından './baslat.sh' komutuyla programı çalıştırabilirsin."
echo "------------------------------------------------------"