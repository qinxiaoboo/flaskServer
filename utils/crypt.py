import base64

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

from flaskServer.config.config import TEXT_PASSWORD, PRIVATE_KEY_PEM


# uses https://www.pycryptodome.org version 3.9.9

def base64Encoding(input):
  dataBase64 = base64.b64encode(input)
  dataBase64P = dataBase64.decode("UTF-8")
  return dataBase64P

def base64Decoding(input):
    return base64.decodebytes(input.encode("ascii"))

def generateSalt32Byte():
  return get_random_bytes(32)
# 文本加密
def aesCbcPbkdf2EncryptToBase64(plaintext):
  passwordBytes = TEXT_PASSWORD.encode("ascii")
  salt = generateSalt32Byte()
  PBKDF2_ITERATIONS = 15000
  encryptionKey = PBKDF2(passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256)
  cipher = AES.new(encryptionKey, AES.MODE_CBC)
  ciphertext = cipher.encrypt(pad(plaintext.encode("ascii"), AES.block_size))
  ivBase64 = base64Encoding(cipher.iv)
  saltBase64 = base64Encoding(salt)
  ciphertextBase64 = base64Encoding(ciphertext)
  return saltBase64 + ":" + ivBase64 + ":" + ciphertextBase64
# 文本解密
def aesCbcPbkdf2DecryptFromBase64(ciphertextBase64):
  passwordBytes = TEXT_PASSWORD.encode("ascii")
  data = ciphertextBase64.split(":")
  salt = base64Decoding(data[0])
  iv = base64Decoding(data[1])
  ciphertext = base64Decoding(data[2])
  PBKDF2_ITERATIONS = 15000
  decryptionKey = PBKDF2(passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256)
  cipher = AES.new(decryptionKey, AES.MODE_CBC, iv)
  decryptedtext = unpad(cipher.decrypt(ciphertext), AES.block_size)
  decryptedtextP = decryptedtext.decode("UTF-8")
  return decryptedtextP


from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# 生成私钥
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 导出私钥
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# 导出公钥
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# print(public_pem)
# print(private_pem)


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# 加载私钥
def load_private_key(pem_data):
    return serialization.load_pem_private_key(
        pem_data,
        password=None,
    )
# 解密 Base64 编码的数据, 非对称解密
def decrypt_data(encrypted_base64):

    private_key = load_private_key(PRIVATE_KEY_PEM.encode('utf-8'))

    # 解码 Base64
    encrypted_data = base64.b64decode(encrypted_base64)

    # 解密数据
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data.decode('utf-8')
# print(aesCbcPbkdf2EncryptToBase64("123qweasd"))
# if __name__ == '__main__':
#
#     print("SO AES CBC 256 encryption with PBKDF2 key derivation")
#
#     plaintext = "The quick brown fox jumps over the lazy dog"
#     print("plaintext: " + plaintext)
#     password = "qinxiaobo"
#
#     print("\n* * * Encryption * * *")
#     ciphertextBase64 = aesCbcPbkdf2EncryptToBase64(plaintext)
#     print("ciphertext: " + ciphertextBase64)
#     print("output is (Base64) salt : (Base64) iv : (Base64) ciphertext")
#
#     print("\n* * * Decryption * * *")
#     ciphertextDecryptionBase64 = ciphertextBase64
#
#     print("ciphertext (Base64): " + ciphertextDecryptionBase64)
#     print("input is (Base64) salt : (Base64) iv : (Base64) ciphertext")
#     decryptedtext = aesCbcPbkdf2DecryptFromBase64(ciphertextBase64)
#     print("plaintext:  " + decryptedtext)