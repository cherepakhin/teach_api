from datetime import date
from pyramid_sqlalchemy import Session
from pydash import find
from teach_api.models import Feature, Question, Answer, FeatureGroup


class FeatureCtrl(object):
  """docstring for FeatureCtrl"""

  def __init__(self, arg):
    super(FeatureCtrl, self).__init__()
    self.arg = arg

  @staticmethod
  def find(params):
    q = Session.query(Feature)
    if 'name' in params and params['name'] != '':
      q = q.filter(
          Feature.name.ilike('%' + params['name'] + '%'))

    result = {}
    result['count_rows'] = q.count()

    rows_per_page = 10
    if 'rows_per_page' in params:
      rows_per_page = int(params['rows_per_page'])

    start_row = 0
    if 'start_row' in params:
      start_row = int(params['start_row'])

    q = q.slice(start_row, start_row + rows_per_page)

    result['results'] = q.all()
    return result

  @staticmethod
  def find_by_like_name(name):
    q = Session.query(Feature)

    q = q.filter(Feature.name.ilike('%' + name + '%'))
    features = q.all()
    return features

  @staticmethod
  def create_feature(params):
    feature = Feature()
    feature.name = params['name']
    feature.info = params['info']
    feature.info_profit = params['info_profit']
    feature.employee_n = params['employee_n']
    for feature_group in params['feature_group']:
      g = FeatureGroup.get(feature_group['n'])
      feature.feature_group.append(g)
    Session.add(feature)
    Session.flush()
    return feature

  @staticmethod
  def create_answer(question, params):
    if 'txt' in params and params['txt'] != '':
      answer = Answer()
      answer.txt = params['txt']
      answer.question_n = question.n
      Session.add(answer)
      Session.flush()
      return answer

  @staticmethod
  def create_question(feature, params):
    question = Question()
    question.txt = params['txt']
    question.feature_n = feature.n
    Session.add(question)
    answer_n = params['answer_n']
    Session.flush()
    if 'answers' in params:
      for answer_params in params['answers']:
        answer = FeatureCtrl.create_answer(question, answer_params)
        if answer is not None and answer_params['n'] == answer_n:
          question.answer_n = answer.n
          Session.flush()
        # print(answer_params)
    return question

  @staticmethod
  def create(params):
    # print(params)
    if 'name' in params and 'info' in params \
            and 'info_profit' in params and 'feature_group' in params \
            and 'employee_n' in params:
      feature = FeatureCtrl.create_feature(params)
      if 'questions' in params:
        questions = params['questions']
        for question in questions:
          FeatureCtrl.create_question(feature, question)
          # print(question)
      return feature
    else:
      raise Exception('Empty params for create feature.')

  @staticmethod
  def update_answer(question, answers_params):
    for answer_param in answers_params:
      n = answer_param['n']
      if n <= 0:
        FeatureCtrl.create_answer(question, answer_param)
      else:
        q = Session.query(Answer).filter(Answer.n == n)
        if 'txt' in answer_param:
          q.update({'txt': answer_param['txt']})

    # Удаление пустых вопросов
    for answer_param in answers_params:
      if 'n' in answer_param and n > 0 and \
              'txt' in answer_param and answer_param['txt'].strip() == '':
        n = answer_param['n']
        # print('delete answer %s' % (n,))
        Session.query(Answer).filter(Answer.n == n).delete()

    answers = Session.query(Answer).filter(
        Answer.question_n == question.n).all()
    for answer in answers:
      test_answer = find(answers_params, {'n': answer.n})
      if test_answer is None:
        # print('delete answer %s' % (answer.n,))
        Session.query(Answer).filter(Answer.n == answer.n).delete()

  @staticmethod
  def update_question(feature, questions_params):
    # print(questions_params)
    for question_param in questions_params:
      n = question_param['n']
      if n <= 0:
        FeatureCtrl.create_question(feature, question_param)
      else:
        q = Session.query(Question).filter(Question.n == n)
        if 'txt' in question_param:
          q.update({'txt': question_param['txt']})
        if 'answer_n' in question_param:
          q.update({'answer_n': question_param['answer_n']})
        question = Question.get(n)
        if 'answers' in question_param:
          FeatureCtrl.update_answer(question, question_param['answers'])
      return feature

  @staticmethod
  def update_feature_group(feature, feature_group_params):
    feature.feature_group = []
    for feature_group in feature_group_params:
      n = feature_group['n']
      feature_group = FeatureGroup.get(n)
      feature.feature_group.append(feature_group)
    return feature

  @staticmethod
  def update(n, params):
    q = Session.query(Feature).filter(Feature.n == n)
    q.update({'ddate': date.today()})
    if 'name' in params:
      q.update({'name': params['name']})
    if 'info' in params:
      q.update({'info': params['info']})
    if 'info_profit' in params:
      q.update({'info_profit': params['info_profit']})
    if 'employee_n' in params:
      q.update({'employee_n': params['employee_n']})
    feature = Feature.get(n)
    if 'questions' in params:
      FeatureCtrl.update_question(feature, params['questions'])
    if 'feature_group' in params:
      feature = FeatureCtrl.update_feature_group(
          feature, params['feature_group'])
    return feature
