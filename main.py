#!/bin/python3
# -*- coding: UTf-8 -*-

from random import choice
import sys, os
import requests
import rich.console
import rich.traceback
from ua import user_agents
import json


console = rich.console.Console(
    width=os.get_terminal_size().columns, height=os.get_terminal_size().lines
)


def get_data(hosts: list | tuple) -> ("host", requests.Response):
    h2_params = "?fields=status,country,countryCode,isp,proxy,query"
    old_h = ""
    for h in hosts:
        if debug:
            console.print(f"Getting data from {h}", justify="center")
        try:
            if h == hosts[1]:
                old_h = h
                h += h2_params
            response = requests.get(h, headers=choice(user_agents))
            if debug:
                console.print(f"HTTP [{response.status_code}]", justify="center")
            if response.ok:
                if old_h == hosts[1]:
                    h = old_h
                return h, response
            else:
                if debug:
                    console.print(response.text)
                continue
        except:
            continue
    else:
        console.print("[red]Failed to get any data! Check connection.", justify="center")
        sys.exit(1)


hosts = [
    "http://ip-api.com/json/",
    "https://ipapi.co/json",
    "https://api.myip.com",
]

if __name__ == "__main__":
    debug = True if "--debug" in sys.argv else False
    h, response = get_data(hosts)
    data = response.text
    data = json.loads(data)
    t = "IPv4"
    isp = ""
    proxy = ""
    country = ""
    wt = "[white]"
    gn = "[green]"
    gr = "[gray]"

    if debug:
        console.print(data)
        console.print(f"Host: {h}")

    if h == hosts[1]:
        t = data["version"]
        ip = data["ip"]
        h0_cn = data["country_name"]
        h0_cc = data["country"]
        country = f"{wt}Location: {gn}[b][i]{h0_cn} ({h0_cc})[/i][/b]"

    elif h == hosts[0]:
        ip = data["query"]
        h1_cc = data['countryCode']
        h1_cn = data['country']
        h1_proxy = data['proxy']
        country = f"{wt}Location: {gn}[b][i]{h1_cn} ({h1_cc})[/i][/b]"
        isp = f"{wt}ISP: {gn}[b][i]{data['isp']}[/i][/b]"
        proxy = f"{gr}Is Proxy, VPN or Tor exit address: {gn}[b][i]{h1_proxy}[/i][/b]"

    else:
        ip = data["ip"]
        h2_cn = data["country"]
        h2_cc = data["cc"]
        country = f"{wt}Location: {gn}[b][i]{h2_cn} ({h2_cc})[/i][/b]"

    console.print(
        f"{wt}{t}: {gn}[b][i]{ip}[/i][/b]",
        country,
        isp,
        proxy,
        sep="\n",
        justify="center",
    )

    response.close()
