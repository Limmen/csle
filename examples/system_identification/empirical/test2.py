from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.management.management_user import ManagementUser
import bcrypt

if __name__ == '__main__':
    # username = "admin"
    # password = "admin"
    # admin = True
    # byte_pwd = password.encode('utf-8')
    # # Generate salt
    # salt = bcrypt.gensalt()
    # # Hash password
    # pw_hash = bcrypt.hashpw(byte_pwd, salt)
    # user = ManagementUser(username=username, password=pw_hash.decode("utf-8"), admin=admin, salt=salt.decode("utf-8"))
    # MetastoreFacade.save_management_user(management_user=user)

    username = "guest"
    password = "guest"
    admin = False
    byte_pwd = password.encode('utf-8')
    # Generate salt
    salt = bcrypt.gensalt()
    # Hash password
    pw_hash = bcrypt.hashpw(byte_pwd, salt)
    user = ManagementUser(username=username, password=pw_hash.decode("utf-8"), admin=admin, salt=salt.decode("utf-8"))
    MetastoreFacade.save_management_user(management_user=user)
