# Use Flask to render a template
# Use PyMongo to interact with Mongo
# Use use the Scraping code from Jupyter
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/")

# Use PyMongo to find the "mars" collection
# Return an HTML template using an index.html file
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Define the route Flask will use
@app.route("/scrape")

# Assign a variable that points to the Mongo database
# Create a variaqble to hold the newly scraped data
# Update the database
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# Save work
if __name__ == "__main__":
   app.run()