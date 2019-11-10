from pdf2image import convert_from_path
from datetime import datetime
now = datetime.now().strftime("%d%m%Y%H%M%S%ms")
pages = convert_from_path('tests.pdf', 500)
name = now + '.png'
for page in pages:
    page.save(name, 'PNG')
