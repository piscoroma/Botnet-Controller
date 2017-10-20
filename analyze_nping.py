import glob
import os

if __name__== "__main__":

   files = glob.glob("client_output/*")
   n = len(files)
   print("N files: " + str(n))
   i = 0
   for file in files:
      i += 1
      if os.path.isfile(file):
         print("Scanning file ("+str(i)+"/"+str(n)+"): " + file + "...")
         try:
            with open(file, 'r') as log_file:
               lines = log_file.readlines()
               log_file.close()
         except Exception as e:
            raise IOError("Error during the reading of file: " + file + "\n" + str(e))

         last_rcvd = None
         for line in lines:
            values = line.split(' ')
            if values[0].__eq__("RCVD"):
               last_rcvd = line
         print(last_rcvd)

