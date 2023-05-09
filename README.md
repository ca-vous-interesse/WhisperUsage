# WhisperUsage

## Installation de Whisper
### Windows

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
