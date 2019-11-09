__author__ = 'Connor'

import re

line = "djkhalkfskahc2019-3dbakbfkh"

regex_str = '.*?((\d+).(\d+).(\d+)).*'

match_obj = re.match(regex_str, line)

if match_obj:
    print('yes')
    print(match_obj.group(1), match_obj.group(2), match_obj.group(3), match_obj.group(4))
    print("fdsjnafkj" "fdjsnkafl")
else:
    print('no')
