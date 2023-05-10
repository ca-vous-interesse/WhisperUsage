# WhisperUsage

## Installation de Whisper
### Windows
Tapez Win+X et sélectionnez le PowerShell (admin)

    Set-ExecutionPolicy AllSigned
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

Restart PowerShell : tapez Win+X et sélectionnez le PowerShell (admin)

    choco install python --version 3.10 --side-by-side
    choco install ffmpeg
    C:\Python310\python -m pip install python-ffmpeg
    choco install git
    C:\Python310\python -m pip install git+https://github.com/openai/whisper.git
    C:\Python310\python -m pip cache purge
    choco install yt-dlp
    whisper --model base --language fr audio.mp3
    whisper --model base --language fr --task translate audio.mp3

### Mac Os
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install git
    brew install python@3.10
    pip3.10 install -U openai-whisper
    brew install ffmpeg
    pip install git+https://github.com/openai/whisper.git
    brew install yt-dlp

En cas d'érreur sur l'installation précédente de ffmpeg (j'ai eu ce problème) réinstaller ffmpeg comme suit:
    
    pip3 uninstall ffmpeg
    pip3 uninstall ffmpeg-python
    pip uninstall ffmpeg
    pip uninstall ffmpeg-python
    brew uninstall ffmpeg

## Mon petit script pour exploiter Whisper
    YoutubeTranscriptDemo.py

Il sait:
- Prendre une URL d'une video YouTube et en extraire l'audio (respectez le copyright!)
- Prendre l'audio d'une video sur votre disque
- Travailler sur un fichier audio sur votre disque
- En extraire un texte
- En extraire un fichier de sous-titres .srt

Github original de Whisper:

    https://github.com/openai/whisper
    
Version modifiée pour avoir un horodatage plus précis des mots:

    https://github.com/jianfch/stable-ts
    https://github.com/m-bain/whisperX
    https://github.com/linto-ai/whisper-timestamped
    
