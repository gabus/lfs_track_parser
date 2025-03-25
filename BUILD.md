### Build .exe files for Windows using PyInstaller.
```bash
pip install -r requirements.txt
pyinstaller --onefile .\track_decoder.py
pyinstaller --onefile .\track_encoder.py
```

### Run it 
```bash
.\track_decoder.exe -i encoded_tracks\AU1_FG_2023_practise.lyt -o decoded_tracks\AU1_FG_2023_practise.json
```
