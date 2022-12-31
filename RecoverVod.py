from datetime import timedelta
import datetime
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor
import requests
import os

"""
* Created By: ItIckeYd 
* Purpose: The following script retrieves the m3u8 to sub-only and deleted twitch videos.
* Date: May 3rd, 2022
*
* Versions:
*
* 1.0 - Initial Release - May 3rd, 2022
* 1.1 - Renamed variables, refactored code to implement methods, added conditionals.
* 1.2 - Refactored date check and added a main.
* 1.3 - Refactored code to retrieve the formatted date.
* 1.4 - Refactored retrieving valid links and main.
* 1.5 - Fixed unmuting speed.
"""

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

all_possible_urls = []
valid_url_list = []
list_of_lines = []


streamer_name = input("Enter streamer name: ").strip()
vodID = input("Enter vod id: ").strip()
timestamp = input("Enter VOD timestamp (YYYY-MM-DD HH:MM:SS): ").strip()

def get_url(url):
    return requests.get(url, timeout=100)

def format_timestamp(vod_datetime):
    formatted_date = datetime.datetime.strptime(vod_datetime, "%Y-%m-%d %H:%M:%S")
    return formatted_date

def get_default_directory():
    default_directory = os.path.expanduser("~\\Documents\\")
    return default_directory

def generate_unmuted_filename():
    unmuted_file_name = get_default_directory()+"VodRecovery_" + vodID + ".m3u8"
    return unmuted_file_name

def get_vod_age():
    bool_vod_expired = False
    days_between = datetime.datetime.today() - format_timestamp(timestamp)
    return days_between.days

def is_vod_date_greater_60():
    bool_vod_expired = False
    days_between = datetime.datetime.today() - format_timestamp(timestamp)
    if days_between > timedelta(days=60):
        bool_vod_expired = True
    else:
        bool_vod_expired = False
    return bool_vod_expired

def get_valid_links():
    for bf_second in range(60):
        vod_date = datetime.datetime(format_timestamp(timestamp).year,format_timestamp(timestamp).month,format_timestamp(timestamp).day,format_timestamp(timestamp).hour,format_timestamp(timestamp).minute,bf_second)
        converted_timestamp = round(time.mktime(vod_date.timetuple()))
        base_url = streamer_name + "_" + vodID + "_" + str(int(converted_timestamp))
        hashed_base_url = str(hashlib.sha1(base_url.encode('utf-8')).hexdigest())[:20]
        formatted_base_url = hashed_base_url + '_' +  base_url
        for domain in domains:
            url = domain+formatted_base_url+"/chunked/index-dvr.m3u8"
            all_possible_urls.append(url)
    with ThreadPoolExecutor(max_workers=100) as pool:
        max_url_list_length = 100
        current_list = all_possible_urls
        for i in range(0, len(current_list), max_url_list_length):
            batch = current_list[i:i + max_url_list_length]
            response_list = list(pool.map(get_url, batch))
            for m3u8_url in response_list:
                if m3u8_url.status_code == 200:
                    valid_url_list.append(m3u8_url.url)
        for valid_url in valid_url_list:
            print(valid_url)
    return valid_url_list


def bool_is_muted():
    is_muted = False
    vod_response = get_url(valid_url_list[0])
    if "-unmuted" not in vod_response.text:
        is_muted = False
    else:
        is_muted = True
    return is_muted

def unmute_vod():
    link_response = get_url(valid_url_list[0])
    temp_file = open(generate_unmuted_filename(), "w")
    temp_file.write(link_response.text)
    temp_file.close()
    with open(generate_unmuted_filename(), "r") as append_file:
        for line in append_file.readlines():
            list_of_lines.append(line)
    append_file.close()
    counter = 0
    with open(generate_unmuted_filename(), "w") as file:
        for segment in list_of_lines:
            url = link_response.url.replace("index-dvr.m3u8", "")
            if "-unmuted" in segment and not segment.startswith("#"):
                counter += 1
                file.write(
                    segment.replace(segment, str(url) + str(counter - 1)) + "-muted.ts" + "\n")
            elif "-unmuted" not in segment and not segment.startswith("#"):
                counter += 1
                file.write(segment.replace(segment, str(url) + str(counter - 1)) + ".ts" + "\n")
            else:
                 file.write(segment)
    file.close()
    print(os.path.basename(generate_unmuted_filename())+" Has been unmuted. File can be found in " + generate_unmuted_filename())

def recover_vod():
    if get_valid_links():
        if bool_is_muted:
            print("Vod contains muted segments")
            bool_unmute_vod = input("Would you like to unmute the vod (Y/N): ")
            if bool_unmute_vod.upper() == "Y":
                unmute_vod()
        else:
            print("Vod does NOT contain muted segments")
    else:
        print("No vods found using current domain list.")


if not is_vod_date_greater_60():
    recover_vod()
else:
    print("Vod is " + str(get_vod_age()) + " days old. Vods typically cannot be recovered when older then 60 days.")
    user_continue = input("Do you want to continue (Y/N): ")
    if user_continue.upper() == "Y":
        recover_vod()
    else:
        exit()

