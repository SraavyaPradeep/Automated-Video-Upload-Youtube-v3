import sys
import argparse
import httplib2
import os
import random
import time
import http.client

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload

credentials_file = "admin.json" # INCLUDE CREDENTIALS FILE HERE
valid_privacy_status = ("public", "private", "unlisted")
chunksize = -1
resumability = True
body={
  "snippet": {
    "title": "Unamed",
    "description": "No Description.",
    "categoryId": "22",
    "thumbnails": {
      "default": {
        "url": "",
        "height": 1280,
        "width": 720
      },
      "high": {
        "url": "",
        "height": 1280,
        "width": 720
      },
      "maxres": {
        "url": "",
        "height": 1280,
        "width": 720
      },
      "standard": {
        "url": "",
        "height": 1280,
        "width": 720
      },
      "medium": {
        "url": "",
        "height": 1280,
        "width": 720
      }
    }, 
    "tags" : []
  },
  "status": {
    "privacyStatus": "private",
    "madeForKids": False,
    "selfDeclaredMadeForKids": False
  }
}

def authentication():
  clientFlow = None
  try:
    clientFlow = flow_from_clientsecrets(credentials_file, scope = "https://www.googleapis.com/auth/youtube.upload")
  except:
    print("Unable to establish OAuth Credentials.")

  if clientFlow is not None:
    oauthFile = Storage("%s_credentials.json" % sys.argv[0][0:-3])
    oauthFile._create_file_if_needed() # resembles the touch method
    checkingCred = oauthFile.get()
    creds = oauthFile.get()

    if checkingCred == None or checkingCred.invalid == True:
      creds = run_flow(clientFlow, oauthFile)
    
    auth = httplib2.Http()
    return build("youtube", "v3", http=creds.authorize(auth))
  else:
    return None

def upload(uploadFileData):
  error = None
  waitingOnResponse = None

  while True:
      try:
        print ("Uploading file...")
        _, waitingOnResponse = uploadFileData.next_chunk()
        if (waitingOnResponse != None):
          break
      except HttpError as e:
        raise HttpError("Error:", e.content)
  
  print ("Successfully uploaded the following video:", waitingOnResponse['id'])
  addThumbnail(waitingOnResponse['id'])

def addThumbnail(id):
  try:
    thumbnail = youtube.thumbnails().set(videoId=id, media_body=MediaFileUpload(body["snippet"]["thumbnails"]["default"]["url"]))
    thumbnail.execute()
  except HttpError as e:
    raise HttpError("Error:", e.content)
  print("Thumbnail upload was successful.")

def extractVideoInformation(fileName):
   # getting information about video
  with open(fileName) as f:
    contents = f.read()
  data = contents.split("\n")
  for i in range(len(data)): 
    data[i] = data[i].split(": ")[1]
  data[3] = data[3].split("..")
  data[4] = data[4].split("..")
  data[5] = data[5].split("..")
  data[6] = data[6].split("..")
  data[7] = data[7].split("..")
  data[-1] = data[-1].split(", ")

  body["snippet"]["title"] = data[0]
  body["snippet"]["description"] = data[1]
  body["snippet"]["category"] = int(data[2])
  body["snippet"]["thumbnails"]["default"]["url"] = data[3][0]
  body["snippet"]["thumbnails"]["default"]["height"] = int(data[3][1])
  body["snippet"]["thumbnails"]["default"]["width"] = int(data[3][2])
  body["snippet"]["thumbnails"]["high"]["url"] = data[4][0]
  body["snippet"]["thumbnails"]["high"]["height"] = int(data[4][1])
  body["snippet"]["thumbnails"]["high"]["width"] = int(data[4][2])
  body["snippet"]["thumbnails"]["maxres"]["url"] = data[5][0]
  body["snippet"]["thumbnails"]["maxres"]["height"] = int(data[5][1])
  body["snippet"]["thumbnails"]["maxres"]["width"] = int(data[5][2])
  body["snippet"]["thumbnails"]["standard"]["url"] = data[6][0]
  body["snippet"]["thumbnails"]["standard"]["height"] = int(data[6][1])
  body["snippet"]["thumbnails"]["standard"]["width"] = int(data[6][2])
  body["snippet"]["thumbnails"]["medium"]["url"] = data[7][0]
  body["snippet"]["thumbnails"]["medium"]["height"] = int(data[7][1])
  body["snippet"]["thumbnails"]["medium"]["width"] = int(data[7][2])
  body["status"]["privacyStatus"] = valid_privacy_status[int(data[8])]
  body["status"]["madeForKids"] = bool(data[9])
  body["status"]["selfDeclaredMadeForKids"] = bool(data[10])
  body["snippet"]["tags"] = data[11]

  print ("Reading information.txt Successful")
  
if __name__ == '__main__':
  argparser.add_argument("--file", required=True, help="This file should be the video being uploaded.")
  argparser.add_argument("--metadataFile", required=True, help="This file should include all the properties for your Youtube video.")
  args = argparser.parse_args()

  youtube = authentication()
  print("Authentication Successful")
  extractVideoInformation(args.metadataFile)

  try:
    data = ",".join(body.keys())
    videoData = youtube.videos().insert(
      part=data,
      body=body,
      media_body=MediaFileUpload(args.file, chunksize=chunksize, resumable=resumability)
    )
    upload(videoData)
  except HttpError as e:
    raise("An HTTP error occurred. Status:", e.resp.status, "Content:", e.content)
