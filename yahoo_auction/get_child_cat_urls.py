from umihico_commons.xlsx_wrapper import to_xlsx
from umihico_commons.chrome_wrapper import Chrome


def get_child_cat_urls(parent_cat_url):
    c = Chrome()
    cat_url_list = []
    link_index = 0
    while True:
        c.get(parent_cat_url)
        cat_links = c.xpath("//ul[@class='child']/li/a")
        if link_index == len(cat_links):
            break
        cat_link = cat_links[link_index]
        name = cat_link.text
        print(name)
        cat_link.click()
        print(c.current_url)
        cat_url_list.append((name, c.current_url))
        link_index += 1
    return cat_url_list


def test_get_child_category_urls():
    parent_cat_url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?ei=UTF-8&p=&auccat=26318&slider=0"
    cat_url_list = get_child_cat_urls(parent_cat_url)
    to_xlsx("cat_url_list.xlsx", cat_url_list)


if __name__ == '__main__':
    test_get_child_category_urls()
