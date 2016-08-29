#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import bs4 as BeautifulSoup

URL = "http://www.rakuten.co.jp/category/fashiongoods/?l-id=top_normal_gmenu_d04"


def main():
    # Get html page
    html = urllib.request.urlopen(URL).read()
    # And se BeautifulSoup to parse it
    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")

    # Extracting tags which contains url to brands page
    tag_list = soup.find("div", attrs={"class": u"riClfx rigSetHeightWrap riMaB20"})
    tag_list = tag_list.findAll("p", attrs={"class": "riTxtAlnC"})

    # Extracting url to brands page from tag list
    url_list = []
    for element in tag_list:
        url_list.append(element.find('a', href=True)['href'])
    print(url_list)


if __name__ == "__main__":
    main()
