import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.result.results_view import ResultsView


class ResultsViewTest(BaseTestDB):

  # @pytest.mark.usefixtures('fix_questions')
  # @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results')
  def test_create(self):
    request = testing.DummyRequest(json_body={'n': 3, 'question_n': 31, 'answer_n': 311,
                                              'is_correct': True, 'employee_n': 1})
    context = testing.DummyResource()
    response = ResultsView(context, request).post()
    self.assertEqual(response['n'], 3)
    self.assertEqual(response['question_n'], 31)
    self.assertEqual(response['answer_n'], 311)
    self.assertEqual(response['is_correct'], True)
    self.assertEqual(response['employee_n'], 1)
