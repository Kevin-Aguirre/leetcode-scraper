from bs4 import BeautifulSoup
from selenium import webdriver
import os
import shutil
import json
import requests

#debuggig
import pprint
import sys 


def getStudyplansFromUser(studyPlansNames):
    print(
        """Welcome! \nPlease enter the LeetCode study plans you would like to work on!
        Note: You must enter the study plan name exactly as it shows up on LeetCode
            Valid Study Plans: 'LeetCode 75'; 'Binary Search'; '30 Days of JavaScript'
            Invalid Study Plans: 'leetcode75'; 'binary search'; '30 Days of Js'
        
        """
    )
    studyPlans = []
    usrRes = str(input("What would you like to study (q to quit): "))
    while (usrRes != 'q'):
        try:
            currStudyPlan = studyPlansNames[usrRes]
            studyPlans.append(usrRes)
            print(f"Succesfully Added: '{usrRes}'")
        except KeyError:
            print(f"Could not add '{usrRes}'. We may not support that study plan at this moment or your spelling is incorrect.")
        usrRes = str(input("What would you like to study (q to quit): "))
    return studyPlans
    

def getProblemInfo(language, problemSlug, problemUrl):
    data = {"operationName":"questionData","variables":{"titleSlug":f"{problemSlug}"},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

    r = requests.post('https://leetcode.com/graphql', json = data).json()
    if (r['data']['question']['isPaidOnly']):
        return ""
    soup = BeautifulSoup(r['data']['question']['content'], 'lxml')

    title = r['data']['question']['title'] # title 

    codeSnippetArray = r['data']['question']['codeSnippets']

    codeSnippet = None # code snippet 
    for codeSnipDict in codeSnippetArray:
        if (codeSnipDict['lang'] == language):
            codeSnippet = codeSnipDict['code'] # code snippet

    question = soup.get_text() # question

    fileContent = f"\"\"\"\n{problemUrl}\n\n\n{title}\n\n{question}\n\"\"\"\n\n{codeSnippet}"
    return fileContent

def formatSubgroupName(rawSubgroup):
    rawSubgroup = rawSubgroup.strip()
    rawSubgroup = rawSubgroup.replace(" ", "")
    formattedSubgroup = rawSubgroup.replace("/","-")
    return formattedSubgroup

def formatProblemUrl(problemSlug):
    return f"https://leetcode.com/problems/{problemSlug}/description/"

def main(): 
    studyPlansNames = {
        'LeetCode 75' : {
            'titleSlug': 'leetcode-75',
        },
        'Top Interview 150' : {
            'titleSlug': 'top-interview-150',
        },
        'Binary Search' : {
            'titleSlug': 'binary-search',
        },
        'SQL 50' : {
            'titleSlug': 'top-sql-50',
        },
        'Introduction to Pandas' : {
            'titleSlug': 'introduction-to-pandas',
        },
        '30 Days of Pandas' : {
            'titleSlug': '30-days-of-pandas',
        },
        '30 Days of JavaScript' : {
            'titleSlug': '30-days-of-javascript',
        },
        'Top 100 Liked' : {
            'titleSlug': 'top-100-liked',
        }
    }

    studyPlans = getStudyplansFromUser(studyPlansNames)
    slugArr = [studyPlansNames[plan]['titleSlug'] for plan in studyPlans] # 🐌
    dr = webdriver.Chrome() 

    #curdir 
    parent_dir = os.getcwd()

    for slug in slugArr:
        dr.get(f"https://leetcode.com/studyplan/{slug}/")
        soup = BeautifulSoup(dr.page_source, "lxml")
        unfilteredProblems = soup.find('script', id="__NEXT_DATA__").text

        # language 
        language = "Python"

        # inner page (where the problems are) as json
        pageJson = json.loads(unfilteredProblems)

        # subgroups list (holds problems in dictionaries )
        problemsSubgroupsList = pageJson['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']["studyPlanV2Detail"]["planSubGroups"]



        os.mkdir(slug)
        os.chdir(f"{parent_dir}/{slug}")

        for subgroup in problemsSubgroupsList:
            subgroupDirName = formatSubgroupName(subgroup['name']) 
            os.mkdir(subgroupDirName)
            os.chdir(f"{parent_dir}/{slug}/{subgroupDirName}")

            for question in subgroup['questions']:
                problemSlug = question['titleSlug']
                problemUrl = formatProblemUrl(problemSlug)
                
                fileContent = getProblemInfo(language, problemSlug, problemUrl)
                if (fileContent != ""):
                    with open(f"{problemSlug}.py", 'w') as file:
                        file.write(fileContent)

            childDir = os.getcwd()
            os.chdir(f"{parent_dir}/{slug}")

            if (os.listdir(childDir) == []):
                shutil.rmtree(childDir)
        
        os.chdir(parent_dir)

    


main()
