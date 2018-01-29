# download the monthly Files based on values stored in a config file
# urls are stored in config file on per line
# path is stored in the config file with the prefixed with PATH:

import requests
import datetime

CONFIG = 'url_config.config'


# unc filepath defined in config file by defining with PATH:<filepath> ona single line
def get_unc_path():
    try:
        infile = open(CONFIG, 'r')
        data = infile.readlines()
    except FileNotFoundError:
        print('Cannot open config file file')
    else:
        for line in data:
            if line[0:5] == 'PATH:':
                unc = line.strip()
                unc = unc.strip('PATH:')
                unc = unc.strip()
                return unc


# function to download the file using requests
def download_file(url):
    now = datetime.datetime.now()
    now = now.strftime('%m-%d-%y')
    unc = get_unc_path()

    # generate the local filename
    local_filename = url.split('/')[-1]
    local_filename = now + '_' + local_filename

    if str(unc) != '':
        outpath = str(unc) + '\\' + local_filename
    else:
        print('Error extracting PATH value from config file')
        return

    try:
        r = requests.get(url, stream=True)
        with open(outpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            status = 1
    except requests.exceptions.RequestException:
        print('unable to connect to', url)
        status = 0
    else:
        f.close()
    return local_filename, status


# generate a log file for each instance.  The log is appended to
def log_file(file_names):
    # create a list for log file
    log_list = []
    now = datetime.datetime.now()
    now = now.strftime('%m-%d-%y')

    try:
        log = open('url_log.log', 'a')

    except FileNotFoundError:
        print('Cannot open log file')

    else:

        log.write('-------------------' + now + '-------------------\n')
        for file in file_names.split(','):
            if 'PATH:' != file[0:5]:
                log_list.append(file)
        for name in log_list:
            log.write(name.strip(',').strip() + '\n')

        log.close()


# main function to call the file download and call log function
# The PATH: var in the config file will be ignored in this loop
def main():
    collect = ''
    try:
        config_file = open(CONFIG, 'r')
        data = config_file.readlines()
    except FileNotFoundError:
        print('Config File not found')

    else:

        print('Gathering URL parameters')
        for url in data:
            if 'PATH:' not in url:

                print('Connecting to', url)
                f, s = download_file(url.strip())
                if s == 1:
                    print(f, 'Downloaded')
                else:
                    print(f, 'Failed to download')
                print('---------------------')
                if s == 1:
                    f = f + ' downloaded successfully'
                else:
                    f = f + ' download failed'
                if collect == '':
                    collect += f
                else:
                    collect += ', ' + f
                    log_file(collect)
        print('Closing Connection.')


main()
