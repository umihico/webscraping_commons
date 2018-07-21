try:
    from scraping_common import lxmls_to_onetext, strip_string
except (Exception, ) as e:
    from .scraping_common import lxmls_to_onetext, strip_string


def _gen_url_from_auc_id(id):
    # url="https://auctions.yahoo.co.jp/jp/show/bid_hist?aID=q204067425"
    url = f"https://auctions.yahoo.co.jp/jp/show/bid_hist?aID={id}"
    return url


def beautify_raw_dict(raw_info_dict):
    info_dict = {}
    for key, value in raw_info_dict.items():
        new_key = strip_string(key)
        new_value = strip_string(value)
        info_dict[new_key] = new_value
    return info_dict


def parse(lxml_root):
    bidhistory_trs = lxml_root.xpath(
        "//div[@id='modCtgSearchResult']/div[@class='untBody']/table")[0].xpath(".//tr")
    bidhistory = []
    for tr in bidhistory_trs:
        tds = tr.xpath(".//td")
        td_texts = [td.text_content() for td in tds]
        bidhistory.append(td_texts)
    return bidhistory


if __name__ == '__main__':
    from lxml.html import fromstring
    from umihico_commons.requests_common import headers_dict_user_agent
    from umihico_commons.chrome_wrapper import Chrome
    from pprint import pprint
    from requests import get
    ID = "q204067425"
    url = _gen_url_from_auc_id(ID)
    print(url)
    # res = get(url, headers=headers_dict_user_agent)
    c = Chrome()
    c.get(url)
    src = c.page_source
    try:
        # lxml_root = fromstring(res.text)
        lxml_root = fromstring(src)
        bid_hist = parse(lxml_root)
        pprint(bid_hist)
    except (Exception, ) as e:
        print(res.text)
