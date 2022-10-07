from django.test import TestCase

import re
s = "RDD23432"
data = re.split('(\d+)',s)
print(data)