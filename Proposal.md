# Proposal v0.1
This readme describes our vision. Most of it may change based on community decisions and requirements. Only fixed idea in this document is "NA SC has to be open source, community controlled and developed". 

There are two scenarios, what will be with NA in future
-   I will to create NAA (Neo alias authority). It is already created on github.
-   The CoZ will be interested acting as NAA. I would like to start discussion about this soon.

# Neo Alias Smart Contract (NA SC)

Neo alias is on chain dapp build on NEO blockchain. The purpose of NA is to make the blockchain more user friendly and simplify the application deployment and maintenance during the dapps lifetime. 

We believe, that service like this should belong to community and not company. In final stage of development will be NA:
- open source
- fully controlled a configured by community - fees, registration durations, trading commission
- independent - NA will work on chain, no further off chain solutions needed 

In the core is the functionality similar to domain name system. NA instead of resolving domains(should be implemented later) resolves:
-	SC aliases
-	NEO Account aliases
-	Asset alias

Other planned aliases:
- domains
- contacts [ name, phone, email , adress ]
- custom address aliases (should not be free, but the community decides)

# Neo Alias sub-services
In current early stage of development Neo alias supports direct calls to NA sub-services. That means that individuals can create own NA, which can be called directly trough root NA. The root NA should stay community controlled.

# Core Neo Alias
Core NA is NA in its simplest form and its only purpose is to provide way to resolve "root_NA". We need core NA to allow updates of root NA without need of updating applications, by simply redirecting "root_NA" to updated version. 

Core Neo Alias should be controlled by neo dev community, if they show interest.

The control over Core NA will be provided only to elected administrators. These administrators can create election of root_NA in case of update and redirect Core NA to point to updated version.

# Neo Alias Economy - NAC (Neo Alias Coin)

Neo Alias Economy is built around 2 fees:
- trading fee - commission (hard coded max 50%)
- holding fee - fee for owning alias for specified time (NEO Accounts should not be included)

All the collected fees will be distributed to NAC holders. The details about rewards will be published with implementation of staking protocol. All non distributed fees will be distributed on protocol launch to all holder proportionately.

Neo Alias (except Neo Accounts) are registered for maximum duration defined by community. If you want register alias, you have to pay fee (community defined per community defined period) for defined duration (up to maximum). The payment is non refundable. 

Example of fee calculation:

Community defined configuration:
- fee period - timestamp - defined per alias type
- fee - BigInteger - defined per alias type
- maximum duration - timestamp 

Calculation: to pay = (duration / fee period) * fee

NAC will be used to pay and trading with aliases. Expected total supply is 100 000 000 or 1 000 000 000 with 8 decimals. (The community decide) 

Expected NAC distribution:
- 1% founder
- 15% dev and marketing fund 
- 5% Neo.org
- 0-5% CoZ
- 50% ICO
- 24-29% staking rewards - in first five years automatically added to fee pool and redistributed to NAC holders .

In case CoZ will be interested in becoming NAA, the 5% reserved to CoZ will be merged with staking rewards and CoZ would control dev fund.

# Neo Account
Neo account was inspired by PASC. It targets to simplify standard adress operations. Supports all NEP5 methods. Neo accounts will be tradable, non-expirable and free of charge. 

It is assitiation between address and account alias in form of string starting with NEO and followed by numbers.
Examples:
- NEO0
- NEO240000000015547754
- NEO266887488999977453

# Neo Account ICO Reservation
- NEO9 reserved for founder(me :)
- NEO0-8 and NEO10-99 reserved for COZ and NEO.org and their developers (to simplify funding)
- NEO100 reserved for NA dev fund
- NEO101 - NEOXXXXX - All investors participating in ICO will get NEO account automatically (Just I need to figure out, how to dump SC storage :)) based on amount invested.
That means the highest invested amount will be NEO101, next 102, next 103 etc.

All reserved account will be automatically registered to participating addresses and can be traded. Reservation in this context means, that if you do not want to sell your account
you cannot lose it (may be limited, if community votes for expirable accounts, but it is not expected)

# Asset Alias
In form of symbol (up to four characters). Pointing to SC of deployed asset. Simplifying wallets development. New assets can be added by adding only the asset symbol.

# Smart Contract Alias
In form of string pointing to Smart Contract. Improving off-chain application development. No more updates required in case of SC change. 

# ICO
Expected ICO date - May/June

Since we have already working MVP. We can expect nearly fully or fully functional NA on ICO launch.

Donations: ARSforLjf3753vR6N3c5Dx4XtMCpq53YVS