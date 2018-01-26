# download the monthly OFAC Files
import requests
import datetime

CONFIG = 'url_config.config'
UNC = '\\\\csgimp22.prodnet.dom\\USA_LOAD\\CURRENT\\OFAC'


def download_file(url):
    now = datetime.datetime.now()
    now = now.strftime('%m-%d-%y')

    # generate the local filename
    local_filename = url.split('/')[-1]
    local_filename = now + '_' + local_filename

    outpath = UNC + '\\' + local_filename

    try:
        r = requests.get(url, stream=True)
        with open(outpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except requests.exceptions.RequestException:
        print('unable to connect to', url)
    else:
        f.close()
    return local_filename


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
            log_list.append(file)
        for name in log_list:
            log.write(name.strip(',').strip() + '\n')

        log.close()


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
            print('connecting to', url)
            f = download_file(url.strip())
            print(f, 'downloaded')
            print('---------------------')
            if collect == '':
                collect += f
            else:
                collect += ', ' + f
        log_file(collect)
        print('Closing Connection.')


main()
