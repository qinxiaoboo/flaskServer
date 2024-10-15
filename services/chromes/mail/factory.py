from flaskServer.services.chromes.mail.outlook import Outlook


class Email:

    @classmethod
    def from_account(cls, idx, chrome, envName, username, password):
        if "outlook.com" in username or "hotmail.com" in username:
            return Outlook(idx, chrome, envName, username, password)

