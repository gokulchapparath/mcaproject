from pdf2image import convert_from_path
from datetime import datetime
import os

now = datetime.now().strftime("%d%m%Y%H%M%S%ms")
pages = convert_from_path('tests.pdf', 500)
name = now + '.png'
dirs = '/home/gokul/Desktop/mcaproject/pdftoimg/test/'
for page in pages:
    page.save(os.path.join(dirs, name), 'PNG')
