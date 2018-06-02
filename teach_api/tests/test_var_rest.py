import pytest

from .atest_mdt import AViewTest


class VarRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_features')
  def test_var_get(self):
    res = self.testapp.get('/v1/var/',
                           headers=self.headers, status=200)
    # print(res.json)
    self.assertEqual(len(res.json.get('feature_groups')), 1)
