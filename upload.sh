#cd ..
#chmod 777 upload.sh
chmod +x upload.sh
echo $1
ffmpeg -i $1.mov -vcodec h264 -acodec mp2 $1.mp4
ffmpeg -i $1.mp4 -ss 00:00:02.150 -vframes 1 -q:v 2 $1.jpg

python3 refactor.py --file="$1.mp4" --metadataFile="$2"