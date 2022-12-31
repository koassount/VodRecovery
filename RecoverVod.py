import datetime
import hashlib
import os
import random
from datetime import timedelta
import grequests
import requests
from bs4 import BeautifulSoup
from moviepy.editor import concatenate_videoclips, VideoFileClip
from natsort import natsorted

domains = ["https://vod-secure.twitch.tv/",
           "https://vod-metro.twitch.tv/",
           "https://vod-pop-secure.twitch.tv/",
           "https://d2e2de1etea730.cloudfront.net/",
           "https://dqrpb9wgowsf5.cloudfront.net/",
           "https://ds0h3roq6wcgc.cloudfront.net/",
           "https://d2nvs31859zcd8.cloudfront.net/",
           "https://d2aba1wr3818hz.cloudfront.net/",
           "https://d3c27h4odz752x.cloudfront.net/",
           "https://dgeft87wbj63p.cloudfront.net/",
           "https://d1m7jfoe9zdc1j.cloudfront.net/",
           "https://d3vd9lfkzbru3h.cloudfront.net/",
           "https://d2vjef5jvl6bfs.cloudfront.net/",
           "https://d1ymi26ma8va5x.cloudfront.net/",
           "https://d1mhjrowxxagfy.cloudfront.net/",
           "https://ddacn6pr5v0tl.cloudfront.net/",
           "https://d3aqoihi2n8ty8.cloudfront.net/"]

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.5; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Linux i686; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.5; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.77",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edg/103.0.1264.77",
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36']


def return_main_menu():
    print("WELCOME TO VOD RECOVERY" + "\n")
    menu = "1) Recover Vod" + "\n" + "2) Recover Clips" + "\n" + "3) Unmute an M3U8 file" + "\n" + "4) Check M3U8 Segments" + "\n" + "5) Download M3U8 (.MP4 extension)" + "\n" + "6) Exit" "\n"
    print(menu)


def get_default_directory():
    return os.path.expanduser("~\\Documents\\")


def generate_log_filename(streamer, vod_id):
    log_filename = os.path.join(get_default_directory(), streamer + "_" + vod_id + "_log.txt")
    return log_filename


def generate_vod_filename(streamer, vod_id):
    vod_filename = os.path.join(get_default_directory(), "VodRecovery_" + streamer + "_" + vod_id + ".m3u8")
    return vod_filename


def generate_website_links(streamer, vod_id):
    website_list = ["https://sullygnome.com/channel/" + streamer + "/stream/" + vod_id,
                    "https://twitchtracker.com/" + streamer + "/streams/" + vod_id,
                    "https://streamscharts.com/channels/" + streamer + "/streams/" + vod_id]

    return website_list


def return_header():
    header = {
        'user-agent': f'{random.choice(user_agents)}'
    }
    return header


def remove_file(file_path):
    if os.path.exists(file_path):
        return os.remove(file_path)


def format_timestamp(timestamp):
    formatted_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return formatted_date


def get_vod_age(timestamp):
    vod_age = datetime.datetime.today() - format_timestamp(timestamp)
    if vod_age.days <= 0:
        return 0
    else:
        return vod_age.days


def vod_is_muted(url):
    return bool("unmuted" in requests.get(url).text)


def get_duration(hours, minutes):
    return (int(hours) * 60) + int(minutes)


def get_reps(duration):
    reps = ((duration * 60) + 2000)
    return reps


def get_clip_format(vod_id, reps):
    default_clip_list = ["https://clips-media-assets2.twitch.tv/" + vod_id + "-offset-" + str(i) + ".mp4" for i in
                         range(reps) if i % 2 == 0]

    alternate_clip_list = ["https://clips-media-assets2.twitch.tv/vod-" + vod_id + "-offset-" + str(i) + ".mp4" for i in
                           range(reps) if i % 2 == 0]

    archived_clip_list = [
        "https://clips-media-assets2.twitch.tv/" + vod_id + "-index-" + "%010g" % (int('000000000') + i) + ".mp4" for i
        in range(reps)]

    clip_format_dict = {}

    clip_format_dict.update({"1": default_clip_list})
    clip_format_dict.update({"2": alternate_clip_list})
    clip_format_dict.update({"3": archived_clip_list})

    return clip_format_dict


def get_all_clip_urls(clip_dict, clip_format):
    full_url_list = []
    for key, value in clip_dict.items():
        if key in clip_format:
            full_url_list += value
    return full_url_list


