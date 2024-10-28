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



async def main(account):
    async with Email.from_account(account) as email_client:
        await email_client.login()
        text = await email_client.wait_for_email(lambda s: 'Your Galxe Verification' in s)
        print(text)
        code = text[text.find('<h1>') + 4:text.find('</h1>')]
        print(code)
        print("登录成功")

if __name__ == '__main__':
    # asyncio.run(getCode())
    account = AccountInfo()
    account.idx = "Q-0"
    account.email_username = "1337556808@qq.com"
    account.email_password = "xixutkibzvzjifcg"
    asyncio.run(main(account))
