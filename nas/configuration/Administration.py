from nas.common.Account import Account


class AdminConfiguration():
    """
    :Holds information about admins:
    \nroot_admin - highest admin, predefined
    \nroot_admin rights:
    \n - core_NASC => can init and participate in admin election
    \n - NASC => can only init NASC
    """
    root_admin = b'x\xc50\xe2V\xef\x8c\xd6\x0b\xf4+\x0f\xb9\x02\xe8\x9eFQ\xc7\xb7'

def init_test_funds():
    adminConfiguration = AdminConfiguration()
    admin_account = Account()
    admin_account.address = adminConfiguration.root_admin
    admin_account.add_available_assets(10000)