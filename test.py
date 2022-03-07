

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')




def money(number:int, grouping:bool=True):
    return f"{locale.currency(number, grouping=grouping).split('.')[0][1:]}"

