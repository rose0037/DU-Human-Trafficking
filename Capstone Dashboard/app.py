from flask import Flask, render_template

# new import
from bokeh.embed import server_document 


######################
# Note - before running this script the bokeh server needs to be running the viz you want to embed
# To do this you also need to allow this application to access it, so, you need to run the command:
#     bokeh server --allow-websocket-origin=localhost:5000 fileName.py
#     where "fileName.py" is the name of the python file that creates the visualization
######################

app = Flask(__name__)

@app.route("/")
def index():
	# Get the script from the running server appliction on port 5006, 
	# then pass into render_template to embed in index.html
	bokeh_script = server_document("http://localhost:5006/capstone_dashboard")  
	return render_template("index.html",bokeh_script=bokeh_script)

# run the app, so to open it go to browser on localhost:5000
if __name__ == "__main__":
	app.run(port=5000,debug=True)
