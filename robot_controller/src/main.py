# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Aprende e Ingenia                                            #
# 	Created:      3/24/2024, 9:51:26 PM                                        #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #
#vex:disable=repl

# Module pid
class PIDControl:
    def __init__(self, kp=30.0, ki=0.5, kd=10) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
        self.max_error_x = 600
        self.max_error_z = 22000
        self.max_speed = 100
        pass
    
    def pid_control(self, error, max_error_type) -> float:
        if error == 0:
           output = 0.0
           return output
        
        if max_error_type == 'x':
          error_normalized = self.normalize_error(error, self.max_error_x)
        else:
           error_normalized = self.normalize_error(error, self.max_error_z)
           
        self.integral += error_normalized
        derivative = error_normalized - self.prev_error
        output = self.kp * error_normalized + self.ki * self.integral + self.kd * derivative
        self.prev_error_x = error_normalized
        return output
    
    def normalize_error(self, error, max_error):
        return error / max_error




import struct




        
