#NIST192p, NIST224p, NIST256p, NIST384p, NIST521p

from ecdsa import NIST256p, SigningKey

sk = SigningKey.generate(curve=NIST256p)
vk = sk.get_verifying_key()
open("NIST256p/private.pem","wb").write(sk.to_pem())
open("NIST256p/public.pem","wb").write(vk.to_pem())

