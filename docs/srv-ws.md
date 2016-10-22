# Webservices on the server side

## pushAction

* method : POST
* params
  * uid: uid (int) of the probe to push the action to
  * action: ["restart"]

* restart action
  * module: ["all", "job"]
  * if module is job
    * job: name of the job to be restarted

the action is added to the host action list, action will be added to
the next ping request from the probe

## ping

* method: POST
* params:
  * uid: uid of the probe

probe calls ping webservice on regular basis in order to inform server
it is still active, on return, if an action is present in the DB, it
will be send back to the probe for execution


## discover

used by the probe to inform server it is online. probe should be
defined in the configuration to be accepted and inserted in the live
DB
* method: POST
* params
  * hostId: uid will be calculated from this unique key
  * ipv4
  * ipv6
* returns:
  * answer: OK
  * uid

## admin/reload

* method: POST

reload the configuration file

## version

returns the version information of the server

* method: GET

## admin/getProbes

returns the list of the registered probes in the live database (not configuration)

* method: GET