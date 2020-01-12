from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
    	op=request.form.getlist('hello')
    	for x in op:
    		if(x == "world"):
    			print("world = 1")
    		if(x == "davidism"):
    			print("davidism = 1")
    		# if(x == 0):
    		# 	print("world = 0")
    		# 	print("davidism = 0")		

	
	

    return '''<form method="post">
<input type="checkbox" name="hello" value="world" checked>
<input type="checkbox" name="hello" value="davidism" checked>
<input type="submit">
</form>'''

app.run(debug=True)
