# Special variables:
#   input  = reference to input workspace
#   output = name of the processed output workspace
# Temporary workspaces should be deleted

# Where should these come from?
rebin_params = '0,10000,100000'

# Comment in Mantid log
print 'Processing events into histogram'

# Just rebinning for now, but could do more
mtd[output] = Rebin(input, Params=rebin_params, PreserveEvents=False)
