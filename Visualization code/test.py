import schemdraw
from schemdraw.flow import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from cgitb import text

information = {
    "blank" : "",
    "condition" : "",
    "participant" : 0,
    "allocation" : "",
    "interventionModel" : "",
    "estimatedStudyTime" : "",
    "outcomePrimary" : [],
    "outcomeSecondary" : [],
    "minAge" : 0,
    "maxAge" : "",
    "gender" : "",
    "healthy" : ""
}

armTypeLabelList = []
armIntervention = []
convertInterventionDescriptionList = []
convertInterventionTypeStringList = []
InterventionList = []

url = "https://clinicaltrials.gov/api/query/full_studies?expr=Prospective%2C+Randomized%2C+Multinational%2C+Multicenter%2C+Double-blind%2C+Placebo+and+Active+Controlled+Trial+in+4+Parallel-groups+of+Patients+Suffering+From+Seasonal+Allergic+Rhinitis&min_rnk=1&max_rnk=&fmt=json"
import requests
def get_info(url):
    response = requests.get(url).json()
    protocolSection = response['FullStudiesResponse']['FullStudies'][0]['Study']['ProtocolSection']

    #condition
    convertString = ''.join([str(item) for item in protocolSection['ConditionsModule']['ConditionList']['Condition']])
    information['condition'] = convertString

    #participant
    information["participant"] = protocolSection['DesignModule']['EnrollmentInfo']['EnrollmentCount']

    #allocation
    information["allocation"] = protocolSection['DesignModule']['DesignInfo']['DesignAllocation']

    #intervention Model
    information["interventionModel"] = protocolSection['DesignModule']['DesignInfo']['DesignInterventionModel']

    #estimated time
    information["estimatedStudyTime"] = protocolSection["StatusModule"]["CompletionDateStruct"]["CompletionDate"]

    #outcome primary
    for i in range(len(protocolSection['OutcomesModule']['PrimaryOutcomeList']['PrimaryOutcome'])):
        information['outcomePrimary'] = protocolSection['OutcomesModule']['PrimaryOutcomeList']['PrimaryOutcome'][i]['PrimaryOutcomeMeasure']

    #outcome secondary
    for i in range(len(protocolSection['OutcomesModule']['SecondaryOutcomeList']['SecondaryOutcome'])):
        information['outcomeSecondary'] = protocolSection['OutcomesModule']['SecondaryOutcomeList']['SecondaryOutcome'][i]['SecondaryOutcomeMeasure']

    #basic information
    information['minAge'] = protocolSection["EligibilityModule"]["MinimumAge"]
    if("MaximumAge" in protocolSection["EligibilityModule"]):
      information['maxAge'] = protocolSection["EligibilityModule"]["MaximumAge"]
    information['gender'] = protocolSection["EligibilityModule"]["Gender"]
    information['healthy'] = protocolSection["EligibilityModule"]["HealthyVolunteers"]

get_info(url)

response = requests.get(url).json()
protocolSection = response['FullStudiesResponse']['FullStudies'][0]['Study']['ProtocolSection']
#arm side
for i in range(len(protocolSection['ArmsInterventionsModule']['ArmGroupList']['ArmGroup'])):
    convertArmTypeString = ''.join([str(item) for item in protocolSection['ArmsInterventionsModule']['ArmGroupList']['ArmGroup'][i]['ArmGroupType']])
    convertArmLabel = ''.join([str(item) for item in protocolSection['ArmsInterventionsModule']['ArmGroupList']['ArmGroup'][i]['ArmGroupLabel']])
    armTypeLabelList.append(convertArmTypeString +": " + convertArmLabel)

#intervention side
for i in range(len(protocolSection['ArmsInterventionsModule']['InterventionList']['Intervention'])):
    convertInterventionTypeString = ''.join([str(item) for item in protocolSection['ArmsInterventionsModule']['InterventionList']['Intervention'][i]['InterventionName']])
    convertInterventionDescription = ''.join([str(item) for item in protocolSection['ArmsInterventionsModule']['InterventionList']['Intervention'][i]['InterventionDescription']])
    convertInterventionTypeStringList.append(convertInterventionTypeString)
    convertInterventionDescriptionList.append(convertInterventionDescription)



with schemdraw.Drawing() as d:
    d+= Start(w = 10, h = 5).label("Population" + "\n" + information['condition'] + "\n" + information['minAge'] + " ~ " + information['maxAge'] + "\n" + "Gender: " + information['gender'] + "\n" + "Health: " + information['healthy'])
    d+= Arrow().right(d.unit*2)
    
    #Input the string 
    d+= Connect(r = 1).label("N= " + information["participant"]).color("blue")
    d+= Arrow().right(d.unit/2)

    d+= Box(w = 10).label(armTypeLabelList[0])
    d+= Arrow().up(d.unit)

    d+= Box(w = 10).label(armTypeLabelList[1])
    d+= Arrow().down(d.unit)

    

        
    
    d.save("output/palindrome flowchart.jpeg", dpi = 300)