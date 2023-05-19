# This will be a flask app that will be used to create a web interface for the MedIntel project

import os
import time
import json

from helpers import buildenzymes

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False # Session is not permanent
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Initialize variables
storedmeds = {} # Dictionary of medicines and which enzymes they induce/inhibit and which enzymes metabolize them
patmeds = [] # List of patient medications
dictsicks = {} # Dictionary of patient sicknesses

# Load the data from the storedmeds.json file and add handling for if the file doesn't exist
if not os.path.exists("storedmeds.json"):
    with open("storedmeds.json", "w") as f:
        json.dump(storedmeds, f)
with open("storedmeds.json", "r") as f:
    storedmeds = json.load(f)

# Ensure templates are auto-reloaded
@app.after_request
def after_request(response):
    """ Ensure responses aren't cached """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0 # HTTP 1.0
    response.headers["Pragma"] = "no-cache" # HTTP 1.0
    return response

@app.route("/")
def index():
    return render_template("index.html", dictsicks = dictsicks)
    
@app.route("/addmed", methods=["GET", "POST"])
def addmed():
    if request.method == "GET":
        return redirect("/")
    else:
        if request.form.get("condition") == None and request.form.get("medname") == None:
            return redirect("/FAQ")
        patmeds.append(request.form.get("medname").lower().capitalize())
        sickness = request.form.get("condition").lower().capitalize()
        if sickness in dictsicks:
            # If the sickness is already in the dictionary, append the medication to the list
            # Check if the medication is already in the list
            if request.form.get("medname").lower().capitalize() not in dictsicks[sickness]:
                dictsicks[sickness].append(request.form.get("medname").lower().capitalize())
        else:
            # If the sickness is not in the dictionary, create a new list with the medication
            dictsicks[sickness] = [request.form.get("medname").lower().capitalize()]
        return redirect("/")

@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")
    # TODO: Add FAQ page and make it automatically bring up the relevant information, depending on the users error


# TODO: Add a page that starts calculating interactions and displays them, starting with the most influenced metabolism pathways
@app.route("/calc")
def calc():
    # TODO: 
    
    
    
    # TODO: Choose what to hand to the done.html page
    return render_template("done.html")


@app.route("/managedata", methods=["GET", "POST"])
def managedata():
    
    if request.method == "GET":
        return render_template("managedata.html", storedmeds = storedmeds)
    
    else:
        medname = request.form.get("medname")
        
        # Check if the medication is already in the dictionary
        # If the medication is already in the dictionary, append the new data to its dictionary
        if medname in storedmeds:
            # Check if the induce relationship is already in the list
            if request.form.get("willinduce") and request.form.get("willinduce") not in storedmeds[medname]["induces"]:
                storedmeds[medname]["induces"].append(request.form.get("willinduce"))
           
            # Check if the inhibit relationship is already in the list
            if request.form.get("willinhibit") and request.form.get("willinhibit") not in storedmeds[medname]["inhibits"]:
                storedmeds[medname]["inhibits"].append(request.form.get("willinhibit"))
            
            # Check if the user entered a metabolize relationship, and if not, return to the managedata page
            if request.form.get("metabolizedby") == None:
                return redirect("/managedata")

            # Check if the metabolize relationship is already in the list
            if request.form.get("metabolizedby") not in storedmeds[medname]["metabolizedby"]:
                storedmeds[medname]["metabolizedby"].append(request.form.get("metabolizedby"))
        else:
            # If the medication is not in the dictionary, create a new dictionary for it
            newmed = {}
            newmed["induces"] = [request.form.get("willinduce")]
            newmed["inhibits"] = [request.form.get("willinhibit")]
            newmed["metabolizedby"] = [request.form.get("metabolizedby")]
            storedmeds[medname] = newmed
        
        # Save the data to a file
        with open("storedmeds.json", "w") as f:
            json.dump(storedmeds, f)
        return redirect("/managedata")
    
