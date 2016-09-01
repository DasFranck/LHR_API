#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import bs4 as BeautifulSoup

URL = "http://www.rakuten.co.jp/category/fashiongoods/?l-id=top_normal_gmenu_d04"


class LHR():
    # Init list
    def __init__(self, debug=False):
        self.url_list = []
        self.result = []
        self.debug = debug

    def debug_print(self, string):
        if (self.debug):
            print(string)

    # Get soup from an url
    def getsoup(self, url):
        # Get html page
        self.debug_print("Getting html from " + url)
        html = urllib.request.urlopen(url).read()
        # And use BeautifulSoup to parse it
        self.debug_print("Parsing soup...")
        soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
        return (soup)

    # Extract the search pages for any luxury handbags brand
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

    # Extract price from the item
    def extract_price(self, item):
        cleaned = ""
        price = item.find("p", attrs={"class": "price"}).text
        for i in price:
            if i.isdigit():
                cleaned += i
        return (int(cleaned))

    # Remove \n and \t from a string
    def clean_text(self, name):
        string = ""
        for i in name:
            if i not in ["\n", "\t"]:
                string += i
        return (string if string[0] is not " " else string[1:])

    # TODO : May also parse the items page to get more pictures instead of the thumbnail
    #        But that will multiply the request amount by 46...
    # Parse a rakuten search page
    def parse_search_page(self, soup):
        item_list = soup.findAll("div", attrs={"class": "rsrSResultSect clfx"})
        for item in item_list:
            item_dict = dict()
            item_dict["name"] = item.img["alt"] if item.img.has_attr("alt") else None
            item_dict["url"] = item.a["href"]
            description = item.find("p", attrs={"class": "copyTxt"})
            if description is not None:
                item_dict["description"] = self.clean_text(description.text)
            else:
                item_dict["description"] = None
            item_dict["price"] = self.extract_price(item)
            item_dict["picture_url"] = item.img["src"]
            item_dict["seller_name"] = self.clean_text(item.find("span", attrs={"class": "txtIconShopName"}).text)
            item_dict["seller_url"] = item.find("span", attrs={"class": "txtIconShopName"}).a["href"]
            self.result.append(item_dict)

    # Launch the API and fill self.result
    def start(self):
        soup = self.getsoup(URL)
        url_brand_list = self.extract_brands(soup)
        self.debug_print(str(len(url_brand_list)) + "brands found, parsing now...")
        for url_brand in url_brand_list:
            print("%d/%d brands parsed" % (url_brand_list.index(url_brand) + 1, len(url_brand_list)))
            i = 1
            failed = False
            while not failed:
                soup = self.getsoup(url_brand + "?p=" + str(i))
                # Check if the search page is back to the first (overflow)
                failed = (i != int(soup.find("input", attrs={"id": "ratPageNum"})["value"]))
                if not failed:
                    self.parse_search_page(soup)
                    i += 1
            print("%d pages analysed\n" % (i - 1))


if __name__ == "__main__":
    lhr = LHR(debug=True)
    lhr.start()
    print(lhr.result)
    print("%s items found." % len(lhr.result))
