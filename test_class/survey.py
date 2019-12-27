# -*- coding:utf-8 -*-
# Filename: survey.py
# Author: Lizi
# Time: 2019/12/22 11:04

class AnonymousSurvey():
    def __init__(self,questions):
        self.questions = questions
        self.responses = []

    def show_questions(self):
        print(self.questions)

    def show_responses(self,new_responses):
        self.responses.append(new_responses)

    def show_result(self):
        print("Survey result: ")
        for response in self.responses:
            print(response.title())

