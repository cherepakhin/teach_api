from pyramid_sqlalchemy import Session


class GetByEqName(object):

  @classmethod
  def get_by_eq_name(cls, name):
    entities = Session.query(cls).filter(
        cls.name == name).all()
    if len(entities) == 1:
      return entities[0]

    raise Exception('Entities with name=' + name + ' not alone')


class AEntity:
  """
  Абстрактный класс для реализации CRUD
  """
  @classmethod
  def get(cls, n):
    entity = Session.query(cls).filter(cls.n == n).one()
    return entity

  @classmethod
  def create(cls, params):
    # print('params=%s' % (params,))
    entity = cls(**params)
    Session.add(entity)
    Session.flush()
    return entity

  @classmethod
  def delete(cls, n):
    Session.query(cls).filter(cls.n == n).delete()
    Session.flush()

  @classmethod
  def update(cls, n, params):
    if params == {}:
      raise Exception('Empty params' + cls)
    Session.query(cls).filter(cls.n == n).update(params)
    entity = cls.get(n)
    return entity
