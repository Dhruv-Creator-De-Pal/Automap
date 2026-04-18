import subprocess
import os






def rootcheck():
    rchk=subprocess.run(["id","-u"], capture_output=True, text =True )
    if rchk.stdout == "0\n":
        print("root cheked ")
        return True
    else:
        print("there is the problem with permissions")
        return False


