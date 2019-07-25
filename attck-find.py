#!/usr/bin/env python
import re
import os
import json
from colorama import *
from pyattck import *
from argparse import ArgumentParser

ATTACK = Attck()

def search(platform, terms, match_all=True):
    platform_re = re.compile(platform, re.I)
    terms_res = [re.compile(term, re.I) for term in terms]
    for technique in sorted(ATTACK.techniques, key=lambda x: x.id):
        if any([platform_re.match(p) for p in technique.platforms]):
            text = technique.name + technique.description
            if match_all:
                if all([tre.search(text) for tre in terms_res]):
                    yield technique
            else:
                if any([tre.search(text) for tre in terms_res]):
                    yield technique

def fold(text, width, margin):
    folded = []
    fold = ""
    for line in text.split("\n"):
        for word in line.split(" "):
            if len(fold) + len(word) + margin > width:
                folded.append(fold)
                fold = word
            else:
                fold += " " + word
        folded.append(fold)
        fold = ""
    
    folded.append(fold)
        
    return folded

def colorize_terms(text, terms, color=Fore.RED):
    terms_res = [re.compile(term, re.I) for term in terms]
    for tre in terms_res:
        for hit in tre.findall(text):
            text = text.replace(hit, f'{color}{hit}{Style.RESET_ALL}')
    return text



def format_technique(technique, terms, fmt):
    if fmt == "raw":
        return technique
    else:
        TERM_COL,TERM_LINES = os.get_terminal_size()
        name = colorize_terms(technique.name, terms)
        description = colorize_terms(technique.description, terms).strip("\n")
        detection = technique.detection.strip("\n")

        out = [
            '#'*(TERM_COL),
            " "*int((TERM_COL-len(name))/2) + f'{name}',
            '#'*(TERM_COL),
            f' {Fore.GREEN}Created{Style.RESET_ALL}: {technique.created}',
            f' {Fore.GREEN}Modified{Style.RESET_ALL}: {technique.modified}',
            '-'*(TERM_COL),
            f' {Fore.GREEN}ID{Style.RESET_ALL}: {technique.id}',
            #f' {Fore.GREEN}Name{Style.RESET_ALL}: {name}',
            f' {Fore.GREEN}Tactic{Style.RESET_ALL}: {technique._tactic}',
            "",
            f' {Fore.GREEN}Link{Style.RESET_ALL}: {technique.wiki}',
            '-'*(TERM_COL),
            f' {Fore.GREEN}Description{Style.RESET_ALL}: {description}',
            '-'*(TERM_COL),
            f' {Fore.GREEN}Detection{Style.RESET_ALL}: {detection}',
            '-'*(TERM_COL),
            "\n\n"
        ]
        return "\n".join(out)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-p", "--platform", default=".*", help="Regexp matching platform to search for.")    
    parser.add_argument("-f", "--format", default="", help="Format output")    
    parser.add_argument("-a", "--all", action="store_true", help="Search for the presence of all terms")    
    parser.add_argument("terms", nargs="+", help="Terms to search for")    

    args = parser.parse_args()

    for t in search(args.platform, args.terms, args.all):
        print(format_technique(t, args.terms, args.format))


    






