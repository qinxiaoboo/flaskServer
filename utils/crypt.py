from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from flaskServer.config.config import TEXT_PASSWORD
import base64

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
if __name__ == '__main__':

    print("SO AES CBC 256 encryption with PBKDF2 key derivation")

    plaintext = "The quick brown fox jumps over the lazy dog"
    print("plaintext: " + plaintext)
    password = "qinxiaobo"

    print("\n* * * Encryption * * *")
    ciphertextBase64 = aesCbcPbkdf2EncryptToBase64(plaintext)
    print("ciphertext: " + ciphertextBase64)
    print("output is (Base64) salt : (Base64) iv : (Base64) ciphertext")

    print("\n* * * Decryption * * *")
    ciphertextDecryptionBase64 = ciphertextBase64

    print("ciphertext (Base64): " + ciphertextDecryptionBase64)
    print("input is (Base64) salt : (Base64) iv : (Base64) ciphertext")
    decryptedtext = aesCbcPbkdf2DecryptFromBase64(ciphertextBase64)
    print("plaintext:  " + decryptedtext)