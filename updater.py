import os
import requests
import zipfile
import re

SELF_NAME = r'TickerTracker.exe'
ZIP_NAME = r'TickerTracker.zip\b'
VERSION_STRING = r'\d+\.\d+\.\d+'
NONE_VERSION = '0.0.0'
SUBJECT_NAME = fr'TickerTracker-{VERSION_STRING}\.exe\b'
FIND_FILES = [SELF_NAME, ZIP_NAME, SUBJECT_NAME]
REPO_URL = 'https://api.github.com/repos/TKeeney25/Update-From-Github/releases/latest'


def fetch_local_subject_file_name() -> str | None:
    local_file_names = os.listdir('./')
    for file_name in local_file_names:
        if re.match(SUBJECT_NAME, file_name, re.IGNORECASE):
            return file_name
    return None


def fetch_github_content() -> dict:
    json_content = requests.get(REPO_URL).json()
    content = dict()
    for asset in json_content['assets']:
        for file in FIND_FILES:
            if re.match(file, asset['name'], re.IGNORECASE):
                content[file] = (asset['name'], asset['browser_download_url'])
    return content


def fetch_file_version(file_name: str) -> list:
    version = re.match(VERSION_STRING, file_name).group(0)
    return_vals = []
    for val in version.split('.'):
        return_vals.append(val)
    return return_vals


def version_greater_than(arg1: list, arg2: list) -> bool:
    for i in range(len(arg1)):
        val1 = arg1[i]
        val2 = arg2[i]
        if val1 == val2:
            continue
        return val1 > val2
    return False


def download_file(file_name: str, download_link: str):
    request_data = requests.get(download_link)
    with open(f'./{file_name}', 'wb') as new_file:
        new_file.write(request_data.content)


def update():
    subject_file = fetch_local_subject_file_name()
    if subject_file is None:
        subject_file = NONE_VERSION
    github_content = fetch_github_content()
    github_self_file, github_self_download_link = github_content[SELF_NAME]
    github_zip_file, github_zip_download_link = github_content[ZIP_NAME]
    github_subject_file, github_subject_download_link = github_content[SUBJECT_NAME]
    try_delete_old_file(github_self_file)
    if version_greater_than(fetch_file_version(github_subject_file), fetch_file_version(subject_file)):
        download_file(github_subject_file, github_subject_download_link)
        if subject_file != NONE_VERSION:
            os.remove(f'./{subject_file}')
        download_file(github_zip_file, github_zip_download_link)
        unzip(github_zip_file)
        download_file(github_self_file + '1', github_self_download_link)
        cycle_file(github_self_file, github_self_file + '1')
        os.execl('./', github_self_file)


def cycle_file(old_file: str, new_file: str):
    os.rename(f'./{old_file}', f'./{old_file}0')
    os.rename(f'./{new_file}', f'./{old_file}')


def try_delete_old_file(old_file: str):
    try:
        os.remove(f'./{old_file}0')
    except FileNotFoundError:
        pass


def unzip(file_name: str):
    with zipfile.ZipFile(f'./{file_name}', 'r') as zip_ref:
        zip_ref.extractall('./')


if __name__ == '__main__':
    try:
        update()
    except Exception as e:
        print('Error Checking for Update:\n' + repr(e))

    try:
        os.execl('./', fetch_local_subject_file_name())  # system
    except Exception as e:
        print('Error Trying to Run Program:\n' + repr(e))
