solaredge2graphite
==================

Small Python script to retrieve inverter readings for a SolarEdge
PV array from the SolarEdge monitoring portal and send them to a Graphite
metrics storage server.


Usage
-----

You will need an API key and your site ID from the SolarEdge monitoring
portal (under Admin -> Settings; if this is not available, contact your
installer).

Supply your Graphite host, the desired prefix, your API key and site ID as
arguments or edit the script and set them as defaults.

Run the script every 15 minutes as a scheduled task. (Don't run it more
frequently than that, as the SolarEdge monitoring portal only updates at
that interval.)

As PV arrays don't tend to generate much energy at night, the `--null`
option skips retrieving the current readings and simply sends zero or
'unknown' values to Graphite, avoiding unnecessary API calls. This is
to avoid hitting the API call limit under heavy usage but will probably
not be required for most users.

To test retrieval of current readings without updating Graphite, use the
`--debug` option. In normal use, the script does not produce any output
unless an error occurs.


Limitations
-----------

The script only retrieves the current power and lifetime energy outputs.
It does not handle stored energy systems such as batteries, for which
there are a number of other API calls that could be used.


Dependencies
------------

Use PIP to install the following Python libraries from PYPI:

 * solaredge
 * graphyte

solaredge2graphite needs Python 3.2+, only because the solaredge API
library requires it.


Author
------

Ade Rixon, http://www.big-bubbles.org.uk/
