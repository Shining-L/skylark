import math

class Pagination:
    def __init__(self, current_page, all_count, limit):
        self.all_count = all_count
        self.limit = limit
        self.current_page = current_page
        
        self.page_count = math.ceil(all_count / limit)
        
    @property
    def start(self):
        return (self.current_page - 1) * self.limit
    
    @property
    def end(self):
        return self.current_page * self.limit
        