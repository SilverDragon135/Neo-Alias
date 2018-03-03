# Neo Alias (NA)
Neo alias is dapp built on NEO blockchain. The purpose of NA is to make the blockchain more user friendly and simplify the application deployment and maintenance during the dapps lifetime. NA does not require off chain solution. Please check Proposal.md for more informations.

# Roadmap

0. code cleanup
    -   setup naming convetion
    -   change boolean return values to integer exit codes (+documentation)
    -   improve tests and divide them per gateway
    -   after improvement of compiler --> fix classes 
    -   document Dynamic SC calls
    -   create ABI documentation
1. voting protocol for NA and election protocol
2. staking protocol for NA
3. add other alias types

# Testing without sub-nas support

All core components if NA can be now tested trough automated testing.

The non-tested parts are DynamicAppCall and sub_nas support now. It seems like they won't be testable trough automated testing for now, at least until I find out way how automatize neo-gui from nel and find way how to grab results on the blockchain.  

# Testing with sub-nas support

Requirements:
-   neo-gui from nel or other app to invoke script, which support sub inner arrays in parameters
-   In ServiceConfiguration set support_sub_nas_call to True.

