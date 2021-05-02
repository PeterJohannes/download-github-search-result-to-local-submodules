import os
import json
from html.parser import HTMLParser
import urllib.request

YELLOW = '\033[93m'
END_COLOR = '\033[0m'

class LinkScrape(HTMLParser):

    def split_url(self, url):
        print(f"#x8832 url '{url}'")
        # url_data = url.strip("https://github.com/")

        url_data = url.replace("https://github.com/", "")
        print(f"#x8833 url_data for split '{url_data}'")
        x = url_data.split("/")
        print(f"#x8834 result '{x[0]}' and '{x[1]}'")

        return x[0], x[1]

    def submodule_add(self, url):
        owner, repository = self.split_url(url)
        new_submodule = f"gh_{owner}_{repository}"

        print(f"\n{url}  from {YELLOW}{owner}{END_COLOR}  repository {YELLOW}{repository}{END_COLOR}  => submodule {YELLOW}{new_submodule}{END_COLOR}")
        command = f"git submodule add {url} {new_submodule}"
        os.system(command)


    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                url = False
                if 'data-hydro-click' in attr:
                    f1, f2 = attr
                    f2_json = json.loads(f2)
                    try:
                        url = f2_json['payload']['result']['url']
                    except:
                        pass
                    if url:
                        print(f"#x7763 url is {url}")
                        self.submodule_add(url)

            
if __name__ == '__main__':

    initialisation = input('create new git repository in this folder [N/y] > ')

    if initialisation == "Y" or  initialisation == "y": 
        command = f"git init"
        os.system(f"{command}")
    
    while True:
        url = input('\nenter the githuab url for scanning or blank for end process > ')

        if url == "":
            break
        request_object = urllib.request.Request(url)
        page_object = urllib.request.urlopen(request_object)
        link_parser = LinkScrape()
        link_parser.feed(page_object.read().decode('utf-8'))