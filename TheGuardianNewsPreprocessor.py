from collections import deque
from datetime import date, timedelta
import os
import json
import logging
from html.parser import HTMLParser

directory_root = '/Users/gpanez/Documents/news/the_guardian'
directory_preprocessed_output = '/Users/gpanez/Documents/news/the_guardian_preprocessed'


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def handle_endtag(self, tag):
        if tag == 'p':
            self.fed.append('\n')

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def process_items():
    start = date(2000, 1, 1)
    end = date(2018, 12, 31)

    current = start
    delta = timedelta(days=1)
    while current <= end:
        directory = directory_root + '/' + current.isoformat()
        if not os.path.exists(directory):
            print('Directory does not exist: ', directory)
        else:
            for file_name in os.listdir(directory):
                with open(directory + '/' + file_name) as file:
                    data = json.load(file)
                    header = ''
                    header += data['webPublicationDate'] + '\n'
                    header += "#####\n"
                    header += data['id'] + '\n'
                    header += "#####\n"
                    header += data['webUrl'] + '\n'
                    header += "#####\n"
                    header += data['webTitle'] + '\n'
                    header += "#####\n"
                    body = data['body']
                    body_text = strip_tags(body)
                    directory_output = directory_preprocessed_output + '/' + current.isoformat()
                    if not os.path.exists(directory_output):  # or not os.path.isdir(directory):
                        logging.debug('Creating directory: [%s]', directory_root)
                        os.makedirs(directory_output)

                    with open(directory_output + '/' + file_name, "w") as file_out:
                        file_out.write(header + body_text)


                    #print('hola')
                    # tags = re.findall('<[a-zA-Z]+', body)
                    # for tag in tags:
                    #     tag_exists = tags_summary.get(tag)
                    #     if tag_exists is None:
                    #         tags_summary[tag] = 1
                    #     else:
                    #         tags_summary[tag] += 1
        current = current + delta
    print("done")


def main():
    logging.basicConfig(filename=directory_preprocessed_output + '/log.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    logging.info("The Guardian News Preprocessor")
    logging.getLogger('TGNP')
    process_items()
    # TODO: Added timing thresholds but need to add limit per day
    # TODO: Added timing thresholds but need to add saving the queue
    # TODO: Need to add cron job, and overall begin and end


if __name__ == "__main__":
    main()
    print("done")