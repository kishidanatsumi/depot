::一图流
@echo off
setlocal enabledelayedexpansion

set OUTPUT_FOLDER=output
if not exist "%OUTPUT_FOLDER%" mkdir "%OUTPUT_FOLDER%"

for %%F in (song3_gdsign_*.wav) do (
    set "SOUND_FILE=%%F"
    set "OUTPUT_FILE=!OUTPUT_FOLDER!\%%~nF.mp4"
::    echo !SOUND_FILE!
::    echo !OUTPUT_FILE!
	
	ffmpeg -loop 1 -y -i 1280.png -i !SOUND_FILE! -r 30 -c:v libx264 -preset medium -tune stillimage -b:a 192k -pix_fmt yuv420p -shortest !OUTPUT_FILE!
)

endlocal
pause

::快速压制
::ffmpeg -i 3.2.mp4 -preset veryfast -vf "scale=500:720,pad=1280:720:360:0:black" -af "volume=2" output/3.2.mp4

::m2v转换
::ffmpeg -i ./monitor_005_40534656.m2v -c:v libx264 -c:a aac -map 0:v:0  output.mp4
