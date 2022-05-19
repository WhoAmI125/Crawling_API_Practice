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

url = "https://clinicaltrials.gov/api/query/full_studies?expr=The+Effect+of+Eplerenone+on+the+Evolution+of+Vasculopathy+in+Renal+Transplant+Patients.+%28EVATRAN%29&min_rnk=1&max_rnk=&fmt=json"
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

fig, ax = plt.subplots()
#Box for the population
rectpopulation = patches.Rectangle(
   (0, 0),
   1.5, 3.0,
   fill = False)

ax.add_patch(rectpopulation)
ax.text(0.2, 3.0, "Population", {"size": 15})
ax.text(0.1, 2.5, "Condition: " + information['condition'], {"size": 5})
ax.text(0.1, 1.8, "Age: " + information['minAge'] + " ~ " + information['maxAge'], {"size": 7})
ax.text(0.1, 1.4, "Gender: " + information['gender'], {"size": 7})
ax.text(0.1, 1.0, "Health: " + information['healthy'], {"size": 7})

#Circle for participants
circleParticipates = plt.Circle(
    (2.2, 1.5), 
    0.3,
    fill = False)
#line connects population-participants
ax.plot([1.5,1.9],[1.5,1.5])
#text showing n = of population
ax.text(2.0, 1.5, "N= " + information["participant"], {"size": 7})
ax.add_patch(circleParticipates)

for i in range(len(armTypeLabelList)):
    count = 0
    depend = 2
    ax.text(2.5, i+0.6, armTypeLabelList[i], {"size": 7})
    ax.plot([2.5,5],[i+0.5,i+0.5])
    for j in range(len(convertInterventionTypeStringList)):
        if("without eplerenone" in convertInterventionTypeStringList[j]):
            ax.text(2.5, i+0.4+count, convertInterventionDescriptionList[j], {"size": 5})
            count -= 0.1
        elif("Eplerenone" in convertInterventionTypeStringList[j]):
            ax.text(2.5, i+0.4+count, convertInterventionDescriptionList[j], {"size": 5})
            count -= 0.1
    if( i % depend == 0):
        ax.plot([5,6],[i+0.5,i+1.5])
        ax.plot([6,8],[i+1.5,i+1.5])
    else:
        ax.plot([5,6],[i+0.5,1.5-i])
        ax.plot([6,8],[1.5-i,1.5-i])
    depend += 1


plt.show()
