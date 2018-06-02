from datetime import datetime
import pytest
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import Result


class ResultTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_questions')
  def test_model_sets_n_automatically(self):
    result = Result(question_n=21,
                    answer_n=211,
                    employee_n=1,
                    is_correct=True,
                    time_begin=datetime(2018, 6, 1, 22, 23, 24),
                    time_end=datetime(2018, 6, 1, 22, 25, 25),
                    )
    Session.add(result)
    # Session.flush()
    # assert result.n is not None
    # print(result.duration)
    assert result.duration == '0:02:01'
    assert result.question_n == 21
    assert result.answer_n == 211
