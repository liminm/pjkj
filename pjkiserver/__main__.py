from .core import app

# Permanent storage / database handling
from .storage import storage

# Start the flask server if run from terminal
if __name__ == "__main__":

	# Tell storage to print out entire database on changes
	storage.verbosePrinting = True

	# Just allow everything to avoid the hassle when running locally.
	@app.after_request
	def add_headers(response):
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = '*'
		response.headers['Access-Control-Allow-Headers'] = '*'
		return response

	app.run()
