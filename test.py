import locale
locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')

res = locale.currency(10000, grouping=True)

print(res[1:])