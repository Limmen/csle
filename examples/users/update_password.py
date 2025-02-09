from csle_common.metastore.metastore_facade import MetastoreFacade
import bcrypt

if __name__ == '__main__':
    admin_user = MetastoreFacade.get_management_user_config(id=1)
    new_pwd = "<PASSWORD>"
    byte_pwd = new_pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(byte_pwd, salt)
    admin_user.password = pw_hash.decode("utf-8")
    admin_user.salt = salt.decode("utf-8")
    MetastoreFacade.update_management_user(management_user=admin_user, id=1)
