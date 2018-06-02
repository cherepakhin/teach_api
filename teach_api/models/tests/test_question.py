import pytest
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import Question


class QuestionTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_questions')
  def test_model_sets_n_automatically(self):
    question = Question(feature_n=3, txt='CONTENT31', answer_n=311)
    Session.add(question)
    Session.flush()
    assert question.answer_n == 311

    questions = Session.query(Question).filter(Question.feature_n == 3).all()
    assert len(questions) == 1
