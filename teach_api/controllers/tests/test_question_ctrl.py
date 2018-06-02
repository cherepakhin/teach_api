import pytest
from datetime import date

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.question_ctrl import QuestionCtrl
from teach_api.controllers.plan_ctrl import PlanCtrl
from teach_api.models import Employee

today = date.today()


class QuestionCtrlTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_rest')
  def test_get_next(self):
    question = QuestionCtrl.get_next('NAME_1')
    self.assertEqual(question.n, 31)

  @pytest.mark.usefixtures('fix_results')
  def test_get_next_for_exist_today_result(self):
    question = QuestionCtrl.get_next('NAME')
    self.assertEqual(question.n, 0)

  def test_devide(self):
    a = 10
    b = 3
    assert (a // b) == 3

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_generate')
  # В фикстурах отвечено на ОДИН из ТРЕХ вопросов СЕГОДНЯ
  # Employee.n = (1,2,3)
  def test_generate_question_plan_finished(self):
    """
    Месячный план ВЫПОЛНЕН
    """
    employee = Employee.get(1)
    PlanCtrl.create(employee.n, today.year, today.month, 1, 1)

    question = QuestionCtrl.generate_question(employee.name)
    assert question.n == 0  # question.n=0 пустой вопрос, означает нет вопроса

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_generate')
  # В фикстурах отвечено на ОДИН из ТРЕХ вопросов СЕГОДНЯ
  # Employee.n = (1,2,3)
  def test_generate_question_plan_not_finished(self):
    """
    Месячный план НЕ ВЫПОЛНЕН
    """
    employee = Employee.get(1)
    PlanCtrl.create(employee.n, today.year, today.month, 1, 2)

    question = QuestionCtrl.generate_question(employee.name)
    # print(question)
    assert question.n != 0  # question.n=0 пустой вопрос, означает нет вопроса
    ANSWERED_QUESTION_N = 21  # номер отвеченного вопроса из фикстуры
    assert question.n != ANSWERED_QUESTION_N

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_generate')
  # В фикстурах отвечено на ОДИН из ТРЕХ вопросов СЕГОДНЯ
  # Employee.n = (1,2,3)
  def test_generate_question_day_finish(self):
    """
    План НЕ ВЫПОЛНЕН. Дневной план ВЫПОЛНЕН
    """
    employee = Employee.get(1)
    PlanCtrl.create(employee.n, today.year, today.month, 2, 1)

    question = QuestionCtrl.generate_question(employee.name)
    # print(question)
    assert question.n == 0  # question.n=0 пустой вопрос, означает нет вопроса

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_generate')
  # В фикстурах отвечено на ОДИН из ТРЕХ вопросов СЕГОДНЯ
  # Employee.n = (1,2,3)
  def test_generate_question_day_not_finish(self):
    """
    План НЕ ВЫПОЛНЕН. Дневной план НЕ ВЫПОЛНЕН
    """
    employee = Employee.get(1)
    PlanCtrl.create(employee.n, today.year, today.month, 2, 3)

    question = QuestionCtrl.generate_question(employee.name)
    # print(question)
    assert question.n != 0  # question.n=0 пустой вопрос, означает нет вопроса
    ANSWERED_QUESTION_N = 21  # номер отвеченного вопроса из фикстуры
    assert question.n != ANSWERED_QUESTION_N

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_repeat')
  def test_repeat_question(self):
    employee = Employee.get(1)
    question = QuestionCtrl.get_repeat(employee)
    assert question.n == 31
