import json

from .atest_mdt import AViewTest


class LoginRestTest(AViewTest):

  # @pytest.mark.skip
  def test_login_post(self):
    res = self.testapp.post(
        '/v1/login/', json.dumps({'name': 'NAME', 'password': 'password'}), status=200)
    self.assertTrue(len(res.json.get('token')) > 0)
    # print(res.json.get('token'))
