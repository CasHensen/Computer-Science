import re
from numpy import unique


def differentResolution(clean_title_pi, clean_title_pj):
    res_of_pi = unique(re.findall(r"\s(\d+)p\s", clean_title_pi))
    res_of_pj = unique(re.findall(r"\s(\d+)p\s", clean_title_pj))
    if len(res_of_pi) == 0 or len(res_of_pj) == 0:
        return False
    if res_of_pi != res_of_pj:
        return True
    return False
