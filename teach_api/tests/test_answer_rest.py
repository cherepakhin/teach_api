import pytest
import json
from pyramid_sqlalchemy import Session

from teach_api.models import Answer
from .atest_mdt import AViewTest


class AnswerRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_questions')
  def test_answer_get(self):
    res = self.testapp.get('/v1/answer/211/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 211)
    # print(res.json)
    self.assertEqual(res.json.get('txt'), 'CONTENT211')
    self.assertEqual(res.json.get('question_n'), 21)

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_answer_delete(self):
    res = self.testapp.delete(
        '/v1/answer/211/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    answers = Session.query(Answer).all()
    assert len(answers) == 2

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_answer_post(self):
    res = self.testapp.post('/v1/answer/211/',
                            json.dumps({'txt': 'NEW_NAME'}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('txt'), 'NEW_NAME')

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_answers_post(self):
    res = self.testapp.post('/v1/answer/',
                            json.dumps(
                                {'n': 214, 'question_n': 21, 'txt': 'CONTENT214'}),
                            headers=self.headers,
                            status=200)
    # self.assertEqual(res.json, {'n': 1})
    self.assertEqual(res.json.get('n'), 214)
    self.assertEqual(res.json.get('question_n'), 21)
    self.assertEqual(res.json.get('txt'), 'CONTENT214')
