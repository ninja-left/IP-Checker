#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon

from random import choice
import sys
import requests
from ua import user_agents
import json
import pyperclip

class MainWindow(QMainWindow):
    def __init__(self, ip_address, ip_version, country_data, isp_data, proxy_data, error_msg, debug):
        super().__init__()
        self.setWindowTitle("What is my IP address?")
        layout = QVBoxLayout()

        ip_layout = QHBoxLayout()
        self.lbl_ip = QLabel(f"{ip_version}:" if error_msg == "" else "")
        self.btn_ip = QPushButton(ip_address if error_msg == "" else error_msg)
        self.btn_ip.clicked.connect(self.copyIP)
        ip_layout.addWidget(self.lbl_ip)
        ip_layout.addWidget(self.btn_ip)
        layout.addLayout(ip_layout)

        loc_layout = QHBoxLayout()
        self.lbl_location = QLabel("Location:")
        self.btn_location = QPushButton(country_data)
        self.btn_location.clicked.connect(self.copyLoc)

        isp_layout = QHBoxLayout()
        self.lbl_isp = QLabel("ISP:")
        self.btn_isp = QPushButton(isp_data)
        self.btn_isp.clicked.connect(self.copyISP)

        proxy_layout = QHBoxLayout()
        self.lbl_proxy = QLabel("Proxy, VPN or Tor exit node:")
        self.btn_proxy = QPushButton(str(proxy_data))
        self.btn_proxy.clicked.connect(self.copyProxy)

        if country_data != "":
            loc_layout.addWidget(self.lbl_location)
            loc_layout.addWidget(self.btn_location)
            layout.addLayout(loc_layout)

        if isp_data != "":
            isp_layout.addWidget(self.lbl_isp)
            isp_layout.addWidget(self.btn_isp)
            layout.addLayout(isp_layout)

        if proxy_data != "":
            proxy_layout.addWidget(self.lbl_proxy)
            proxy_layout.addWidget(self.btn_proxy)
            layout.addLayout(proxy_layout)
        
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
    
    def copyIP(self):
        pyperclip.copy(self.btn_ip.text())

    def copyLoc(self):
        pyperclip.copy(self.btn_location.text())
    
    def copyISP(self):
        pyperclip.copy(self.btn_isp.text())

    def copyProxy(self):
        pyperclip.copy(self.btn_proxy.text())


def get_data(hosts: list | tuple) -> ("host", requests.Response):
    h2_params = "?fields=status,country,countryCode,isp,proxy,query"
    old_h = ""
    for h in hosts:
        if debug:
            print(f"Getting data from {h}")
        try:
            if h == hosts[0]:
                old_h = h
                h += h2_params
            response = requests.get(h, headers=choice(user_agents))
            if debug:
                print(f"HTTP [{response.status_code}]")
            if response.ok:
                if old_h == hosts[0]:
                    h = old_h
                return h, response
            else:
                if debug:
                    print(response.text)
                continue
        except:
            continue
    else:
        print("Failed to get any data! Check connection.")
        error_msg = "Failed to get any data! Check connection."


if __name__ == "__main__":
    hosts = [
    "http://ip-api.com/json/",
    "https://ipapi.co/json",
    "https://api.myip.com",
    ]
    pyperclip.determine_clipboard()
    debug = True if "--debug" in sys.argv else False
    error_msg = ""
    ip_ver = 'IPv4'
    country = ""
    isp = ""
    proxy = ""
    wt = "[white]"
    gn = "[green]"
    gr = "[gray]"

    h, response = get_data(hosts)
    data = response.text
    data = json.loads(data)

    if debug:
        print(data)
    
    if h == hosts[0]:
        ip_addr = data["query"]
        h1_cc = data['countryCode']
        h1_cn = data['country']
        h1_proxy = data['proxy']
        country = f"{h1_cn} ({h1_cc})"
        isp = data['isp']
        proxy = h1_proxy

    elif h == hosts[1]:
        ip_ver = data["version"]
        ip_addr = data["ip"]
        h0_cn = data["country_name"]
        h0_cc = data["country_code"]
        country = f"{h0_cn} ({h0_cc})"

    else:
        ip_addr = data["ip_addr"]
        h2_cn = data["country"]
        h2_cc = data["cc"]
        country = f"{h2_cn} ({h2_cc})"

    app = QApplication(sys.argv)
    window = MainWindow(ip_addr, ip_ver, country, isp, proxy, error_msg, debug)
    window.show()

    app.exec_()
