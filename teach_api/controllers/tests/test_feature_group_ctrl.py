import pytest

# from pyramid_sqlalchemy import Session
from teach_api.tests.base_test_db import BaseTestDB

from teach_api.models import FeatureGroup
from teach_api.controllers.feature_group_ctrl import FeatureGroupCtrl
from teach_api.controllers.feature_ctrl import FeatureCtrl


class FeatureGroupCtrlTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_find_by_name(self):
    feature_group = FeatureGroupCtrl.find_by_name('group11')
    self.assertEqual(feature_group.n, 11)
    self.assertEqual(feature_group.name, 'group11')

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_find_by_like_name(self):
    feature_groups = FeatureGroupCtrl.find_by_like_name('group')
    assert len(feature_groups) == 2

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_find_by_name_exception(self):
    with pytest.raises(Exception) as e:
      FeatureGroupCtrl.find_by_name('NAME1')
    assert 'FeatureGroup not found' in str(e.value)

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_feature_groups')
  def test_create_parent_is_none(self):
    feature_group = FeatureGroupCtrl.create(parent_n=None, name='NAME1')
    self.assertEqual(feature_group.n, 12)
    self.assertEqual(feature_group.name, 'NAME1')
    self.assertEqual(feature_group.parent_n, None)

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_create_parent_not_none(self):
    feature_group = FeatureGroupCtrl.create(parent_n=1, name='NAME1')
    self.assertEqual(feature_group.n, 12)
    self.assertEqual(feature_group.name, 'NAME1')
    self.assertEqual(feature_group.parent_n, 1)
    parent = FeatureGroup.get(1)
    self.assertEqual(len(parent.children), 2)

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_delete_child(self):
    FeatureGroupCtrl.delete(n=11)
    parent = FeatureGroup.get(1)
    self.assertEqual(len(parent.children), 0)

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_delete_parent(self):
    # f_group = FeatureGroup.get(1)
    # print('\n')
    # print('before {}'.format(len(f_group.children)))
    FeatureGroupCtrl.delete(n=1)
    # Session.flush()
    feature_groups = FeatureGroupCtrl.find_by_like_name('')
    # print('after {}'.format(len(feature_groups)))
    # print('parent_n {}'.format(feature_groups[0].parent_n))
    assert len(feature_groups) == 0

  @pytest.mark.usefixtures('fix_features')
  def test_delete_with_features(self):
    FeatureGroupCtrl.delete(n=1)
    # feature_groups = FeatureGroupCtrl.find_by_like_name('')
    # print('\nafter {}'.format(len(feature_groups)))
    features = FeatureCtrl.find_by_like_name('')
    assert len(features) == 1
    assert len(features[0].feature_group) == 0

  def test_simple_intersection(self):
    big = [1, 2, 3, 4]
    small = [2, 3]
    result = list(set(big) - set(small))
    assert result == [1, 4]

  def test_intersection(self):
    big = [
        {'n': 1, 'name': 'name1'},
        {'n': 2, 'name': 'name2'},
        {'n': 3, 'name': 'name3'},
        {'n': 4, 'name': 'name4'},
    ]

    small = [
        {'n': 2, 'name': 'name2'},
        {'n': 3, 'name': 'name3'},
        {'n': 5, 'name': 'name5'},
    ]
    a_small = [x['n'] for x in small]
    a_big = [x['n'] for x in big]
    print(a_small)
    result = list(set(a_big) - set(a_small))
    assert result == [1, 4]
    result = list(set(a_small) - set(a_big))
    assert result == [5]

  @pytest.mark.usefixtures('fix_features')
  def test_update(self):
    feature_group = FeatureGroupCtrl.update(n=1, name='GROUP1')
    assert feature_group.n == 1
    assert feature_group.name == 'GROUP1'

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_find_by_name_root(self):
    feature_group = FeatureGroupCtrl.find_by_name('group1')
    self.assertEqual(feature_group.n, 1)
    self.assertEqual(feature_group.name, 'group1')
    self.assertEqual(feature_group.parent_n, None)
    # print(feature_group.parent_n)

  @pytest.mark.usefixtures('fix_many_feature_groups')
  def test_get_root(self):
    feature_groups = FeatureGroupCtrl.get_root()
    assert len(feature_groups) == 2
    assert len(feature_groups[0].children) == 2
    assert len(feature_groups[1].children) == 1