def parse_m3u8_link(url):
    streamer = url.split("_")[1]
    vod_id = url.split("_")[2].split("/")[0]
    return streamer, vod_id


def return_file_contents(streamer, vod_id):
    with open(generate_log_filename(streamer, vod_id)) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    return content


def get_all_urls(streamer, vod_id, timestamp):
    vod_url_list = []
    for seconds in range(60):
        epoch_timestamp = ((format_timestamp(timestamp) + timedelta(seconds=seconds)) - datetime.datetime(1970, 1,
                                                                                                          1)).total_seconds()
        base_url = streamer + "_" + vod_id + "_" + str(int(epoch_timestamp))
        hashed_base_url = str(hashlib.sha1(base_url.encode('utf-8')).hexdigest())[:20]
        for domain in domains:
            vod_url_list.append(domain + hashed_base_url + "_" + base_url + "/chunked/index-dvr.m3u8")
    return vod_url_list


def get_valid_urls(url_list):
    valid_url_list = []
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in url_list]
    for result in grequests.imap(rs, size=100):
        if result.status_code == 200:
            valid_url_list.append(result.url)
    return valid_url_list


def parse_datetime_streamscharts(tracker_url):
    for _ in range(10):
        response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, 'html.parser')
            streamscharts_datetime = bs.find_all('time', {'class': 'ml-2 font-bold'})[0].text.strip().replace(",", "") + ":00"
            return datetime.datetime.strftime(datetime.datetime.strptime(streamscharts_datetime, "%d %b %Y %H:%M:%S"), "%Y-%m-%d %H:%M:%S")


def parse_datetime_twitchtracker(tracker_url):
    response = requests.get(tracker_url, headers=return_header(), allow_redirects=False)
    bs = BeautifulSoup(response.content, 'html.parser')
    twitchtracker_datetime = bs.find_all('div', {'class': 'stream-timestamp-dt'})[0].text
    return twitchtracker_datetime


def unmute_vod(url):
    file_contents = []
    counter = 0
    vod_file_path = generate_vod_filename(parse_m3u8_link(url)[0], parse_m3u8_link(url)[1])
    with open(vod_file_path, "w") as vod_file:
        vod_file.write(requests.get(url, stream=True).text)
    vod_file.close()
    with open(vod_file_path, "r") as vod_file:
        for lines in vod_file.readlines():
            file_contents.append(lines)
    vod_file.close()
    with open(vod_file_path, "w") as vod_file:
        for segment in file_contents:
            url = url.replace("index-dvr.m3u8", "")
            if "-unmuted" in segment and not segment.startswith("#"):
                counter += 1
                vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + "-muted.ts" + "\n")
            elif "-unmuted" not in segment and not segment.startswith("#"):
                counter += 1
                vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + ".ts" + "\n")
            else:
                vod_file.write(segment)
    vod_file.close()
    print(os.path.basename(vod_file_path) + " Has been unmuted. File can be found in " + vod_file_path)


def get_segments(url):
    counter = 0
    file_contents, segment_list = [], []
    vod_file_path = generate_vod_filename(parse_m3u8_link(url)[0], parse_m3u8_link(url)[1])
    if os.path.exists(vod_file_path):
        with open(vod_file_path, "r+") as vod_file:
            for segment in vod_file.readlines():
                url = url.replace("index-dvr.m3u8", "")
                if "-muted" in segment and not segment.startswith("#"):
                    counter += 1
                    segment_list.append(str(url) + str(counter - 1) + "-muted.ts")
                elif "-muted" not in segment and not segment.startswith("#"):
                    counter += 1
                    segment_list.append(str(url) + str(counter - 1) + ".ts")
                else:
                    pass
        vod_file.close()
    else:
        with open(vod_file_path, "w") as vod_file:
            vod_file.write(requests.get(url, stream=True).text)
        vod_file.close()
        with open(vod_file_path, "r") as vod_file:
            for lines in vod_file.readlines():
                file_contents.append(lines)
        vod_file.close()
        counter = 0
        with open(vod_file_path, "w") as unmuted_vod_file:
            for segment in file_contents:
                url = url.replace("index-dvr.m3u8", "")
                if "-unmuted" in segment and not segment.startswith("#"):
                    counter += 1
                    unmuted_vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + "-muted.ts" + "\n")
                    segment_list.append(str(url) + str(counter - 1) + "-muted.ts")
                elif "-unmuted" not in segment and not segment.startswith("#"):
                    counter += 1
                    unmuted_vod_file.write(segment.replace(segment, str(url) + str(counter - 1)) + ".ts" + "\n")
                    segment_list.append(str(url) + str(counter - 1) + ".ts")
                else:
                    pass
        unmuted_vod_file.close()
    return segment_list


