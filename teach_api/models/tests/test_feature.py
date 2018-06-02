import pytest
from pyramid_sqlalchemy import Session
from datetime import date

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import Feature, FeatureGroup


class FeatureTest(BaseTestDB):

  # @pytest.mark.usefixtures('fix_feature_groups')
  @pytest.mark.usefixtures('fix_features')
  def test_model_sets_n_automatically(self):
    feature = Feature(name='name_feature', employee_n=1)
    feature_group = FeatureGroup.get(1)
    feature.feature_group.append(feature_group)
    Session.add(feature)
    Session.flush()
    assert feature.n is not None
    assert feature.name == 'name_feature'
    assert feature.employee_n == 1
    assert feature.ddate == date.today()
