# -*- coding:utf-8 -*-
# Filename: language_survey.py
# Author: Lizi
# Time: 2019/12/22 11:10

from survey import AnonymousSurvey
import unittest


class TestAnonymousSurvey(unittest.TestCase):
    def test_store_single_response(self):
        question = "What language did you first learn to speak?"
        my_survey = AnonymousSurvey(question)
        my_survey.show_responses('English')
        self.assertIn('English',my_survey.responses)

    def test_store_three_response(self):
        question = "What language did you first learn to speak?"
        my_survey = AnonymousSurvey(question)
        responses = ['English','Chinese','Spanish']
        for response in responses:
            my_survey.show_responses(response)

        for response in responses:
            self.assertIn(response,my_survey.responses)


    # def setUp(self):
    #     question = "What language did you first learn to speak?"
    #     self.my_survey = AnonymousSurvey(question)
    #     self.responses = ['English','Chinese','Spanish']
    #
    #
    # def test_store_single_response(self):
    #     self.my_survey.show_responses(self.responses[0])
    #     self.assertIn(self.responses[0],self.my_survey.responses)
    #
    # def test_store_three_response(self):
    #     for response in self.responses:
    #         my_survey.show_responses(response)
    #
    #     for response in self.responses:
    #         self.assertIn(response,self.my_survey.responses)
if __name__ == '__main__':
    unittest.main()