import os
import subprocess
import PySimpleGUI as sg

POSTS_FILE = 'Posts.txt'
BLACKLIST_FILE = 'blacklist.api'
SAVE_FOLDER = 'saves'

def download_from_url(url):
    try:
        subprocess.run(['wget', url, '-P', SAVE_FOLDER])
        return True
    except:
        return False

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        open(BLACKLIST_FILE, 'a').close()
    
    with open(BLACKLIST_FILE, 'r') as file:
        return file.read().splitlines()

def add_to_blacklist(url):
    with open(BLACKLIST_FILE, 'a') as file:
        file.write(url + '\n')

def main():
    sg.theme('DarkBlue')

    layout = [
        [sg.Text("e621 Downloader", size=(20, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text('Items Left:', size=(15, 1)), sg.Text('0', key='-COUNT-')],
        [sg.ProgressBar(100, orientation='h', size=(35, 20), key='-PROGRESS-')],
        [sg.Output(size=(60, 10), key='-OUTPUT-')],
    ]

    window = sg.Window('e621 Downloader', layout, finalize=True)

    blacklist = load_blacklist()
    items_to_download = []

    with open(POSTS_FILE, 'r') as file:
        items_to_download = file.read().splitlines()

    count = len(items_to_download)

    while count > 0:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            break
        
        window['-COUNT-'].update(count)

        if items_to_download:
            url = items_to_download.pop(0)

            if url in blacklist:
                print(f'Skipping blacklisted URL: {url}')
                count -= 1
                continue

            print(f'Downloading: {url}')

            if download_from_url(url):
                add_to_blacklist(url)
                count -= 1
                window['-PROGRESS-'].update(len(blacklist), len(items_to_download) + len(blacklist))
            else:
                print(f'Error downloading: {url}')

    window.close()

if __name__ == '__main__':
    main()

