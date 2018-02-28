# Testing snippets

!!! All snippets are moved to automated testing in tests\tests_to_run.py !!!

Hint: These snippets were used to no sub_nas testing, for sub_nas testing change False value to True, since you will need DynamicAppCall

load_run ..\NA\NASC.avm test 0710 05 True False na_alias_data ["asdhasdy",2]
-  returns all informations stored about alias, if does not exist, returns False

load_run ..\NA\NASC.avm test 0710 05 True False na_update_target ["asdhasdy","ARSforLjf3753vR6N3c5Dx4XtMCpq53YVS",2]
-   first calls transfers alias to another owner, result True

load_run ..\NA\NASC.avm test 0710 05 True False na_update_target ["asdhasdy","ARSforLjf3753vR6N3c5Dx4XtMCpq53YVS",2]
-   second call fails with result False, because we are no longer owner of alias

load_run ..\NA\NASC.avm test 0710 02 True False na_renew ["asdhasdy","1519952704",2]
-   renew alias expiration to selected timestamp

load_run ..\NA\NASC.avm test 0710 05 True False na_delete ["asdhasdy",2]
-   retuns 1 --> deletes alias

load_run ..\NA\NASC.avm test 0710 05 True False na_offer_sell ["asdhasdy",1000,2]
-   places sell offer with price 1000 of assets (for now it would be gas, later NAC)

load_run ..\NA\NASC.avm test 0710 05 True False na_cancel_sale_offer ["asdhasdy",2]
-   closes sell offer


