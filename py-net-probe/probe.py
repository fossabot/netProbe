# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-04-24 22:49:18 alex>
#

import logging
import subprocess
import time
import pprint

# -----------------------------------------
def restartProbe(jobName, probeProcess):
    """
    restart the probe (generally after config refresh
    """

    logging.info("restart probe {}".format(jobName))

    # stops the process
    
    if probeProcess.__contains__(jobName):
        p = probeProcess[jobName]['handler']
        
        # is the process stopped ?
        if p.poll() != None:
            logging.info("probe-{} already stopped".format(jobName))
        else:
            logging.info("send SIGTERM to probe {}".format(jobName))
            p.terminate()

            # wait at most for 5 seconds
            i = 10
            while p.poll() != None:
                time.sleep(0.5)
                i -= 1
                if i <= 0:
                    break
            if i>0:
                logging.info("probe {} stopped in {:0.1f}s".format(jobName, (10-i)*0.5))
            else:
                logging.error("probe {} not terminated".format(jobName))
                logging.warning("need to do something on the probe")

    # starts the probe process
    p = subprocess.Popen(["/usr/bin/python", "probe-{}.py".format(jobName)])
    if p == None:
        logging.error("need to handle subprocess failure")

    probeProcess[jobName] = { "handler" : p,
                              "started" : time.time()
                            }

    # pprint.pprint(probeProcess)

    logging.info("probe {} started".format(jobName))

# -----------------------------------------
def stopAllProbes(probeProcess):
    """
    stop all the probes
    """

    logging.info("stop all probes")

    for jobName in probeProcess.keys():
        probe = probeProcess[jobName]
        p = probe['handler']
        
        logging.info("send SIGTERM to probe {}".format(jobName))
        p.terminate()

        p.wait()

    logging.info("all probes are stoppped")