def check_segment_availability(segments):
    valid_segment_counter = 0
    all_segments = []
    valid_segments = []
    for url in segments:
        all_segments.append(url.strip())
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in all_segments]
    for result in grequests.imap(rs, size=100):
        if result.status_code == 200:
            valid_segment_counter += 1
            valid_segments.append(result.url)
    return valid_segments

def vod_recover(streamer, vod_id, timestamp):
    print("Vod is " + str(
        get_vod_age(timestamp)) + " days old. If the vod is older than 60 days chances of recovery are slim." + "\n")
    url_list = get_valid_urls(get_all_urls(streamer, vod_id, timestamp))
    if len(url_list) > 0:
        if vod_is_muted(url_list[0]):
            print(url_list[0] + "\n" + "Vod contains muted segments")
            user_input = input("Would you like to unmute the vod (Y/N): ")
            if user_input.upper() == "Y":
                unmute_vod(url_list[0])
                print("Total Number of Segments: " + str(len(get_segments(url_list[0]))))
                user_option = input("Would you like to check if segments are valid (Y/N): ")
                if user_option.upper() == "Y":
                    print(str(len(check_segment_availability(get_segments(url_list[0])))) + " of " + str(
                        len(get_segments(url_list[0]))) + " Segments are valid")
                else:
                    return
            else:
                return
        else:
            print(url_list[0] + "\n" + "Vod does NOT contain muted segments")
    else:
        print(
            "No vods found using current domain list. " + "\n" + "See the following links if you would like to check the other sites: " + "\n")
        for website in generate_website_links(streamer, vod_id):
            print(website)


def manual_vod_recover():
    streamer_name = input("Enter streamer name: ")
    vod_id = input("Enter vod id: ")
    timestamp = input("Enter VOD start time (YYYY-MM-DD HH:MM:SS): ")
    vod_recover(streamer_name, vod_id, timestamp)


def website_vod_recover():
    tracker_url = input("Enter twitchtracker/streamscharts url:  ")
    if "streamscharts" in tracker_url:
        streamer = tracker_url.split("channels/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("streams/", 1)[1]
        vod_recover(streamer, vod_id, parse_datetime_streamscharts(tracker_url))
    elif "twitchtracker" in tracker_url:
        streamer = tracker_url.split("com/", 1)[1].split("/")[0]
        vod_id = tracker_url.split("streams/", 1)[1]
        vod_recover(streamer, vod_id, parse_datetime_twitchtracker(tracker_url))
    else:
        print("Link not supported.. Returning to main menu.")
        return

def bulk_vod_recovery():
    streamer_name = input("Enter streamer name: ")
    file_path = input("Enter full path of sullygnome CSV file: ").replace('"', '')
    for timestamp, vodID in parse_vod_csv_file(file_path).items():
        print("\n" + "Recovering Vod....", vodID)
        url_list = get_valid_urls(get_all_urls(streamer_name, vodID, timestamp))
        if len(url_list) > 0:
            if vod_is_muted(url_list[0]):
                print(url_list[0])
                print("Vod contains muted segments")
            else:
                print(url_list[0])
                print("Vod does NOT contain muted segments")
        else:
            print("No vods found using current domain list." + "\n")


def recover_all_clips():
    total_counter, iteration_counter, valid_counter = 0, 0, 0
    valid_url_list = []
    streamer = input("Enter streamer name: ")
    vod_id = input("Enter vod id: ")
    hours = input("Enter stream duration hour value: ")
    minutes = input("Enter stream duration minute value: ")
    clip_format = input("What clip url format would you like to use (IF multiple.. separate by spaces)? " + "\n" + "1) Default (Most vods)" + "\n" + "2) Alternate (2017 and up)" + "\n" + "3) Archived (June-August of 2016)" + "\n").split()
    full_url_list = get_all_clip_urls(get_clip_format(vod_id, get_reps(get_duration(hours, minutes))), clip_format)
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in full_url_list]
    for result in grequests.imap(rs, size=100):
        total_counter += 1
        iteration_counter += 1
        if total_counter == 500:
            print(str(iteration_counter) + " of " + str(len(full_url_list)))
            total_counter = 0
        if result.status_code == 200:
            valid_counter += 1
            valid_url_list.append(result.url)
            print(str(valid_counter) + " Clip(s) Found")
    if len(valid_url_list) >= 1:
        user_option = input("Do you want to log results to file (Y/N): ")
        if user_option.upper() == "Y":
            with open(generate_log_filename(streamer, vod_id), "w") as log_file:
                for url in valid_url_list:
                    log_file.write(url + "\n")
            log_file.close()
            user_option = input("Do you want to download the recovered clips (Y/N): ")
            if user_option.upper() == "Y":
                download_clips(get_default_directory(), streamer, vod_id)
            else:
                return
        else:
            return
    else:
        print("No clips found! Returning to main menu.")
        return


