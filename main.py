from bs4 import BeautifulSoup
from selenium import webdriver
from PySide6 import QtCore, QtWidgets
import sys
import os
import shutil
import json
import requests

queryLanguages = {
    'PostgreSQL' : {
        'extension': 'sql',
        'sl_comm_chars' : '--',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Pandas' : {
        'extension': 'py',
        'sl_comm_chars' : '#',
        'ml_comm_start' : '"""',
        'ml_comm_end' : '"""'
    },
    'Oracle' : {
        'extension': 'dbf',
        'sl_comm_chars' : '--',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'MS SQL Server' : {
        'extension': 'mdf',
        'sl_comm_chars' : '--',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    }, 
    'MySQL' : {
        'extension': 'sql',
        'sl_comm_chars' : '#',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    }
}

allowedLanguages = {
    'C++' : {
        'extension': 'cpp',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Java': { 
        'extension': 'java',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Python' : {
        'extension': 'py',
        'sl_comm_chars' : '#',
        'ml_comm_start' : '"""',
        'ml_comm_end' : '"""'
    },
    'Python3' : {
        'extension': 'py',
        'sl_comm_chars' : '#',
        'ml_comm_start' : '"""',
        'ml_comm_end' : '"""'
    },
    'C' : {
        'extension': 'c',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    }, 
    'C#' : {
        'extension': 'cs',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'JavaScript' : {
        'extension': 'js',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'TypeScript' : {
        'extension': 'ts',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'PHP' : {
        'extension': 'php',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Swift' : {
        'extension': 'swift',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Kotlin' : {
        'extension': 'kt',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    }, 
    'Go' : {
        'extension': 'go',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Ruby' : {
        'extension': 'rb',
        'sl_comm_chars' : '#',
        'ml_comm_start' : '=begin',
        'ml_comm_end' : '=end'
    },
    'Scala': {
        'extension': 'sc',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Rust' : {
        'extension': 'rs',
        'sl_comm_chars' : '//',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    }, 
    'Racket' : {
        'extension': 'rkt',
        'sl_comm_chars' : ';',
        'ml_comm_start' : '#|',
        'ml_comm_end' : '|#'
    },
    'PostgreSQL' : {
        'extension': 'sql',
        'sl_comm_chars' : '--',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'Pandas' : {
        'extension': 'py',
        'sl_comm_chars' : '#',
        'ml_comm_start' : '"""',
        'ml_comm_end' : '"""'
    },
    'Oracle' : {
        'extension': 'dbf',
        'sl_comm_chars' : '--',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    },
    'MS SQL Server' : {
        'extension': 'mdf',
        'sl_comm_chars' : '--',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    }, 
    'MySQL' : {
        'extension': 'sql',
        'sl_comm_chars' : '#',
        'ml_comm_start' : '/*',
        'ml_comm_end' : '*/'
    }
    
}

studyPlansNames = {
    'LeetCode 75' : {
        'titleSlug': 'leetcode-75',
        'allowedLanguages': allowedLanguages
    },
    'Top Interview 150' : {
        'titleSlug': 'top-interview-150',
        'allowedLanguages': allowedLanguages
    },
    'Binary Search' : {
        'titleSlug': 'binary-search',
        'allowedLanguages': allowedLanguages
    },
    'SQL 50' : {
        'titleSlug': 'top-sql-50',
        'allowedLanguages': queryLanguages
    },
    'Introduction to Pandas' : {
        'titleSlug': 'introduction-to-pandas',
        'allowedLanguages': {
            'Pandas' : {
                'extension': 'py',
                'sl_comm_chars' : '#',
                'ml_comm_start' : '"""',
                'ml_comm_end' : '"""'
            }
        },
    },
    '30 Days of Pandas' : {
        'titleSlug': '30-days-of-pandas',
        'allowedLanguages': queryLanguages,
    },
    '30 Days of JavaScript' : {
        'titleSlug': '30-days-of-javascript',
        'allowedLanguages': {
            'JavaScript' : {
                'extension': 'js',
                'sl_comm_chars' : '//',
                'ml_comm_start' : '/*',
                'ml_comm_end' : '*/'
            },
            'TypeScript' : {
                'extension': 'ts',
                'sl_comm_chars' : '//',
                'ml_comm_start' : '/*',
                'ml_comm_end' : '*/'
            }
        },
    },
    'Top 100 Liked' : {
        'titleSlug': 'top-100-liked',
        'allowedLanguages': allowedLanguages,
    }
}


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.studyPlans = {}

        self.studyPlansLabel = QtWidgets.QLabel(self.formatPlans() if len(self.studyPlans) > 0 else "No study plans.")

        self.studyPlansDropdownLabel = QtWidgets.QLabel("Supported study plans:")

        self.studyPlansDropdown = QtWidgets.QComboBox()
        self.studyPlansDropdown.addItems(studyPlansNames.keys())

        self.addPlanButton = QtWidgets.QPushButton("Add Study Plan")
        self.addPlanButton.clicked.connect(self.addPlan)

        self.languagesLayout = QtWidgets.QVBoxLayout()

        self.generateFilesButton = QtWidgets.QPushButton("Generate Files")
        self.generateFilesButton.clicked.connect(self.generateFiles)

        # self.progress_label = QtWidgets.QTextEdit(self)
        # self.progress_label.setReadOnly(True)
        # self.progress_label.setText("Generating files...\n")

        self.layout = QtWidgets.QVBoxLayout(self)
        
    @QtCore.Slot()
    def initializeApp(self):
        self.layout.addWidget(self.studyPlansLabel)
        self.layout.addWidget(self.studyPlansDropdownLabel)
        self.layout.addWidget(self.studyPlansDropdown)
        self.layout.addWidget(self.addPlanButton)
        self.layout.addLayout(self.languagesLayout)
        self.layout.addWidget(self.generateFilesButton)


    @QtCore.Slot()
    def addPlan(self):
        newPlan = self.studyPlansDropdown.currentText()
        if newPlan and newPlan not in self.studyPlans:
            self.studyPlans[newPlan] = None
            self.addLanguageSelector(newPlan)
            self.studyPlansLabel.setText(self.formatPlans())

    @QtCore.Slot()
    def addLanguageSelector(self, plan):
        # Create a dropdown for selecting language
        languageLabel = QtWidgets.QLabel(f"Select language for {plan}:")
        languageDropdown = QtWidgets.QComboBox()
        
        # Add all available languages
        languageDropdown.addItems(studyPlansNames[plan]["allowedLanguages"].keys())
        
        # Set a default language (e.g., English)
        defaultLanguage = "Python"
        index = languageDropdown.findText(defaultLanguage)
        if index != -1:  # Check if the language is found in the dropdown
            languageDropdown.setCurrentIndex(index)
        else:
            languageDropdown.setCurrentIndex(0)  # Fallback to the first item
        
        # Set the default selection in the languageSelections dictionary
        self.studyPlans[plan] = languageDropdown.currentText()

        # Update the selection when the user changes the dropdown value
        languageDropdown.currentTextChanged.connect(lambda lang: self.updateLanguageSelection(plan, lang))

        # Add the dropdown and label to the layout
        self.languagesLayout.addWidget(languageLabel)
        self.languagesLayout.addWidget(languageDropdown)

    @QtCore.Slot()
    def updateLanguageSelection(self, plan, lang):
        self.studyPlans[plan] = lang

    @QtCore.Slot()
    def formatPlans(self):
        savedString = "Saved Plans: "
        for index, plan in enumerate(self.studyPlans):
            if index == 0:
                savedString += f"{plan}"
            else:
                savedString += f", {plan}"
        return savedString


    @QtCore.Slot()
    def generateFiles(self):
        self.clear_layout(self.layout)
        # while self.layout.count():
        #     child = self.layout.takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()

        self.progress_label = QtWidgets.QTextEdit(self)
        self.progress_label.setReadOnly(True)
        self.progress_label.setText("Generating files...\n")

        self.layout.addWidget(self.progress_label)

        generateFiles(self, self.studyPlans)


        

    @QtCore.Slot()
    def updateProgress(self, message):
        current_text = self.progress_label.toPlainText()
        self.progress_label.setText(current_text + message + "\n")

    @QtCore.Slot()
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())
                child.layout().deleteLater()

# currently unused 
def getStudyplansFromUser(study_plans_names, allowed_languages):
    print(
        """Welcome! \nPlease enter the LeetCode study plans you would like to work on!
        Note: You must enter the study plan name exactly as it shows up on LeetCode
            Valid Study Plans: 'LeetCode 75'; 'Binary Search'; '30 Days of JavaScript'
            Invalid Study Plans: 'leetcode75'; 'binary search'; '30 Days of Js'
        
        """
    )
    study_plans = {}
    usr_res = str(input("What would you like to study (q to quit): "))
    while (usr_res != 'q'):
        try:
            curr_study_plan = study_plans_names[usr_res]

            language = str(input(f"Which programming language would you like to study '{usr_res}' in?\nValid Programming Languages ('C++', 'Java', 'Python', 'Python3', 'C', 'C#', 'JavaScript', 'TypeScript', 'PHP', 'Swift', 'Kotlin', 'Go', 'Ruby', 'Scala', 'Rust', 'Racket'): "))
            while (language not in list(allowed_languages.keys())):
                language = str(input(f"Invalid Language. \nValid Programming Languages ('C++', 'Java', 'Python', 'Python3', 'C', 'C#', 'JavaScript', 'TypeScript', 'PHP', 'Swift', 'Kotlin', 'Go', 'Ruby', 'Scala', 'Rust', 'Racket'): "))

            study_plans[usr_res] = language
            print(f"Succesfully Added: '{usr_res}' with language {language}.")
        except KeyError:
            print(f"Could not add '{usr_res}'. We may not support that study plan at this moment or your spelling is incorrect.")
        usr_res = str(input("What would you like to study (q to quit): "))
    print("\n+-------------------------------------------------------------------------------------+\n")
    return study_plans
    

def getProblemInfo(curr_lang, problem_slug, problem_url, allowed_languages):
    data = {"operationName":"questionData","variables":{"titleSlug":f"{problem_slug}"},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

    r = requests.post('https://leetcode.com/graphql', json = data).json()
    if (r['data']['question']['isPaidOnly']):
        return ""
    soup = BeautifulSoup(r['data']['question']['content'], 'lxml')

    title = r['data']['question']['title'] # title 

    code_snippet_array = r['data']['question']['codeSnippets']

    code_snippet = None # code snippet 
    for code_snip_dict in code_snippet_array:
        if (code_snip_dict['lang'] == curr_lang):
            code_snippet = code_snip_dict['code'] # code snippet

    if (not code_snippet):
        alt_langs = [code_snip_dict['lang'] for code_snip_dict in code_snippet_array]
        print(f"We could not generate the problem '{title}' with the language '{curr_lang}', please choose one of the following:")
        print(alt_langs)
        choice = str(input("Which language would you like to use instead?: "))
        while (choice not in alt_langs):
            choice = input("Invalid Language, choose another one:")
        
        curr_lang = choice
    
    for code_snip_dict in code_snippet_array:
        if (code_snip_dict['lang'] == curr_lang):
            code_snippet = code_snip_dict['code'] # code snippet

    
    question = soup.get_text() # question

    file_content = f"{allowed_languages[curr_lang]['ml_comm_start']}\n{problem_url}\n\n\n{title}\n\n{question}\n{allowed_languages[curr_lang]['ml_comm_end']}\n{code_snippet}"
    
    return {
        'content' : file_content,
        'extension' : allowedLanguages[curr_lang]['extension']
    }
    

def formatSubgroupName(raw_subgroup):
    raw_subgroup = raw_subgroup.strip()
    raw_subgroup = raw_subgroup.replace(" ", "")
    formatted_subgroup = raw_subgroup.replace("/","-")
    return formatted_subgroup

def formatProblemUrl(problem_slug):
    return f"https://leetcode.com/problems/{problem_slug}/description/"


# def generateFiles(study_plans):
def generateFiles(gui, study_plans):
    
    dr = webdriver.Chrome() 

    parent_dir = os.getcwd()

    for study_plan in study_plans:
        curr_lang = study_plans[study_plan]
        studyplan_slug = studyPlansNames[study_plan]['titleSlug']

        dr.get(f"https://leetcode.com/studyplan/{studyplan_slug}/")
        soup = BeautifulSoup(dr.page_source, "lxml")
        unfiltered_problems = soup.find('script', id="__NEXT_DATA__").text

        


        # inner page (where the problems are) as json
        page_json = json.loads(unfiltered_problems)

        # subgroups list (holds problems in dictionaries )
        subgroups_list = page_json['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']["studyPlanV2Detail"]["planSubGroups"]

        try:
            os.mkdir(studyplan_slug)
        except FileExistsError:
            # print(f"A directory with the name '{studyplan_slug}' already exists. Going to the next study plan.")
            gui.updateProgress(f"A directory with the name '{studyplan_slug}' already exists. Going to the next study plan.")
            continue


        gui.updateProgress(f"Creating {studyplan_slug}/...")
        os.chdir(f"{parent_dir}/{studyplan_slug}")

        for subgroup in subgroups_list:
            subgroup_dir_name = formatSubgroupName(subgroup['name']) 
            os.mkdir(subgroup_dir_name)
            gui.updateProgress(f"\tCreating {studyplan_slug}/{subgroup_dir_name}/...")
            os.chdir(f"{parent_dir}/{studyplan_slug}/{subgroup_dir_name}")

            for question in subgroup['questions']:
                problem_slug = question['titleSlug']
                problem_url = formatProblemUrl(problem_slug)

                #start 

                # if (problem_url == "https://leetcode.com/problems/the-number-of-rich-customers/description/"):
                #     pass

                data = {"operationName":"questionData","variables":{"titleSlug":f"{problem_slug}"},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}

                r = requests.post('https://leetcode.com/graphql', json = data).json()
                if (r['data']['question']['isPaidOnly']):
                    gui.updateProgress(f'Failed to fetch data from \'{problem_url}\', you must pay for this problem.')
                    continue
                    
                soup = BeautifulSoup(r['data']['question']['content'], 'lxml')

                title = r['data']['question']['title'] # title 

                code_snippet_array = r['data']['question']['codeSnippets']

                code_snippet = None # code snippet 
                for code_snip_dict in code_snippet_array:
                    if (code_snip_dict['lang'] == curr_lang):
                        code_snippet = code_snip_dict['code'] # code snippet

                file_content_raw = None
                file_content = None
                if (not code_snippet):
                    alt_langs = [code_snip_dict['lang'] for code_snip_dict in code_snippet_array]
                    gui.updateProgress(f"We could not generate the problem '{title}' with the language '{curr_lang}', please choose one of the following:")
                    gui.updateProgress(alt_langs)
                    choice = str(input("Which language would you like to use instead?: "))
                    while (choice not in alt_langs):
                        choice = input("Invalid Language, choose another one:")
                    
                    memorize_lang = input("Would you like to use this language for the rest of the study plan? (y/n): ").lower()
                    while (not(memorize_lang == "y" or memorize_lang == "n")):
                        memorize_lang = input("Invalid Input, memorize language? (y/n): ").lower()
                    curr_lang = choice if memorize_lang == "y" else curr_lang

                    temp_lang = choice
                
                    for code_snip_dict in code_snippet_array:
                        if (code_snip_dict['lang'] == temp_lang):
                            code_snippet = code_snip_dict['code'] # code snippet

                    question = soup.get_text() # question
                    file_content_raw = f"{allowedLanguages[temp_lang]['ml_comm_start']}\n{problem_url}\n\n\n{title}\n\n{question}\n{allowedLanguages[temp_lang]['ml_comm_end']}\n{code_snippet}"
                    file_content = {
                        'content' : file_content_raw,
                        'extension' : allowedLanguages[temp_lang]['extension']
                    }
                else:
                    question = soup.get_text() # question
                    file_content_raw = f"{allowedLanguages[curr_lang]['ml_comm_start']}\n{problem_url}\n\n\n{title}\n\n{question}\n{allowedLanguages[curr_lang]['ml_comm_end']}\n{code_snippet}"
                    file_content = {
                        'content' : file_content_raw,
                        'extension' : allowedLanguages[curr_lang]['extension']
                    }


                question = soup.get_text() # question


                #end            

                if (file_content != ""):
                    gui.updateProgress(f"\t\tCreating {studyplan_slug}/{subgroup_dir_name}/{problem_slug}.{file_content['extension']}...")
                    with open(f"{problem_slug}.{file_content['extension']}", 'w') as file:
                        file.write(file_content['content'])
                else:
                    gui.updateProgress("something went wrong")

            child_dir = os.getcwd()
            os.chdir(f"{parent_dir}/{studyplan_slug}")

            if (os.listdir(child_dir) == []):
                shutil.rmtree(child_dir)
        
        os.chdir(parent_dir)
        gui.updateProgress("\n+" + ('-' * 190) + "+\n")

    gui.updateProgress("All Done! Happy Coding!\n")

def main():     
    
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 150)
    widget.show()
    widget.initializeApp()

    sys.exit(app.exec())
    

if __name__ == "__main__":
    main()