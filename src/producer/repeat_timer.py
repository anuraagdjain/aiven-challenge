# Source: https://brandonrozek.com/blog/pythonsetinterval/
from threading import Timer


class Repeat(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