def parse_clip_csv_file(file_path):
    vod_info_dict = {}
    csv_file = open(file_path, "r+")
    lines = csv_file.readlines()[1:]
    for line in lines:
        if line.strip():
            filtered_string = line.partition("stream/")[2].replace('"', "")
            vod_id = filtered_string.split(",")[0]
            duration = filtered_string.split(",")[1]
            if vod_id != 0:
                reps = get_reps(int(duration))
                vod_info_dict.update({vod_id: reps})
            else:
                pass
    csv_file.close()
    return vod_info_dict


def parse_vod_csv_file(file_path):
    vod_info_dict = {}
    csv_file = open(file_path, "r+")
    lines = csv_file.readlines()[1:]
    for line in lines:
        if line.strip():
            if len(line.split(",")[1].split(" ")[1]) > 3:
                day = line.split(",")[1].split(" ")[1][:2]
            else:
                day = line.split(",")[1].split(" ")[1][:1]
            month = line.split(",")[1].split(" ")[2]
            year = line.split(",")[1].split(" ")[3]
            timestamp = line.split(",")[1].split(" ")[4]
            stream_datetime = day + " " + month + " " + year + " " + timestamp
            vod_id = line.partition("stream/")[2].split(",")[0].replace('"', "")
            stream_date = datetime.datetime.strftime(
                datetime.datetime.strptime(stream_datetime.strip().replace('"', "") + ":00", "%d %B %Y %H:%M:%S"),
                "%Y-%m-%d %H:%M:%S")
            vod_info_dict.update({stream_date: vod_id})
    csv_file.close()
    return vod_info_dict


def get_random_clips():
    counter = 0
    vod_id = input("Enter vod id: ")
    hours = input("Enter stream duration hour value: ")
    minutes = input("Enter stream duration minute value: ")
    clip_format = input("What clip url format would you like to use (IF multiple.. separate by spaces)? " + "\n" + "1) Default (Most vods)" + "\n" + "2) Alternate (2017 and up)" + "\n" + "3) Archived (June-August of 2016)" + "\n").split()
    full_url_list = get_all_clip_urls(get_clip_format(vod_id, get_reps(get_duration(hours, minutes))), clip_format)
    random.shuffle(full_url_list)
    print("Total Number of Urls: " + str(len(full_url_list)))
    request_session = requests.Session()
    rs = [grequests.head(u, session=request_session) for u in full_url_list]
    for result in grequests.imap(rs, size=100):
        if result.status_code == 200:
            counter += 1
            if counter == 1:
                print(result.url)
                user_option = input("Do you want another url (Y/N): ")
                if user_option.upper() == "Y":
                    continue
                else:
                    return
        counter = 0


def bulk_clip_recovery():
    vod_counter, total_counter, valid_counter, iteration_counter = 0, 0, 0, 0
    streamer = input("Enter streamer name: ")
    file_path = input("Enter full path of sullygnome CSV file: ").replace('"', '')
    user_option = input("Do you want to download all clips recovered (Y/N)? ")
    clip_format = input("What clip url format would you like to use (IF multiple.. separate by spaces)? " + "\n" + "1) Default (Most vods)" + "\n" + "2) Alternate (2017 and up)" + "\n" + "3) Archived (June-August of 2016)" + "\n").split()
    for vod, duration in parse_clip_csv_file(file_path).items():
        vod_counter += 1
        print("Processing Twitch Vod... " + str(vod) + " - " + str(vod_counter) + " of " + str(
            len(parse_clip_csv_file(file_path))))
        original_vod_url_list = get_all_clip_urls(get_clip_format(vod, duration), clip_format)
        request_session = requests.Session()
        rs = [grequests.head(u, session=request_session) for u in original_vod_url_list]
        for result in grequests.imap(rs, size=100):
            total_counter += 1
            iteration_counter += 1
            if total_counter == 500:
                print(str(iteration_counter) + " of " + str(len(original_vod_url_list)))
                total_counter = 0
            if result.status_code == 200:
                valid_counter += 1
                print(str(valid_counter) + " Clip(s) Found")
                with open(generate_log_filename(streamer, vod), "a+") as log_file:
                    log_file.write(result.url + "\n")
                log_file.close()
            else:
                continue
        if valid_counter != 0:
            if user_option.upper() == "Y":
                download_clips(get_default_directory(), streamer, vod)
            else:
                print("Recovered clips logged to " + generate_log_filename(streamer, vod))
        total_counter, valid_counter, iteration_counter = 0, 0, 0


