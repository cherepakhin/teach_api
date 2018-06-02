import pytest
import json
from pyramid_sqlalchemy import Session

from teach_api.models import Question
from .atest_mdt import AViewTest


class QuestionRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_questions')
  def test_question_get(self):
    res = self.testapp.get('/v1/question/21/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 21)
    self.assertEqual(res.json.get('n'), 21)
    self.assertEqual(res.json.get('feature_n'), 2)
    self.assertEqual(res.json.get('txt'), 'CONTENT21')
    answers = res.json.get('answers')
    assert len(answers) == 3
    # print(res.json)

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_question_delete(self):
    res = self.testapp.delete(
        '/v1/question/21/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    questions = Session.query(Question).all()
    assert len(questions) == 0

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  @pytest.mark.usefixtures('fix_questions')
  def test_question_post(self):
    res = self.testapp.post('/v1/question/21/',
                            json.dumps({'txt': 'NEW_TXT'}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('txt'), 'NEW_TXT')

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_questions_post(self):
    res = self.testapp.post('/v1/question/',
                            json.dumps({'n': 31,
                                        'feature_n': 3,
                                        'txt': 'CONTENT31',
                                        'answer_n': 311
                                        }),
                            headers=self.headers,
                            status=200)
    # self.assertEqual(res.json, {'n': 1})
    self.assertEqual(res.json.get('n'), 31)
    self.assertEqual(res.json.get('txt'), 'CONTENT31')
