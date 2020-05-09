from configparser import ConfigParser
import os
config = ConfigParser()
config.read('C:/Users/Hanxven/Desktop/Python_code/edu无情刷时间机器/set.ini',encoding='utf-8')
print(config.sections()) 
print(__doc__)

config.set('HanxvenSet','cookie','NoCookie')
if not config.has_section('Last'):
    config.add_section('Last')
config.write(open('C:/Users/Hanxven/Desktop/Python_code/edu无情刷时间机器/set.ini', 'w'),space_around_delimiters=False)