@echo off
REM AIRLOCK · Convert GIFs to optimized MP4s for the website
REM Requires ffmpeg in PATH. Download from https://ffmpeg.org/download.html if you don't have it.
REM Run this batch file from the Website_Airlock folder. It will create MP4 versions of all GIFs alongside them.

echo Converting GIFs to MP4...
echo.

for %%f in (Airlock_*.gif) do (
    echo Converting %%f...
    ffmpeg -y -i "%%f" -vcodec libx264 -crf 24 -preset slow -movflags +faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "%%~nf.mp4"
    echo.
)

echo.
echo Done! Compare file sizes:
dir Airlock_*.gif Airlock_*.mp4 | findstr "Airlock_"
echo.
echo Next step: in media.html, swap each GIF reference like:
echo   ^<img src="Airlock_BuildYourBase.gif"^>
echo to:
echo   ^<video src="Airlock_BuildYourBase.mp4" autoplay loop muted playsinline^>^</video^>
echo.
pause
