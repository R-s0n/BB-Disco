import requests, argparse, subprocess
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

class HackerOne:
    def __init__(self, mrp=None):
        self.url = "https://hackerone.com/directory/programs"
        self.class_ = "daisy-link--major"
        self.platform = "HackerOne"
        self.mrp = mrp
        self.link = f"https://hackerone.com/{mrp}"

class MostRecentPrograms:
    def __init__(self, hackerone, bugcrowd, intigriti):
        self.hackerone = hackerone
        self.bugcrowd = bugcrowd
        self.intigriti = intigriti

def get_most_recent_program_obj(program):
    try:
        get_content = subprocess.run([f'node bbdisco.js {program.url}'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
        content = get_content.stdout
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.findAll('a', program.class_)
        return links[0]
    except Exception as e:
        print("[!] Something went wrong!  Skipping this round...")
        return False

def send_init_notification():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    home_dir = get_home_dir.stdout.replace("\n", "")
    message_json = {'text':':bulb::bulb:  Bug Bounty Program Monitoring Server Online!  :bulb::bulb:','username':'BB-Disco','icon_emoji':':bug:'}
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    requests.post(f'{token}', json=message_json)

def send_slack_notification(program):
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    home_dir = get_home_dir.stdout.replace("\n", "")
    message_json = {'text':f':fire::fire:  There is a new program on {program.platform}!  Title: *{program.mrp}*  |  Link: {program.link}  :fire::fire:','username':'HackerOne','icon_emoji':':bug:'}
    print(message_json)
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    print(f"[+] New Program Found!  Name: {program.mrp}")
    # requests.post(f'{token}', json=message_json)

def hackerone_check(mrps):
    program = HackerOne(mrps.hackerone)
    mrpo = get_most_recent_program_obj(program)
    mrp = mrpo.text
    if mrp != mrps.hackerone:
        print(f"[!] New HackerOne Program Found!  {mrp}")
        new_program = HackerOne(mrp)
        send_slack_notification(new_program)
        mrps.hackerone = mrp
        return mrps
    else:
        now = datetime.now()
        formatted_now = now.strftime("%m/%d/%Y, %H:%M:%S")
        print(f"[-] Same -- {mrp} -- {formatted_now}")
        return mrps

def get_init_programs():
    hackerone = HackerOne()
    mrpo = get_most_recent_program_obj(hackerone)
    mrp = mrpo.text
    print(f"[-] HackerOne -- Initial Program -- {mrp}")
    send_init_notification()
    return MostRecentPrograms(mrp, "", "")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=False)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=False)
    return parser.parse_args()

def main(args):
    mrps = get_init_programs()
    while True:
        mrps = hackerone_check(mrps)
        sleep(10)

if __name__ == "__main__":
    args = arg_parse()
    main(args)