from pdf2image import convert_from_path
from datetime import datetime
import os

now = datetime.now().strftime("%d%m%Y%H%M%S%ms")
filename = 'sample.pdf'
pages = convert_from_path(filename, 500)
name = now + '.png'
dirs = '/home/aru/Desktop/pdftoimg/test/'
base_filename  =  os.path.splitext(os.path.basename(name))[0] + '.png'
print(enumerate(pages))
for i, page in enumerate(reversed(pages)):
    page.save(os.path.join(dirs, name + str(i) ), 'PNG')
