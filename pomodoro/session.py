'''
NOTE: session is more than jsut a timer, it alternates between work and break for however many iterations
'''
from pomodoro.timer import Timer

class PomodoroSession:

    def __init__(self, work_duration, break_duration):
        self.work_timer = Timer(work_duration)
        self.break_timer = Timer(break_duration)
        self.current_phase = "work"
        self.completed_cycles = 0

    def start(self): 
        if self.current_phase == "work":
            self.work_timer.start()
        else:
            self.break_timer.start()
   
    def pause(self): 
        if self.current_phase == "work":
            self.work_timer.pause()
        else:
            self.break_timer.pause()
            
    def reset(self):
        self.work_timer.reset()
        self.break_timer.reset()
        self.current_phase = "work"
        self.completed_cycles = 0 

    def tick(self): 
        if self.current_phase == "work":
            self.work_timer.tick()

            if self.work_timer.remaining <=0:
                self.switch_phase()
        else:
            self.break_timer.tick()
            
            if self.break_timer.remaining <= 0:
                self.switch_phase()

    def switch_phase(self):
        if self.current_phase == "work":
            self.current_phase = "break"
            self.break_timer.reset()
            self.break_timer.start()
            self.completed_cycles +=1

        else:
            self.current_phase = "work"
            self.work_timer.reset()
            self.work_timer.start()
    
    def get_status(self):
        if self.current_phase == "work":
            return{
                "phase": "work",
                "remaining" : self.work_timer.remaining,
                "status" : self.work_timer.status
            }
        else:
            return{
                "phase": "break",
                "remaining": self.break_timer.remaining,
                "status": self.break_timer.status
            }
            
