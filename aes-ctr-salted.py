from Crypto.Cipher import AES
import pyscrypt

password = b"HelloWorld"
salt = b"SeaSalt"

N = 1024
r = 1
p = 1

key16 = pyscrypt.hash(password,salt, N,r,p, 16)


m = "sssosisdiusdhudshudshusuhdshudsd"
secret = b's\xa4\xc9\xc6\xa1\x0f\x93\xc05\x0b?\x81\x0e\xe2\x0e '
crypto1 = AES.new(key16, AES.MODE_CTR, counter=lambda: secret)
crypto2 = AES.new(key16, AES.MODE_CTR, counter=lambda: secret)

encrypt = crypto1.encrypt(plaintext=m)
decrypt = crypto2.decrypt(encrypt)
print(decrypt)

