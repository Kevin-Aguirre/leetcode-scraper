import sys
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.studyPlans = ["letcode 75", "binary search", "foobar"]

        self.text = QtWidgets.QLabel(self.formatPlans() if len(self.studyPlans) > 0 else "No study plans.")
        
        self.addPlanButton = QtWidgets.QPushButton("Add Study Plan")
        self.addPlanButton.clicked.connect(self.addPlan)
        
        self.generateFilesButton = QtWidgets.QPushButton("Generate Files")

        self.input = QtWidgets.QLineEdit(self)
        self.input.setPlaceholderText("Enter Leetcode study plan here")



        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.addPlanButton)



    @QtCore.Slot()
    def addPlan(self):
        newPlan = self.input.text()
        if (newPlan):
            self.studyPlans.append(newPlan)
            self.text.setText(self.formatPlans())
            self.input.clear()
             

    @QtCore.Slot()
    def formatPlans(self):
        savedString = "Saved Plans:\n"
        for plan in self.studyPlans:
            savedString += f"\t- {plan}\n"
        return savedString

    @QtCore.Slot()
    def generateFiles(self):
        print('generating files')        



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()


    sys.exit(app.exec())