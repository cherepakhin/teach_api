import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.answer.answers_view import AnswersView


class AnswersViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_questions')
  def test_create(self):
    request = testing.DummyRequest(
        json_body={'n': 214, 'question_n': 21, 'txt': 'CONTENT214'})
    context = testing.DummyResource()
    response = AnswersView(context, request).post()
    self.assertEqual(response['n'], 214)
    self.assertEqual(response['txt'], 'CONTENT214')
    self.assertEqual(response['question_n'], 21)
