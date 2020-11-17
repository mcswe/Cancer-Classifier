#Author: github.com/mcswe
#March 7, 2020
###############################################################################
ATTRS = []
ATTRS.append("ID")
ATTRS.append("radius")
ATTRS.append("texture")
ATTRS.append("perimeter")
ATTRS.append("area")
ATTRS.append("smoothness")
ATTRS.append("compactness")
ATTRS.append("concavity")
ATTRS.append("concave")
ATTRS.append("symmetry")
ATTRS.append("fractal")
ATTRS.append("class")
###############################################################################


def make_training_set(filename):
    training_records = []
    for line in open(filename,'r'):
        if '#' in line:
            continue
        line = line.strip('\n')
        line_list = line.split(',')
        
        # Create a dictionary for the line and map the attributes in
        # ATTRS to the corresponding values in the line of the file
        record = {}
        
        # read patient ID as an int:
        record[ATTRS[0]] = int(line_list[0].strip())
        
        # read attributes 1 through 10 as floats:
        for i in range(1,11):
            record[ATTRS[i]] = float(line_list[i])
        
        # read the class (label), which is "M", or "B" as a string:
        record[ATTRS[11]] = line_list[31].strip() 

        # Add the dictionary to a list
        training_records.append(record)        

    return training_records


def make_test_set(filename):
    test_records = make_training_set(filename)

    for record in test_records:
        record["prediction"] = "none"

    return test_records


def train_classifier(training_records):
    """
        Precondition: training_records is a list of patient record
                      dictionaries, each of which has the keys
                      in the global variable ATTRS
        Postcondition: the returned dict has midpoint values calculated
                       from the training set for all 10 attributes except
                       "ID" and"class".
    """
    malignant_midpoint = {}
    benign_midpoint = {}
    midpoint = {}
    
    #counters for malignant and benign patients
    m_patient = 0
    b_patient = 0
    
    #loop through global list of attributes
    for i in ATTRS[1:11]:
        malignant_midpoint[i] = 0
        benign_midpoint[i] = 0
        midpoint[i] = 0
    
    #loop through each patient in the training records (type list)
    for dictionary in training_records:
        #loop through attributes (type dictionary) in list of attributes
        for attribute in ATTRS[1:11]:      
            if dictionary["class"] == "M":
                #add the patient's (dictionary) attribute (type: float) to the malignant_midpoint dictionary at index attribute
                malignant_midpoint[attribute] = malignant_midpoint[attribute] + dictionary[attribute]
                m_patient += 1
            else:
                benign_midpoint[attribute] = benign_midpoint[attribute] + dictionary[attribute]
                b_patient += 1
                
    #calculate the midpoint
    for i in ATTRS[1:11]:
        malignant_midpoint[i] = malignant_midpoint[i]/m_patient
        benign_midpoint[i] = benign_midpoint[i]/b_patient
        midpoint[i] = 10*(malignant_midpoint[i]+benign_midpoint[i])/2

    return midpoint

def classify(test_records, classifier):
    """ Use the given classifier to make a prediction for each record in
        test_records, a list of dictionary patient records with the keys in
        the global variable ATTRS. A record is classified as malignant
        if at least 5 of the attribute values are above the classifier's
        threshold.
        Precondition: classifier is a dict with midpoint values for all
                      keys in ATTRS except "ID" and "class"
        Postcondition: each record in test_records has the "prediction" key
                       filled in with the predicted class, either "M" or "B"
    """
    #loop through patients in test_records
    for patient in test_records:
        #vote counters for benign and malignant
        benign_vote = 0
        malignant_vote = 0
        #loop through attributes in list of attributes excluding ID
        for attribute in ATTRS[1:11]:
            #if the votes for the patient's attribute is larger
            if patient[attribute] >= classifier[attribute]:
                #vote for malignant
                malignant_vote += 1
            else:
                #vote for benign
                benign_vote += 1
        
        #uses largest vote to classify the prediction!        
        if malignant_vote >= benign_vote:
            patient["prediction"] = "M"
        else:
            patient["prediction"] = "B"
        
def report_accuracy(test_records):
    """ Print the accuracy of the predictions made by the classifier
        on the test set as a percentage of correct predictions.
        
        Precondition: each record in the test set has a "prediction"
        key that maps to the predicted class label ("M" or "B"), as well
        as a "class" key that maps to the true class label. """
    
    #correct predictions out of total predictions
    correct = 0
    total = 0
    for patient in test_records:
        #if the prediction and class are the same, it is a correct guess
        if patient["prediction"] == patient["class"]:
            correct += 1
            total += 1
        else:
            #even though the guess wasn't correct, it was still a guess
            total += 1
    print("Classifier accuracy:" , correct/total*100)

def check_patients(test_records, classifier):
    """ Repeatedly prompt the user for a Patient ID until the user
        enters "quit". For each patient ID entered, search the test
        set for the record with that ID, print a message and prompt
        the user again. If the patient is in the test set, print a
        table: for each attribute, list the name, the patient's value,
        the classifier's midpoint value, and the vote cast by the
        classifier. After the table, output the final prediction made
        by the classifier.
        If the patient ID is not in the test set, print a message and
        repeat the prompt. Assume the user enters an integer or quit
        when prompted for the patient ID.
    """
    # prompt user for an ID
    promptUser = input("Enter an ID.")
    # while the user has not entered "quit":
    while promptUser != "quit":
    # determine whether the entered patient ID is in the test set
        validID = False
        for record in test_records:
            if promptUser == str(record["ID"]):
                validID = True
                # if it is,
                table(record, classifier)  
    # otherwise, print a message saying the patient ID wasn't found
        if validID == False:
            print("The patient ID wasn't found.")                  
        # prompt the user for another ID
        promptUser = input("Enter another ID.")

#function to make the table
def table(record, classifier):
    print("Attribute".rjust(15) + "Patient".rjust(12) + "Classifier".rjust(12) + "Vote". rjust(12))
    for key in ATTRS[1:11]:
        print(key.rjust(15), end = "")
        print(str("{:.4f}".format(record[key])).rjust(12), end = "")
        print(str("{:.4f}".format(classifier[key])).rjust(12), end = "")
        
        if record[key] >= classifier[key]:
            print("Malignant".rjust(12))
        else:
            print("Benign".rjust(12))
    
    #determine the diagnosis    
    if record["prediction"] == "M":
        diagnosis = "Malignant"
    else:
        diagnosis = "Benign"
        
    print("Classifier's diagnosis: " + diagnosis)

if __name__ == "__main__": 
    # Main program - COMPLETE

    # load the training set
    print("Reading in training data...")
    training_data_file = "cancerTrainingData.txt"
    training_set = make_training_set(training_data_file)
    print("Done reading training data.")
    
    # load the test set 
    print("Reading in test data...")
    test_file = "cancerTestingData.txt"
    test_set = make_test_set(test_file)
    print("Done reading test data.\n")

    print("Training classifier..."    )
    classifier = train_classifier(training_set)
    print("Classifier cutoffs:")
    for key in ATTRS[1:11]:
       print("    ", key, ": ", classifier[key], sep="")
    print("Done training classifier.\n")

    print("Making predictions and reporting accuracy")
    classify(test_set, classifier)
    report_accuracy(test_set)
    print("Done classifying.\n")

    # prompt the user for patient IDs and provide details on the diagnosis
    check_patients(test_set, classifier)
