from multiprocessing import Condition, Lock 
from multiprocessing import Array, Manager, Value 

class Table():
    def __init__(self, NPHIL, manager):
        self.fforks = manager.list([True for _ in range(NPHIL)])
        self.mutex = Lock()
        self.free_fork = Condition(self.mutex)
        self.current_phil = None
        self.nphil = NPHIL

    def set_current_phil(self, phil):
        self.current_phil = phil
        
    def wants_eat(self, phil):
        self.mutex.acquire()
        self.free_fork.wait_for(self.free_forks)
        self.fforks[phil] = False
        self.fforks[(phil + 1) % self.nphil] = False
        self.mutex.release()

    
    def wants_think(self, phil):
        self.mutex.acquire()
        self.fforks[phil] = True
        self.fforks[(phil + 1) % self.nphil] = True
        self.free_fork.notify_all()
        self.mutex.release()

    def get_current_phil(self):
        return self.current_phil

    def are_free_forks(self):
        phil = self.current_phil
        return self.fforks[phil] and self.fforks[(phil + 1) % self.nphil]

    
  

