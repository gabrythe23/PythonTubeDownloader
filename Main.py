import youtube_dl
import urllib
import sys
import os
import ffmpy

def GetYoutubeUrl() :
    options = {
    'ignoreerrors': True,
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': "mp3",
}
    ydl = youtube_dl.YoutubeDL(options)
    val = raw_input("Youtube URL/Playlist: ")
    try:
        with ydl:
            result = ydl.extract_info(
                val,
                download=False
            )
    except Exception as err:
        sys.exit()
    if 'entries' in result:
        video = [result['entries'], result['title']]
    else:
        video = [result]
    return video

def DoDownload(youtubevid, title) :
    title = title.encode('utf-8')
    videotitle = youtubevid['title'].encode('utf-8')
    videourl = youtubevid['url']
    print("Downloading " + videotitle + ". Please Wait! :)")
    createpath = "./Downloads/"
    if title != "":
        createpath += title + "/"
    if not os.path.exists(createpath): 
        os.makedirs(createpath)
    filestr = createpath + videotitle + ".mp3"
    if os._exists(filestr):
        print("File already exists! :(")
        return
    dl = ffmpy.FFmpeg(
        global_options={
            '-hide_banner': None,
            '-loglevel panic': None
            },
        inputs={videourl: None},
        outputs={filestr: None}
    )
    dl.run()

def Main() :
    youtubevids = GetYoutubeUrl()
    playlisttitle = ""
    if(len(youtubevids) > 1):
        playlisttitle = youtubevids[1]
        for vid in youtubevids[0] :
            DoDownload(vid,playlisttitle)
    else:
        for vid in youtubevids :
            DoDownload(vid,playlisttitle)
    print("Download has completed, check the 'Downloads' Folder in the current directory.")
    while True:
        val = raw_input("Would you like to download more? [Y/N] ").lower()
        if val == "y":
            Main()
        if val == "n":
            sys.exit()
            break

Main()
