# Neo Alias (NA)
Neo alias is dapp built on NEO blockchain. The purpose of NA is to make the blockchain more user friendly and simplify the application deployment and maintenance during the dapps lifetime. NA does not require off chain solution. Please check Proposal.md for more informations.

# Roadmap

0. code cleanup
    -   setup naming convetion
    -   change boolean return values to integer exit codes (+documentation)
    -   add units test where possible
    -   after improvement of compiler --> fix classes 
    -   document Dynamic SC calls
    -   create ABI documentation
    -   lower tx costs caused by poor OOP
1. voting protocol for NA and election protocol
2. staking protocol for NA
3. add other alias types

# Testing without sub-nas support

na.py - fully tested
-   na_register, na_renew, na_update_target,na_transfer, na_delete, na_query, na_alias_data

na_trady.py 
-   na_offer_sell, na_cancel_sale_offer - tested
-   buy_offer was not yet tested, but should work

NEP5.py
-   tested all API for coin info
-   transfers and approvals conform to NEP5 template - therfore should work properly

SmartNEP5.py
-   Even if biggest selling point of this dapp, wasnt tested yet.
    Reason: we had problems with compiler and didn't have time for proper assets management testing. Neverthless the main funtionality is implemented and tested. The SmartNEP5 is just a gateway/showcase how to use core service and may be implemented as separate smart contract.

# Testing with sub-nas support

Requirements:
-   neo-gui from nel or other app to invoke script, which support sub inner arrays in parameters
-   uncomment section in NAS\gateway\NeoAliasService.py and NASC.py