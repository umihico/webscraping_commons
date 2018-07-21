try:
    from scraping_common import lxmls_to_onetext, strip_string
except (Exception, ) as e:
    from .scraping_common import lxmls_to_onetext, strip_string
import re


def beautify_raw_dict(raw_info_dict):
    info_dict = {}
    for key, value in raw_info_dict.items():
        new_key = strip_string(key)
        new_value = strip_string(value)
        info_dict[new_key] = new_value
    return info_dict


def parse(lxml_root):
    raw_info_dict = {}
    trs_xpath_dict = {
        'prices_trs': "//div[@class='untHead' and contains(.,'商品の情報')]/following-sibling::div[contains(@class,'untBody')]//div[contains(@class,'untTaxPrice')]//table",
        'details_trs': "//div[./p[contains(.,'詳細情報')]]",
        'seller_trs': "//div[@class='untHead' and contains(.,'出品者の情報')]/following-sibling::div[contains(@class,'untBody')]//table",
        'payment_trs': "//div[@class='untHead' and contains(.,'支払いについて')]/following-sibling::div[contains(@class,'untBody')]//table",
        'shipping_trs': "//div[@class='untHead' and contains(.,'送料、商品の受け取りについて')]/following-sibling::div[contains(@class,'untBody')]//table", }
    for trs_xpath in trs_xpath_dict.values():
        trs = lxml_root.xpath(trs_xpath)[0].xpath(".//tr")
        for tr in trs:
            key = lxmls_to_onetext(tr.xpath(".//th"))
            value = lxmls_to_onetext(tr.xpath(".//td"))
            raw_info_dict[key] = value

    script_text = '\n'.join([e.text_content() for e in lxml_root.xpath(
        "//script[@type='text/javascript']")])
    script_text = script_text.replace('"', '')
    keys = ["productID", "productName", "productCategoryID", "price",
            "winPrice", "quantity", "bids", "starttime", "endtime"]
    for key in keys:
        # print(key)
        value = re.findall(key + ": .+?,", script_text)[0]
        value = value.replace(key + ": ", '')
        value = value[:len(value) - 1]
        raw_info_dict[key] = value
    info_dict = beautify_raw_dict(raw_info_dict)
    return info_dict


if __name__ == '__main__':
    from lxml.html import fromstring
    from pprint import pprint
    from umihico_commons.requests_wrapper import get
    url = "https://page.auctions.yahoo.co.jp/jp/auction/302276461"
    res = get(url)
    print(res.text)
    lxml_root = fromstring(res.text)

    # [print(()) for x in lxml_root.xpath("//*[@property]")]

    raw_info_dict = parse(lxml_root)
    pprint(raw_info_dict)
