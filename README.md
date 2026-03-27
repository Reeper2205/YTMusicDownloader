# YTMusicDownloader
This Python script creates a graphical user interface (GUI) application using tkinter to download audio from YouTube videos as MP3 files using the yt_dlp library.

The script provides a user-friendly GUI for downloading YouTube videos as MP3 files. Users enter a YouTube URL, optionally specify an output directory, and click "Download MP3" to save the audio. The app shows progress, handles errors, and ensures the GUI remains responsive by using threading. It relies on ffmpeg.exe for audio conversion, which must be included when bundled as an executable.

Still on going. create an EXE for this but too large to upload.

Recent updates allow this to work with Windows 11. 

Prerequisites

    Python 3.8 or higher
    Git (optional, for cloning)

Step 1: Download the Project

Option A: Using Git

bash

git clone https://github.com/Reeper2205/YTMusicDownloader.git
cd YTMusicDownloader

Option B: Direct Download

    Visit https://github.com/Reeper2205/YTMusicDownloader
    Click the green "Code" button
    Select "Download ZIP"
    Extract the ZIP file to your desired location

Step 2: Install Python Dependencies

Install the required packages manually:

bash

pip install yt-dlp
pip install mutagen

Common dependencies for YouTube downloaders:

    yt-dlp - The core YouTube download library
    mutagen - For adding metadata to audio files (optional but recommended)

Note: Check the Python files in the project to see if any other libraries are imported and install them as needed.
Step 3: Download FFmpeg and FFprobe

Windows:

    Download FFmpeg from https://www.gyan.dev/ffmpeg/builds/
        Choose the "ffmpeg-release-essentials.zip" build
    Extract the ZIP file to a temporary location
    Copy the following files from the bin folder:
        ffmpeg.exe
        ffprobe.exe
    Place these files in your project's root directory (same folder as your Python script)


Step 4: Create an Executable with Bundled FFmpeg

Using PyInstaller (Recommended):

    Install PyInstaller:

bash

pip install pyinstaller

    Create the executable with bundled FFmpeg and FFprobe:

bash

pyinstaller --onefile --windowed --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." --icon=icon.ico main.py

PyInstaller Options Explained:

    --onefile - Creates a single executable file
    --windowed - Hides the console window (remove if you want to see output)
    --add-binary "ffmpeg.exe;." - Bundles ffmpeg.exe with the executable
    --add-binary "ffprobe.exe;." - Bundles ffprobe.exe with the executable
    --icon=icon.ico - Adds a custom icon (optional)

    Find your executable in the dist folder

Alternative - Using Auto-py-to-exe (GUI Method):

    Install auto-py-to-exe:

bash

pip install auto-py-to-exe

    Launch the GUI:

bash

auto-py-to-exe

    Configure settings:
        Script Location: Select your main Python file
        Onefile: Select "One File"
        Console Window: Select "Window Based" (no console)
        Icon: (Optional) Add your icon file
        Additional Files:
            Click "Add Files"
            Add ffmpeg.exe (destination: .)
            Add ffprobe.exe (destination: .)
        Click "Convert .py to .exe"

    The executable will be created in the output folder


Step 5: Distribute to Family

    Copy the .exe file from the dist folder
    That's it! FFmpeg and FFprobe are now bundled inside the executable
    No additional installation required for end users
    Optionally, create a simple folder structure:

    YTMusicDownloader/
    ├── YTMusicDownloader.exe
    ├── README.txt (simple instructions)
    └── Downloads/ (folder for downloaded music)

    Create a ZIP file for easy distribution

Troubleshooting

"FFmpeg not found" error even with bundled version:

    Ensure your Python code uses the get_ffmpeg_path() function above
    Check that sys._MEIPASS is being used correctly in the compiled executable
    Verify both ffmpeg.exe and ffprobe.exe were in the project folder before building

File Structure

Your project should look like this before building:

YTMusicDownloader/
├── main.py (or your main script)
├── ffmpeg.exe
├── ffprobe.exe
├── icon.ico (optional)
└── other_files.py

After building with PyInstaller:

YTMusicDownloader/
├── build/ (temporary build files)
├── dist/
│   └── YTMusicDownloader.exe (distribute this!)
├── main.py
├── ffmpeg.exe
├── ffprobe.exe
└── YTMusicDownloader.spec (PyInstaller config)
