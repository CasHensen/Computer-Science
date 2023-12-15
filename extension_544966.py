import re


def differentInch(clean_title_pi, clean_title_pj):
    inches_of_pi = re.findall(r"(\d+)inch", clean_title_pi)
    inches_of_pj = re.findall(r"(\d+)inch", clean_title_pj)

    if len(inches_of_pi) == 0 or len(inches_of_pj) == 0:
        return False

    for inch_pi in inches_of_pi:
        for inch_pj in inches_of_pj:
            if abs(int(inch_pi) - int(inch_pj)) <= 1:  # sometimes decimal numbers are used (e.g., 46 and 45.9 both)
                return False

    return True


def differentHz(clean_title_pi, clean_title_pj):
    hz_of_pi = re.findall(r"(\d+)hz", clean_title_pi)
    hz_of_pj = re.findall(r"(\d+)hz", clean_title_pj)

    if len(hz_of_pi) == 0 or len(hz_of_pj) == 0:
        return False

    if hz_of_pi != hz_of_pj:
        return True

    return False
