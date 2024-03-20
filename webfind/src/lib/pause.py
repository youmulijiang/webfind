import threading

class Pause():
    def __init__(self) -> None:
        self._threads = []
        self._play_event = threading.Event()
        self._quit_event = threading.Event()
        self._pause_semaphore = threading.Semaphore(0)
    
    def pause(self):
        print("正在退出程序,清除子线程中")
        self._play_event.clear()  
        for thread in self._threads:
            if thread.is_alive():
                self._pause_semaphore.acquire()