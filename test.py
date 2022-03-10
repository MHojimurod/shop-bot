

import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')




def money(number:int, grouping:bool=True):
    print(locale.currency(number, grouping=grouping),"bbb")
    return f"{locale.currency(number, grouping=grouping).split('.')[0][1:]}"





# data = "\na\nb\nc\nd\n"

# # data = data.lstrip()
# data = data.strip()
# print(data)

# for i in data.split("\r\n"):
#     print(i)


print("aaa")