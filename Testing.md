# Testing snippets

!!! All snippets are moved to automated testing in tests\tests_to_run.py !!!

Hint: These snippets were used to no sub_nas testing, for sub_nas testing change False value to True, since you will need DynamicAppCall

load_run ..\NA\NASC.avm test 0710 05 True False na_offer_sell ["asdhasdy",1000,2]
-   places sell offer with price 1000 of assets (for now it would be gas, later NAC)

load_run ..\NA\NASC.avm test 0710 05 True False na_cancel_sale_offer ["asdhasdy",2]
-   closes sell offer