@app.route("/presentwarnings", methods=["GET"])
def presentwarnings():
    if request.method == "GET":
        # For every medication in the patients list of medications, check if it is in the storedmeds dictionary
        # If there is a medication that is not in the storedmeds dictionary, redirect to the managedata page
        for med in patmeds:
            if med not in storedmeds:
                return redirect("/managedata")
        # For each medication in the patients list of medications, check if it induces or inhibits any enzymes
        # If it does, add the enzyme to a list of enzymes that are induced or inhibited by the patients medications
        # For each enzyme in the list, keep track of which medications induce/inhibit it
        inducedenzymes = {}
        inhibitedenzymes = {}
        for med in patmeds:
            for enzyme in storedmeds[med]["induces"]:
                if enzyme in inducedenzymes:
                    # Check if the medication is already in the list
                    if med not in inducedenzymes[enzyme]:
                        inducedenzymes[enzyme].append(med)
                else:
                    inducedenzymes[enzyme] = [med]
            for enzyme in storedmeds[med]["inhibits"]:
                if enzyme in inhibitedenzymes:
                    # Check if the medication is already in the list
                    if med not in inhibitedenzymes[enzyme]:
                        inhibitedenzymes[enzyme].append(med)
                else:
                    inhibitedenzymes[enzyme] = [med]
        # For each medication in the patients list of medications, check if the enzymes it is metabolized by are found in the inducedenzymes or inhibitedenzymes lists
        # If they are, add the medication to a list of medications that are metabolized by enzymes that are induced or inhibited by the patients medications
        toofast = {}
        tooslow = {}
        for med in patmeds:
            for enzyme in storedmeds[med]["metabolizedby"]:
                if enzyme in inducedenzymes:
                    # Add the medication to the list of medications that are metabolized by enzymes that are induced by the patients medications
                    # and therefore may be metabolized too quickly
                    if med not in toofast:
                        toofast[med] = [enzyme]
                    else:
                        toofast[med].append(enzyme)
                if enzyme in inhibitedenzymes:
                    # Add the medication to the list of medications that are metabolized by enzymes that are inhibited by the patients medications
                    # and therefore may be metabolized too slowly
                    if med not in tooslow:
                        tooslow[med] = [enzyme]
                    else:
                        tooslow[med].append(enzyme)
        # For each medicine in toofast:
        # For every enzyme in toofast[medicine], look up which medications induce it
        # and add them to the dictionary of lists called toofastmeds
        toofastmeds = {}
        for med in toofast:
            toofastmeds[med] = []
            for enzyme in toofast[med]:
                for inducingmed in inducedenzymes[enzyme]:
                    # Dont append if med == inducingmed or if inducingmed is already in the list
                    if inducingmed not in toofastmeds[med] and med != inducingmed:
                        toofastmeds[med].append(inducingmed)
        # For each medicine in tooslow:
        # For every enzyme in tooslow[medicine], look up which medications inhibit it
        # and add them to the dictionary of lists called tooslowmeds
        tooslowmeds = {}
        for med in tooslow:
            tooslowmeds[med] = []
            for enzyme in tooslow[med]:
                for inhibitingmed in inhibitedenzymes[enzyme]:
                    # Dont append if med == inhibitingmed
                    if inhibitingmed not in tooslowmeds[med] and med != inhibitingmed:
                        tooslowmeds[med].append(inhibitingmed)
        title="Results"
        counthelp = set(toofastmeds.keys()) | set(tooslowmeds.keys())
        count = len(counthelp)
        # Add any keys from toofastmeds whose lists are empty to fastdelete[]
        fastdelete = []
        for med in toofastmeds:
            if toofastmeds[med] == []:
                fastdelete.append(med)
        # Add any keys from tooslowmeds whose lists are empty to slowdelete[]
        slowdelete = []
        for med in tooslowmeds:
            if tooslowmeds[med] == []:
                slowdelete.append(med)
        # Delete any keys from toofastmeds whose lists are empty
        for med in fastdelete:
            del toofastmeds[med]
        # Delete any keys from tooslowmeds whose lists are empty
        for med in slowdelete:
            del tooslowmeds[med]
        
        return render_template("presentwarnings.html", count=count, toofastmeds=toofastmeds, tooslowmeds=tooslowmeds, patmeds=patmeds, inducedenzymes=inducedenzymes, inhibitedenzymes=inhibitedenzymes, title=title)
    else:
        return redirect("/")