# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2016-09-22 12:18:35 alex>
#

""" probe management module """

import logging
import subprocess
import time
import psutil
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
            if i > 0:
                logging.info("probe {} stopped in {:0.1f}s".format(jobName, (10-i)*0.5))
            else:
                logging.error("probe {} not terminated".format(jobName))
                logging.warning("need to do something on the probe")

    # starts the probe process
    p = subprocess.Popen(["/usr/bin/python", "probe-{}.py".format(jobName)])
    if p == None:
        logging.error("need to handle subprocess failure")

    probeProcess[jobName] = {"handler" : p,
                             "started" : time.time()}

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

# -----------------------------------------
def checkProbe(jobName, probeProcess):
    """
    check the probe for presence
    """

    logging.info("check probe {}".format(jobName))

    if probeProcess.__contains__(jobName):
        p = probeProcess[jobName]['handler']
        
        # is the process stopped ?
        if p.poll() != None:
            logging.info("probe-{} stopped, code {}".format(jobName, p.returncode))
            return False

    return True

# -----------------------------------------
def checkProbes(probeProcess):
    """ check all started probes
    """

    for k in probeProcess.keys():
        if checkProbe(k, probeProcess) == False:
            restartProbe(k, probeProcess)

# -----------------------------------------
def statsProbes(a):
    """
    gather stats from all started probes
    """

    (probeProcess, stats) = a

    for k in probeProcess.keys():
        if checkProbe(k, probeProcess) == True:
            statsProbe(k, probeProcess, stats)

# -----------------------------------------
def statsProbe(jobName, probeProcess, stats):
    """
    get stats for the job process in order to push these towards server
    """

    logging.info("gather stats for probe {}".format(jobName))

    if probeProcess.__contains__(jobName):
        pid = probeProcess[jobName]['handler'].pid
        p = psutil.Process(pid) # may raise error NoSuchProcess

        stats.setVar("stats-{}-{}".format(jobName, "create_time"), int(p.create_time()))
        stats.setVar("stats-{}-{}".format(jobName, "nice"), p.nice())

        a = p.io_counters()
        stats.setVar("stats-{}-{}".format(jobName, "io_read_count"), a[0])
        stats.setVar("stats-{}-{}".format(jobName, "io_write_count"),a[1])
        stats.setVar("stats-{}-{}".format(jobName, "io_read_bytes"), a[2])
        stats.setVar("stats-{}-{}".format(jobName, "io_write_bytes"), a[3])

        a = p.num_ctx_switches()
        stats.setVar("stats-{}-{}".format(jobName, "ctx_switch"), a[0]+a[1])

        stats.setVar("stats-{}-{}".format(jobName, "fds"), p.num_fds())
        stats.setVar("stats-{}-{}".format(jobName, "threads"), p.num_threads())
        
        a = p.cpu_times()
        stats.setVar("stats-{}-{}".format(jobName, "cpu_times_user"), a[0])
        stats.setVar("stats-{}-{}".format(jobName, "cpu_times_system"), a[1])

        stats.setVar("stats-{}-{}".format(jobName, "cpu_cores"), len(p.cpu_affinity()))

        a = p.memory_info()
        stats.setVar("stats-{}-{}".format(jobName, "mem_rss"), a[0])
        stats.setVar("stats-{}-{}".format(jobName, "mem_vms"), a[1])
        stats.setVar("stats-{}-{}".format(jobName, "mem_shared"), a[2])
        stats.setVar("stats-{}-{}".format(jobName, "mem_text"), a[3])
        stats.setVar("stats-{}-{}".format(jobName, "mem_lib"), a[4])
        stats.setVar("stats-{}-{}".format(jobName, "mem_data"), a[5])

        stats.setVar("stats-{}-{}".format(jobName, "mem_percent"), p.memory_percent())

        stats.setVar("stats-{}-{}".format(jobName, "connections"), len(p.connections()))

        stats.setVar("stats-{}-{}".format(jobName, "open_files"), len(p.open_files()))
