

class Game:

    def __init__(self, key):
        self._key = key
        self._state = "Initializing"
        self._map1 = None
        self._map2 = None
        self._previous_target = None
        self._hit_count1 = 0
        self._hit_count2 = 0


    def get_state(self):
        return self._state
    
    def set_state(self, new_state):
        self._state  = new_state


    def get_key(self):
        return self._key
    
    def set_key(self, new_key):
        self._key  = new_key


    def get_map1(self):
        return self._map1
    
    def set_map1(self, new_map):
        self._map1  = new_map


    def get_map2(self):
        return self._map2
    
    def set_map2(self, new_map):
        self._map2  = new_map


    def get_previous_target(self):
        return self._previous_target

    def set_previous_target(self, new_target):
        self._previous_target = new_target


    def increment_count1(self):
        self._hit_count1 += 1

    def increment_count2(self):
        self._hit_count2 += 1

    
    def get_count1(self):
        return self._hit_count1

    def get_count2(self):
        return self._hit_count2

    

    

    
