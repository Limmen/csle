from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.management.management_user import ManagementUser
import bcrypt

if __name__ == '__main__':
    pwd = "ogb5o)wbdZkWwg*x0l^Y"
    byte_pwd = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(byte_pwd, salt)
    user = ManagementUser(
        username="test",
        password=pw_hash.decode("utf-8"),
        email="test@csle.com",
        first_name="test",
        last_name="test",
        organization="test",
        admin=False,
        salt=salt.decode("utf-8")
    )
    MetastoreFacade.save_management_user(management_user=user)
