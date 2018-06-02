import pytest
from pyramid import testing
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.question.question_view import QuestionView


class QuestionViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_get(self):
    # Session.flush()
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 21
    response = QuestionView(context, request).get()
    self.assertEqual(response.get('n'), 21)
    self.assertEqual(response.get('feature_n'), 2)
    self.assertEqual(response.get('txt'), 'CONTENT21')
    answers = response.get('answers')
    assert len(answers) == 3

  @pytest.mark.usefixtures('fix_questions')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 21
    response = QuestionView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_update(self):
    request = testing.DummyRequest(json_body={'txt': 'NEW_TXT'})
    context = testing.DummyResource()
    context.n = 21
    response = QuestionView(context, request).update()
    self.assertEqual(response.get('n'), 21)
    self.assertEqual(response.get('txt'), 'NEW_TXT')
