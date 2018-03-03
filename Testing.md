# Testing snippets

!!! All snippets are moved to automated testing in tests\tests_to_run.py and tests\test_to_run_smart_NEP5.py !!!
*In automated testing you can find all these snippets and more. I left this snippets here in case you want to see how to call test NA manually.*


Hint: These snippets were used for testing without sub_nas support, for sub_nas testing change False value to True, since you will need DynamicAppCall. In ServiceConfiguration set support_sub_nas_call to True.

build ..\NA\NASC.py test 0710 05 True False na_register ["aaaa","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",2,"target",1519912704]
-   should fail - invalid target

load_run ..\NA\NASC.avm test 0710 05 True False na_register ["aaab","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",2,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]
-   first time should success and returns alias_data as array
-   seconds time should fail because already registered

load_run ..\NA\NASC.avm test 0710 05 True False na_register ["asdhasdy","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",0,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1519912704]
-   returns True - registers general alias

load_run ..\NA\NASC.avm test 0710 05 True False na_register ["aaac","ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",2,"ASnSxavKzDvwXh3ZLxBWhqMbbntwn2TJBM",1509912704]
-   should fail already expired

load_run ..\NA\NASC.avm test 0710 05 True False na_alias_data ["asdhasdy",2]
-  returns all informations stored about alias, if does not exist, returns False

load_run ..\NA\NASC.avm test 0710 05 True False na_query ["asdhasdy",2]
-  returns target of selected alais or None if not exist

load_run ..\NA\NASC.avm test 0710 05 True False na_query ["asdhasdy"]
-  retuns empty bytearray, bacuase alias is not found --> falls back to general alias type, because type was not defined and alias of this kind was not yet created

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