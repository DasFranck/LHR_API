#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import bs4 as BeautifulSoup

URL = "http://www.rakuten.co.jp/category/fashiongoods/?l-id=top_normal_gmenu_d04"


class LHR_API():
    # Init list and dict
    def __init__(self):
        self.url_list = []
        self.result = dict()

    def getsoup(self, url):
        # Get html page
        html = urllib.request.urlopen(url).read()
        # And use BeautifulSoup to parse it
        soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
        return (soup)

    def extract_brands(self, soup):
        # Extract tags which contains url to brands page in the luxury ブランド section
        tag_list = soup.find("div", attrs={"class": "riClfx rigSetHeightWrap riMaB20"})
        tag_list = tag_list.findAll("p", attrs={"class": "riTxtAlnC"})

        # Extract urls to brand pages from tag list
        tmp_list = []
        url_brand_list = []
        for element in tag_list:
            tmp_list.append(element.find('a', href=True)['href'])

        # Extract urls to luxury handbags from brandpages
        # Note: Coach, Chanel and Loewe don't have an handbags section
        for element in tmp_list:
            tag_list = self.getsoup(element).findAll("div")
            if tag_list is not None:
                for tag in tag_list:
                    if "ハンドバッグ" in str(tag):
                        a_block = tag.find("a", href=True)
                        if (a_block is not None and "search" in a_block["href"]):
                            url_brand_list.append(a_block["href"])

        # Remove duplicates and return the list
        return (list(set(url_brand_list)))

    def start(self):
        # try:
        soup = self.getsoup(URL)
        # except Exception as err_msg:
        #    print("Error: Getting soup has failed: %s" % err_msg)
        #    return
        url_brand_list = self.extract_brands(soup)
        print(url_brand_list)


if __name__ == "__main__":
    lhr = LHR_API()
    lhr.start()
