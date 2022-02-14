
def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


class ToJson:
    def __init__(self, top_dict):
        self.top_dict = top_dict

    def to_json(self):
        dict_json = {}
        for key, value in self.top_dict.items():
            keys = key.__dict__
            key_dict = {}
            for s, t in keys.items():
                key_dict[s] = t
                dict_json[value] = key_dict
        return dict_json

