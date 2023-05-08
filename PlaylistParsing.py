from dotenv import load_dotenv
import os
import base64
from requests import post,get 
import json
from csv import writer,reader
import re
from SoundDownloader import initiation,SearchnDownload

#load some constants from evironment file
load_dotenv()

#CSV file name and location
csv = "Pre_Refined_list.csv"                      #The CSV is for debug option and other development in the future
absolute_path = os.path.dirname(__file__)
out_csv = os.path.join(absolute_path, csv)

#Getting environment constants
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#Follow Spotify instruction to acquire acess token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url ='https://accounts.spotify.com/api/token'
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url,headers=headers,data=data)
    print(result.status_code)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Create Authorization header for requesting get 
def get_auth_header(token):
    return {"Authorization" : "Bearer "+ token}

#Get tracks (name,URL) to the CSV file in the playlist - return the next url (if there are still more tracks, return NONE if there are none)
def get_playlist_tracks(token, url):
    headers = get_auth_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)
    next = json_result['next']
    Items = json_result['items']
    TracksInfo = []
    for item in Items:
        TracksInfo.append((item['track']['name'],item['track']['external_urls']['spotify']))
        # TracksInfo.append(item['track']['external_urls']['spotify'])  #Debuging lines
        # print(TracksInfo)
    return (next,TracksInfo)

#CSV writing function for debugging and other future developments
def CSVWriter(List: list):
    with open(out_csv,"a",encoding="utf-8",newline='') as f_object: 
            writer_object = writer(f_object)    #Initiate the write tool
            for item in List:
                writer_object.writerow(item)        #Write the line  

#Check the available track in local folder
def LocalList(FolderPath: os.pardir):
    List = []
    for filename in os.listdir(FolderPath):
        Title = re.search(' - (.+?).mp3',filename)
        List.append(Title.group(1))
        # print(Title.group(1))
    print(len(List))
    return List

#Refine the track list after comparing to the local folder
def RefineList(LocalList: list,ParsedList: list):
    Local = set(LocalList)
    RefinedList = []
    List = [i for i, item in enumerate(ParsedList) if (item[0] not in Local)]
    print(len(List))
    for i in List:
        RefinedList.append(ParsedList[i])
    # for i in RefinedList:
    #     print(i)
    return RefinedList

#Main download Loop - consequently find the song in the list then initiate download - Each loop will open 10 tabs
def downloadLoop(TrackList: list):
        K = True
        while(K):
            print(f"There are total {len(TrackList)} tracks in the playlist ...\n Press any key to start download ...")
            input() 
            print("Initiating ....")
            DWLDList = [] 
            wait,BRWS = initiation()
            if (len(TrackList)<=10):
                Loop = len(TrackList)
            else:
                Loop = 10
            for i in range(Loop):
                print(f"Start download ...{TrackList[i][0]}")
                link = TrackList[i][1]
                SearchnDownload(wait,BRWS,link,i+1)
                DWLDList.append(TrackList[i])
            BRWS.close()
            print("Please wait for all dowload to be completed.\nPress any key to confirm")
            input()
            print("Downloaded...\n")
            for i in range(len(DWLDList)):
                print(DWLDList[i][0])
            TrackList = list(set(TrackList) - set(DWLDList))
            print(f"\nThere are {len(TrackList)} left in Playlist ")
            input()
            if len(TrackList) == 0:
                break
            BRWS.quit()
            print("Please check if close the current browser already quited before continue ... ")
            input()
            print("Continue to download ? press (y) to continue")
            confirm = input()
            if confirm != 'y':
                K = False
        input()

def main():
    token = get_token()
    print('Input playlist link: ... ')
    PlaylistLink = input()
    m = re.search('playlist/(.+?)?si=',PlaylistLink)
    if m:
        PlaylistID = m.group(1)
        PlaylistID = PlaylistID[:-1]
    url = f"https://api.spotify.com/v1/playlists/{PlaylistID}/tracks"
    TrackList = []
    NextList = []
    (nexturl,TrackList) = get_playlist_tracks(token, url)
    while(nexturl):
        (nexturl,NextList) = get_playlist_tracks(token, nexturl)
        for track in NextList:
            TrackList.append(track)
        NextList = []
    print(len(TrackList))
    print("Giving the current Mp3 folder:")
    FolderPath = input()
    CurrentList = LocalList(FolderPath)
    Refined = RefineList(CurrentList,TrackList)
    downloadLoop(Refined)

    
if __name__ == "__main__":
    main()
