# Special variables:
#   input  = reference to input workspace
#   output = name of the processed output workspace
# Temporary workspaces should be deleted

from mantid.simpleapi import Rebin, mtd
from config import rebin_params


# Comment in Mantid log
print 'Processing events into histogram'

# Just rebinning for now, but could do more
mtd[output] = Rebin(input, Params=rebin_params, PreserveEvents=False)
