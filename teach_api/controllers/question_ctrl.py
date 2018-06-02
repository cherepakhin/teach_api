from datetime import date

from sqlalchemy import not_, func
from pyramid_sqlalchemy import Session
from teach_api.models import Question, Result
from teach_api.controllers.employee_ctrl import EmployeeCtrl
from teach_api.controllers.plan_ctrl import PlanCtrl
from teach_api.controllers.result_ctrl import ResultCtrl


class QuestionCtrl(object):

  def __init__(self, arg):
    super(QuestionCtrl, self).__init__()

  @staticmethod
  def get_next(employee_name):
    """
    Получение следующего вопроса для сотрудника
    """
    null_question = Question(n=0)
    employee = EmployeeCtrl.find_by_name(employee_name)
    today_results = Session.query(Result).filter(
        Result.ddate == date.today()).all()
    if len(today_results) > 0:
      return null_question
    subquery = Session.query(Result.question_n).filter(
        Result.employee_n == employee.n)
    q = Session.query(Question).filter(not_(Question.n.in_(subquery)))
    questions = q.all()
    if len(questions) == 0:
      return null_question
    return questions[0]

  @staticmethod
  def get_repeat(employee):
    """
    Получение вопроса среди уже отвеченных,
    в случае когда на все вопросы уже ответили,
    но по плану нужно еще задать. Т.е. вопросы задаются повторно.
    """
    result = Session.query(Result.question_n).filter(
        Result.employee_n == employee.n, Result.question_n == Question.n).group_by(
        Result.question_n).order_by(func.count()).first()

    question = Question.get(result.question_n)
    return question

  @staticmethod
  def generate_question(employee_name):
    """
    Получение след.вопроса в зависимости от плана и уже отвеченных вопросов
    """
    null_question = Question(n=0)
    today = date.today()
    year = today.year
    month = today.month
    employee = EmployeeCtrl.find_by_name(employee_name)
    plan = PlanCtrl.get_current_plan(employee_name, year, month)
    qty_answered = ResultCtrl.count_answered(
        employee, year, month)  # уже отвечено
    if plan.qty_question > qty_answered:
      qty_day = plan.qty_question // plan.qty_work + 1  # к-во вопросов в день
      # print('qty_day = %s' % (qty_day,))
      # print(plan)
      params = {
          'employee_n': employee.n,
          'date': today
      }
      results = ResultCtrl.find(params)  # отвечено сегодня
      # print('results = %s' % (results,))
      if len(results) < qty_day:  # если план на день еще не выполнен
        subquery = Session.query(Result.question_n).filter(
            Result.employee_n == employee.n)
        q = Session.query(Question).filter(not_(Question.n.in_(subquery)))
        questions = q.all()
        # print(questions)
        if len(questions) == 0 or questions is None:
          return QuestionCtrl.get_repeat(employee)
        return questions[0]
      else:
        return null_question
    else:
      # План по вопросам сделан
      return null_question
