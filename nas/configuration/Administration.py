from nas.common.Account import Account


class AdminConfiguration():
    """
    :Holds information about admins:
    \nroot_admin - highest admin, predefined
    \nroot_admin rights:
    \n - core_NASC => can init and participate in admin election
    \n - NASC => can only init NASC
    """
    #root_admin = b'\x02[|\xf4\xf8\x1f\x1b\x84\xb9M\xca!?\xb3\xecr\xb9\xea,c\x9c\x9a\x05G;\x83\xfa\xe1ek\xad\xb9/'
    root_admin = b'\x02\xa7\xbcU\xfe\x86\x84\xe0\x11\x97h\xd1\x04\xba0y[\xdc\xc8f\x19\xe8d\xad\xd2aVr>\xd1\x85\xcdb'

def init_test_funds():
    adminConfiguration = AdminConfiguration()
    admin_account = Account()
    admin_account.address = adminConfiguration.root_admin
    admin_account.add_available_assets(10000)