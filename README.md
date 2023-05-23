# Automated-Youtube-Video-Upload

Automates the process of converting a .mov file to .mp4, selecting a frame for the thumbnail, and uploading the video to Youtube.

# Getting Started

The python file references the Youtube Data API v3, which requires users to create a new Google Console Project. 

Afterwards:

(1) Enable the Youtube Data API v3

(2) Configure OAuth Screen

(3) Add your email as a Test User

(4) Create credentials for OAuth Client ID, set Application Type as Desktop app

(5) Download the JSON file

(6) Modify the credentials_file variable of refactor.py to include the path to your JSON file

(7) Modify the information.txt file to include your video's information


# Running upload.sh

(1) Install ffmpeg as a command line prompt

(2) Add it to your PATH variable

(3) Run the following command:

````
./upload.sh [FILE NAME] [information.txt]
````

NOTE: [FILE NAME] should not include the file's current extension

**Youtube requires phone number authentication for accounts uploading a thumbnail. 

Disclaimer: This code was written during my internship at TheoryOfStocks. I have been given permission to share this on my personal Github Page. 
