import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.question.questions_view import QuestionsView


class QuestionsViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_questions')
  def test_create(self):
    request = testing.DummyRequest(json_body={
        'n': 31,
        'feature_n': 3,
        'txt': 'CONTENT31',
        'answer_n': 311})
    context = testing.DummyResource()
    response = QuestionsView(context, request).post()
    self.assertEqual(response['n'], 31)
    self.assertEqual(response['txt'], 'CONTENT31')
    self.assertEqual(response['feature_n'], 3)
