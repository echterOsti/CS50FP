# Author: Peter Ostermeier
def buildenzymes(storedmeds):
    """Build the dictionary of enzymes and their associated medications"""
    # Initialize variables
    enzymes = {} # Dictionary of enzymes and which medications induce/inhibit them and which medications are metabolized by them
    # Build the dictionary of enzymes by reversing the storedmeds dictionary
    for med in storedmeds:
        for enzyme in storedmeds[med]["metabolizedby"]:
            if enzyme in enzymes:
                # Check if the medication is already in the list
                if med not in enzymes[enzyme]["metabolizes"]:
                    enzymes[enzyme]["metabolizes"].append(med)
            else:
                enzymes[enzyme] = {"metabolizes": [med], "inducedby": [], "inhibitedby": []}

        for enzyme in storedmeds[med]["induces"]:
            if enzyme in enzymes:
                # Check if the medication is already in the list
                if med not in enzymes[enzyme]["inducedby"]:
                    enzymes[enzyme]["inducedby"].append(med)
            else:
                enzymes[enzyme] = {"metabolizes": [], "inducedby": [med], "inhibitedby": []}
        
        for enzyme in storedmeds[med]["inhibits"]:
            if enzyme in enzymes:
                # Check if the medication is already in the list
                if med not in enzymes[enzyme]["inhibitedby"]:
                    enzymes[enzyme]["inhibitedby"].append(med)
            else:
                enzymes[enzyme] = {"metabolizes": [], "inducedby": [], "inhibitedby": [med]}
    return enzymes
