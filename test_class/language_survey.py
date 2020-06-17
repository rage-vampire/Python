# -*- coding:utf-8 -*-
# Filename: language_survey.py
# Author: Lizi
# Time: 2019/12/22 11:10

from survey import AnonymousSurvey



question = "What language did you first learn to speak?"
my_survey = AnonymousSurvey(question)
my_survey.show_questions()

while True:
    response = input("Language: ")
    if response == 'q':
        break
    my_survey.show_responses(response)

my_survey.show_result()

