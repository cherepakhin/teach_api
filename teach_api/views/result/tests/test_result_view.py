import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.result.result_view import ResultView


class ResultViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_results')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = ResultView(context, request).get()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('question_n'), 21)
    self.assertEqual(response.get('answer_n'), 211)
    self.assertEqual(response.get('employee_n'), 1)
    self.assertEqual(response.get('is_correct'), True)

  @pytest.mark.usefixtures('fix_results')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = ResultView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_results')
  def test_update(self):
    request = testing.DummyRequest(json_body={'is_correct': False})
    context = testing.DummyResource()
    context.n = 1
    response = ResultView(context, request).update()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('is_correct'), False)
