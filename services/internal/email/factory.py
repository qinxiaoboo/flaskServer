import asyncio

from flaskServer.entity.galxeAccount import AccountInfo
from flaskServer.services.internal.email.base import BaseClient

from flaskServer.services.internal.email.imap import IMAPClient
from flaskServer.services.internal.email.mail3 import Mail3Client


class Email:

    @classmethod
    def from_account(cls, account: AccountInfo) -> BaseClient:
        if 'mail3.me' in account.email_username:
            return Mail3Client(account)
        return IMAPClient(account)


def _extract_code_from_email(text):
    return text[text.find('<h1>') + 4:text.find('</h1>')]


async def getCode():
    account = AccountInfo()
    account.email_username = "yun16603860403@outlook.com"
    account.email_password = "5201314xiao"
    account.idx = 1
    try:
        async with Email.from_account(account) as email_client:
            await email_client.login()
            email_text = await email_client.wait_for_email(lambda s: s == 'Please confirm your email on Galxe')
            code = _extract_code_from_email(email_text)
            print(code)
    except Exception as e:
        raise Exception(f'Failed to link email: {str(e)}')


if __name__ == '__main__':
    # asyncio.run(getCode())
    import imaplib
    import email
    conn = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    conn.login("yun16603860403@outlook.com", "5201314xiao")
    print("登录成功")