"""
Python clone of CPython implementation of python dictionary
"""


class DictItem:
    def __init__(self, h, k, v):
        self.key_hash = h
        self.key = k
        self.value = v


class Dict:
    def __init__(self):
        self.index_list = [None] * 8
        self.entries = []
        self.size = 0
        self.max_len = 8

    def _get_next_index(self, key_hash, k):
        seed = key_hash
        p = key_hash
        c = 0
        while True:
            possible_index = (5 * seed + 1 + p) % self.max_len
            actual_index = self.index_list[possible_index]
            if actual_index:
                if self.entries[actual_index].key == k:
                    return possible_index, True
            else:
                return possible_index, False
            seed = possible_index
            p >>= 5
            c += 1
            if c > self.max_len:
                break
        raise Exception("Something's wrong")

    def _resize(self, length):
        self.index_list = [None] * length
        self.max_len = length
        old_entries = self.entries[:]
        self.entries = []
        self.size = 0
        for di in old_entries:
            self.__setitem__(di.key, di.value)

    def _check_and_resize(self):
        if self.size >= (self.max_len * 2) // 3:
            self._resize(2 * self.max_len)

    def __setitem__(self, k, v):
        key_hash = hash(k)
        idx, exists = self._get_next_index(key_hash, k)
        actual_index = self.index_list[idx]
        if exists:
            self.entries[actual_index].value = v
            return
        di = DictItem(key_hash, k, v)
        self.entries.append(di)
        self.index_list[idx] = len(self.entries) - 1
        self.size += 1
        self._check_and_resize()

    def __getitem__(self, k):
        key_hash = hash(k)
        idx, exists = self._get_next_index(key_hash, k)
        actual_index = self.index_list[idx]
        if exists:
            return self.entries[actual_index].value
        raise KeyError(k)
    
    def __len__(self):
        return self.size
    
    def __repr__(self):
        repr = ""
        for k, v in self.items():
            repr += f"{k} - {v}\n"
        return repr
    
    def __str__(self):
        return self.__repr__()
    
    def __contains__(self, k):
        try:
            self.__getitem__(k)
            return True
        except KeyError:
            return False
        
    def __iter__(self):
        for di in self.entries:
            yield di.key

    def get(self, k, optional=None):
        try:
            return self.__getitem__(k)
        except KeyError:
            return None

    def keys(self):
        return [di.key for di in self.entries]

    def values(self):
        return [di.value for di in self.entries]

    def items(self):
        return [(di.key, di.value) for di in self.entries]
