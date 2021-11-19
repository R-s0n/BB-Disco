import requests, argparse, subprocess
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

def get_most_recent_program_obj(args):
    get_content = subprocess.run(['node bbdisco.js'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    content = get_content.stdout
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.findAll('a', class_="daisy-link--major")
    print(links[1])
    print(links[2])
    return links[0]

def send_slack_notification(args, program, program_link):
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    home_dir = get_home_dir.stdout.replace("\n", "")
    message_json = {'text':f':fire::fire:  There is a new program on HackerOne!  Title: *{program}*  |  Link: {program_link}  :fire::fire:','username':'HackerOne','icon_emoji':':bug:'}
    f = open(f'{home_dir}/.keys/slack_web_hook')
    token = f.read()
    print("sending notification")
    requests.post(f'{token}', json=message_json)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server', help='IP Address of MongoDB API', required=False)
    parser.add_argument('-P','--port', help='Port of MongoDB API', required=False)
    return parser.parse_args()

def main(args):
    mrpo = get_most_recent_program_obj(args)
    mrp = mrpo.text
    print(f"[-] Initial Program -- {mrp}")
    mrp_link = f"https://hackerone.com{mrpo['href']}"
    # send_slack_notification(args, mrp, mrp_link)
    while True:
        if mrp != get_most_recent_program_obj(args).text:
            send_slack_notification(args, mrp, mrp_link)
        else:
            now = datetime.now()
            formatted_now = now.strftime("%m/%d/%Y, %H:%M:%S")
            print(f"[-] Same -- {mrp} -- {formatted_now}")
        sleep(600)

if __name__ == "__main__":
    args = arg_parse()
    main(args)