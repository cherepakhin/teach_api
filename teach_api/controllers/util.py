def update_by_param(q, name_param, params):
  if name_param in params:
    q.update({name_param: params[name_param]})


def update_by_params(q, names, params):
  for name_param in names:
    update_by_param(q, name_param, params)
