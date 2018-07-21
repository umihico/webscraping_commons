try:
    from scraping_common import lxmls_to_onetext, strip_string
except (Exception, ) as e:
    from .scraping_common import lxmls_to_onetext, strip_string


def parse(lxmltree):
    # print(lxmltree.xpath("//title")[0].text_content())
    xpaths0text_contents = {
        'title': "./td[@class='a1']//h3/a",
        'seller_name': "./td[@class='a1']//div[@class='a4 cf']/p/a",
        'raw_category': "./td[@class='a1']//p[@class='com_slider']",
        'end_date_raw_text': "./td[@class='pr2']/span[@class='d']",
        'end_time_raw_text': "./td[@class='pr2']/span[@class='t']"}
    image_url_xpath = "./td[@class='i']//img/@src"
    items_xpath = "//div[@id='list01']//tr[./td[@class='i'] and ./td[@class='a1'] and ./td[@class='pr1']]"
    rows = lxmltree.xpath(items_xpath)
    items = []
    for row in rows:
        info_dict = {key: strip_string(row.xpath(x)[0].text_content())
                     for key, x in xpaths0text_contents.items()}
        info_dict['image_url'] = row.xpath(image_url_xpath)[0]
        info_dict['url'] = row.xpath(xpaths0text_contents['title'])[
            0].attrib["href"]
        items.append(info_dict)
    return items


if __name__ == '__main__':
    from lxml.html import fromstring
    from pprint import pprint
    from requests import get
    from umihico_commons.requests_common import headers_dict_user_agent
    # url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?select=06&ei=UTF-8&n=100&auccat=26318&istatus=1"
    url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=%E6%9C%80%E9%AB%98%E3%83%A9%E3%83%B3%E3%82%AF+%E7%88%86%E5%85%89+%EF%BC%B410%2F%EF%BC%B416+%E3%83%9D%E3%82%B8%E3%82%B7%E3%83%A7%E3%83%B3%E8%BB%8A%E5%B9%85%2F%E3%83%90%E3%83%83%E3%82%AF%E3%83%A9%E3%83%B3%E3%83%97+89%EF%BC%B7%E7%B4%9A&va=%E6%9C%80%E9%AB%98%E3%83%A9%E3%83%B3%E3%82%AF+%E7%88%86%E5%85%89+%EF%BC%B410%2F%EF%BC%B416+%E3%83%9D%E3%82%B8%E3%82%B7%E3%83%A7%E3%83%B3%E8%BB%8A%E5%B9%85%2F%E3%83%90%E3%83%83%E3%82%AF%E3%83%A9%E3%83%B3%E3%83%97+89%EF%BC%B7%E7%B4%9A&b=1&n=20"
    response = get(url, headers=headers_dict_user_agent)
    lxmltree = fromstring(response.text)
    print(response.text)
    raw_info_dict = get_yauc_closed_list(lxmltree)
    pprint(raw_info_dict)
