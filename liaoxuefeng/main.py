import pycurl
import certifi
from io import BytesIO

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(pycurl.CAINFO, certifi.where())
c.setopt(
    c.URL,
    'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014316090478912dab2a3a9e8f4ed49d28854b292f85bb000'
)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()
# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
print(body.decode('iso-8859-1'))