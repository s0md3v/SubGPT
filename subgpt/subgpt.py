import argparse
import asyncio
import json
import os
import sys
import tldextract

import dns.resolver
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='file containing subdomains', dest='input_file')
parser.add_argument('-o', help='file to write generated/resolved subdomains', dest='output_file')
parser.add_argument('-c', help='file containing cookies in json format', dest='cookies_file')
parser.add_argument('--dont-resolve', help='just show generated subs, don\'t resolve them', dest='dont_resolve', action='store_true')
args = parser.parse_args((sys.argv[1:] or ['--help']))

prompt = "Based on the following existing subdomains on a domain, predict 50 more subdomains that are likely to exist."

cookies = []
try:
    if not args.cookies_file:
        print("[Error] Cookie file is missing. Provide a valid file through -c option.", file=sys.stderr)
        quit(1)
    with open(args.cookies_file, 'r') as f:
        cookies = json.load(f)
except:
    print("[Error] Cookie file doesn't exist or has icorrect format.", file=sys.stderr)
    quit(1)

if not args.input_file or not os.path.exists(args.input_file):
    print("[Error] Input file is missing. Provide a valid file through -i option.", file=sys.stderr)
    quit(1)


async def get_reply(text):
    """
    send the text to bing as a prompt and return the reply
    """
    bot = Chatbot(cookies=cookies)
    reply1 = await bot.ask(prompt=text, conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
    reply2 = await bot.ask(prompt="Predict 50 more please.", conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub")
    await bot.close()
    return reply1, reply2


def sub_validation(sub):
    """
    very basic check to see if a line in the reply is a subdomain
    """
    return sub and ' ' not in sub and len(sub) <= 250 and not sub.startswith('-')


def extract_subs(reply):
    """
    takes bing's reply and extracts the subdomains
    """
    try:
        for msg in reply["item"]["messages"]:
            if msg["author"] == "bot":
                return [line.lstrip('- ') for line in msg["text"].split('\n')]
    except KeyError:
        print(reply, file=sys.stderr)
        return []


def get_ips(hostname):
    """
    find the ip addresses of a hostname (handles cnames too)
    """
    try:
        return [answer.to_text() for answer in dns.resolver.resolve(hostname, "A")]
    except dns.resolver.NXDOMAIN:
        return []


def main():
    """
    it's the main function, its supposed to be this cluttered
    """
    domain = ""
    known_subs = set()
    with open(args.input_file, 'r') as f:
        first = True
        for line in f:
            if first:
                parsed = tldextract.extract(line.strip())
                domain = "." + parsed.domain + "." + parsed.suffix
                first = False
            clean = ''.join(line.rstrip().rsplit(domain, 1))
            known_subs.add(clean)
        known_subs = sorted(known_subs)

    max_len = 2000
    current_len = len(prompt)
    chunk = ""
    generated_subs = []
    output_file = open(args.output_file, 'a+') if args.output_file else sys.stdout

    print("Not stuck :)", file=sys.stderr, end="\r")  # hey user, its just slow, not stuck

    for i, sub in enumerate(known_subs):
        if current_len + len(sub) >= max_len or i+1 == len(known_subs):
            reply1, reply2 = asyncio.run(get_reply(prompt + chunk))
            generated_subs.extend(filter(sub_validation, extract_subs(reply1)))
            generated_subs.extend(filter(sub_validation, extract_subs(reply2)))
            chunk = ""
            current_len = len(prompt)
            print(f"Progress: {int(i*100/len(known_subs))}%", file=sys.stderr, end="\r")
        chunk += " " + sub
        current_len += len(sub) + 1

    if args.dont_resolve:
        for sub in set(generated_subs):
            print(sub + domain, file=output_file)
        quit(0)

    print(f"Resolving {len(generated_subs)} generated subdomains.", file=sys.stderr, end="\r")

    blacklist = []
    try:
        for answer in get_ips("subgptfirt" + domain):
            blacklist.append(answer)
    except dns.resolver.NXDOMAIN:
        pass
    else:
        for answer in get_ips("subgptsecod" + domain):
            if answer not in blacklist:
                blacklist.append(answer)

    for sub in set(generated_subs):
        answers = [answer not in blacklist for answer in get_ips(sub + domain)]
        if answers and all(answers):
            print(sub + domain, file=output_file)

    print(" " * 50, file=sys.stderr, end="\r")