def download_m3u8(url):
    videos = []
    ts_video_list = natsorted(check_segment_availability(get_segments(url)))
    for ts_files in ts_video_list:
        print("Processing.... " + ts_files)
        if ts_files.endswith(".ts"):
            video = VideoFileClip(ts_files)
            videos.append(video)
    final_vod_output = concatenate_videoclips(videos)
    final_vod_output.to_videofile(os.path.join(get_default_directory(), parse_m3u8_link(url)[0] + "_" + parse_m3u8_link(url)[1] + ".mp4"), fps=60, remove_temp=True)


def download_clips(directory, streamer, vod_id):
    counter = 0
    print("Starting Download....")
    download_directory = os.path.join(directory, streamer.title() + "_" + vod_id)
    if os.path.exists(download_directory):
        pass
    else:
        os.mkdir(download_directory)
    for links in return_file_contents(streamer, vod_id):
        counter = counter + 1
        if "-offset-" in links:
            clip_offset = links.split("-offset-")[1].replace(".mp4", "")
        else:
            clip_offset = links.split("-index-")[1].replace(".mp4", "")
        link_url = os.path.basename(links)
        r = requests.get(links, stream=True)
        if r.status_code == 200:
            if str(link_url).endswith(".mp4"):
                with open(os.path.join(download_directory, streamer.title() + "_" + str(vod_id) + "_" + str(
                        clip_offset)) + ".mp4", 'wb') as x:
                    print(datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S    ") + "Downloading... Clip " + str(
                        counter) + " of " + str(len(return_file_contents(streamer, vod_id))) + " - " + links)
                    x.write(r.content)
            else:
                print("ERROR: Please check the log file and failing link!", links)
        else:
            print("ERROR: " + str(r.status_code) + " - " + str(r.reason))
            pass


def run_script():
    menu = 0
    while menu < 6:
        return_main_menu()
        menu = int(input("Please choose an option: "))
        if menu == 6:
            exit()
        elif menu == 1:
            vod_type = int(input(
                "Enter what type of vod recovery: " + "\n" + "1) Recover Vod" + "\n" + "2) Recover vods from SullyGnome CSV export" + "\n"))
            if vod_type == 1:
                recovery_method = input("Enter vod recovery method: " + "\n" + "1) Manual Recover" + "\n" + "2) Website Recover" + "\n")
                if recovery_method == "1":
                    manual_vod_recover()
                elif recovery_method == "2":
                    website_vod_recover()
                else:
                    print("Invalid option returning to main menu.")
            elif vod_type == 2:
                bulk_vod_recovery()
            else:
                print("Invalid option! Returning to main menu.")
        elif menu == 2:
            clip_type = int(input(
                "Enter what type of clip recovery: " + "\n" + "1) Recover all clips from a single VOD" + "\n" + "2) Find random clips from a single VOD" + "\n" + "3) Bulk recover clips from SullyGnome CSV export" + "\n"))
            if clip_type == 1:
                recover_all_clips()
            elif clip_type == 2:
                get_random_clips()
            elif clip_type == 3:
                bulk_clip_recovery()
            else:
                print("Invalid option! Returning to main menu.")
        elif menu == 3:
            url = input("Enter M3U8 Link: ")
            if vod_is_muted(url):
                unmute_vod(url)
            else:
                print("Vod does NOT contain muted segments")
        elif menu == 4:
            url = input("Enter M3U8 Link: ")
            print(str(len(check_segment_availability(get_segments(url)))) + " of " + str(
                len(get_segments(url))) + " Segments are valid")
            remove_file(generate_vod_filename(parse_m3u8_link(url)[0], parse_m3u8_link(url)[1]))
        elif menu == 5:
            url = input("Enter M3U8 Link: ")
            download_m3u8(url)
        else:
            print("Invalid Option! Exiting...")


run_script()
