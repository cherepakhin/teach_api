import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.answer.answer_view import AnswerView


class AnswerViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 211
    response = AnswerView(context, request).get()
    self.assertEqual(response.get('n'), 211)
    self.assertEqual(response.get('txt'), 'CONTENT211')

  @pytest.mark.usefixtures('fix_questions')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 211
    response = AnswerView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  @pytest.mark.usefixtures('fix_questions')
  def test_update(self):
    request = testing.DummyRequest(json_body={'txt': 'NEW_NAME'})
    context = testing.DummyResource()
    context.n = 211
    response = AnswerView(context, request).update()
    self.assertEqual(response.get('n'), 211)
    self.assertEqual(response.get('txt'), 'NEW_NAME')
