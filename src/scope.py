class Scope():
    """
        List of dictionaries to save name->type.
        This class represents an stack of environments.
        Each dictionary represents an environment.
    """

    def __init__(self):
        self.store = [dict()]

    def get(self, key):
        for item in self.store[::-1]:
            if key in item:
                return item[key]
        raise KeyError(key)

    def add(self, key, value):
        self.store[-1][key] = value

    def remove(self, key):
        del self.store[-1][key]

    def new(self):
        self.store.append(dict())

    def destroy(self):
        del self.store[-1]


if __name__ == '__main__':
    scope = Scope()
    scope.add('Main', ('Int', 'Int'))
    print(scope.store)
    scope.remove('Main')
    print(scope.store)
    scope.new()
    print(scope.store)
    scope.destroy()
    print(scope.store)
