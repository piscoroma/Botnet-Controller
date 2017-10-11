import os
import logging

class Bash():
    def __init__(self, command):
        command = command + " 2>&1"
        self.pipe = os.popen(command)
        self.output = self.pipe.read()
        self.exit_code = self.pipe.close()
        if self.exit_code is not None:
            logging.debug ("Error code: "+str(self.exit_code)+" -Due to command: "+str(command)+" - Message: "+self.output)
    
    def get_output(self):
        return self.output


