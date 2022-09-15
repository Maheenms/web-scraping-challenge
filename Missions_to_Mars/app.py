# the main goal of creating flask is to print the scrape_all dictionary onto a scrape route and then connect it to mongoDB

from flask import Flask, render_template, redirect, url_for # url_for is used for to go to and from our endpoints of the flask app /moving to the index route and mongodb 
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#use flask pymongo to set up the connnection to the mongo database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_database" # this connects the mongoDB and also creates a mars_data_da databse 
mongo = PyMongo(app)

@app.route("/")
def index():
    #return"hello! you are here on index" # checking to see if we get the index page 


    #access information from the mongo database once we have uploaded it using the scrape route
    mars_data_scraped = mongo.db.marsDataCollection.find_one()
    #print(mars_data_scraped)
    #return "Flask uploaded"
    return render_template("index.html", mars = mars_data_scraped)
    


@app.route("/scrape")
def scrape():
    #return " Welcome to the scraping page"

    
    # refernce to a databse collection(table)
    mars_Table = mongo.db.marsDataCollection # creates a collection called marsDataCollection

    # drop the table if it exists so that we run multiple times, it doesnt create new tables 
    mongo.db.marsDataCollection.drop()

    
   
    # call scrape mars script
    mars_data_scraped = scrape_mars.scrape_all()
    #return mars_data_scraped # prints the dictionary to the scrape page


    # take the dictinary and load it into mongoDB collection 
    mars_Table.insert_one(mars_data_scraped)

    #return mars_data
    # go back to the index route
    return redirect("/")


if __name__ == "__main__":
    app.run()    
