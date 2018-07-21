import codecs


def get_local_html(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        src = f.readlines()
        src = '\n'.join(src)
        return src


def lxmls_to_onetext(lxml_element_list):
    string = ''.join([x.text_content() for x in lxml_element_list])
    return string


def strip_string(string):
    for replace in [' ', "　", "\n", "\t", "\xa0", ]:
        string = string.replace(replace, '')
    string = string.strip()
    if string.startswith(':') or string.startswith('：'):
        string = string[1:]
    string = string.strip()
    return string
