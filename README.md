# Neo Alias (NA)
Neo alias is dapp built on NEO blockchain. The purpose of NA is to make the blockchain more user friendly and simplify the application deployment and maintenance during the dapps lifetime. NA does not require off chain solution. Please check Proposal.md for more informations.

# Project status update
-   I´m currently busy with another project (until the end of april), after that NA is going to be fist priority.
-   I´m proud, that NA is listed in excelent project list from first NEO dev competition (https://neo.org/awards.html).
-   Sadly, NA was not successful in terms of acquiring prize (NEO and CoZ dev competition), which is crucial for NA ICO deployment on NEO blockchain. 
    1.  That means, the NA deployment will be delayed until we receive necessary funding for SC deployment.
    2.  One of reason for failing in competition was probably immaturity of NA (early stage of development, project not finished, may not be considered MVP yet).
    And because of that, I will focus in the future for improving current NA SC (voting, lowering fees - by algorithm simplification, etc.) and building infrastracture (NA server, support for NA in wallets etc.)
-   I will submit NA in next competitions too. Let's hope in better results, so the NA may come to reality :)
-   In case you want help with NA funding, please use NEO address:
    *Donations: ARSforLjf3753vR6N3c5Dx4XtMCpq53YVS*
    All funds will be used only for NA deployment. The use of funds will be fully transparent and will be announced/listed for now here and later on NA website. In case of some investors wanting to fund deployment of NA ICO smartcontract - it is possible to do it in form of presale, what means the NAT rewards for presale investors would be hardcoded in ICO SC.

# Roadmap

- Number one priority for now will be to find a way, how to automated testing dynamicappcall. 
0. code cleanup
    -   setup naming convetion
    -   change boolean return values to integer exit codes (+documentation)
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
-   In gateway/na.py set sub_nas to True. 
