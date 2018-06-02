import pytest
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import FeatureGroup, Feature


class FeatureGroupTest(BaseTestDB):

  def test_model_sets_n_automatically(self):
    _group = FeatureGroup(name='NAME_FEATURE_GROUP')
    Session.add(_group)
    Session.flush()
    assert _group.n is not None
    assert _group.parent_n is None
    assert _group.name == 'NAME_FEATURE_GROUP'

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_parent(self):
    _group = FeatureGroup.get(11)
    assert _group.n == 11
    assert _group.parent_n == 1

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_childs(self):
    _group = FeatureGroup.get(1)
    assert _group.n == 1
    assert _group.parent_n is None
    assert len(_group.children) == 1
    assert _group.children[0].n == 11

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_add_childs(self):
    _group12 = FeatureGroup(n=13, name='NAME_FEATURE_GROUP', parent_n=1)
    Session.add(_group12)
    Session.flush()

    _group = FeatureGroup.get(1)
    assert len(_group.children) == 2
    assert _group.children[0].n == 13
    assert _group.children[1].n == 11

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_del_childs(self):
    _group11 = FeatureGroup.get(11)
    Session.delete(_group11)
    _group = FeatureGroup.get(1)
    assert len(_group.children) == 0

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_add_feature(self):
    _group11 = FeatureGroup.get(11)
    NAME_FEATURE = 'NAME_FEATURE'
    _feature = Feature(n=1, name=NAME_FEATURE, feature_group=[_group11])
    Session.add(_feature)
    assert _feature.n is not None
    assert len(_feature.feature_group) == 1

  @pytest.mark.usefixtures('fix_many_feature_groups')
  def test_get_child_with_parent(self):
    _group = FeatureGroup.get(11)
    assert _group.parent_name == 'group1'

    _group = FeatureGroup.get(1)
    assert _group.parent_name == ''
