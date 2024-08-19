from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

# Gera um par de chaves RSA e as converte para Base64
def generate_key_pair_base64():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    private_key_base64 = base64.b64encode(private_key).decode('utf-8')
    public_key_base64 = base64.b64encode(public_key).decode('utf-8')
    
    return private_key_base64, public_key_base64

# Assina uma mensagem usando a chave privada em Base64
def sign_message_base64(private_key_base64, message):
    private_key = RSA.import_key(base64.b64decode(private_key_base64))
    h = SHA256.new(message.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(h)
    return base64.b64encode(signature).decode('utf-8')

def load_public_key_base64(public_key_base64):
    return RSA.import_key(base64.b64decode(public_key_base64))

# Verifica a assinatura usando chaves e assinatura em Base64
def verify_signature(message, signature_base64, public_key_base64):
    public_key = load_public_key_base64(public_key_base64)
    h = SHA256.new(message.encode('utf-8'))
    try:
        pkcs1_15.new(public_key).verify(h, base64.b64decode(signature_base64))
        return True
    except (ValueError, TypeError):
        return False
    
# Função principal
def main():
    # Gera o par de chaves em Base64
    private_key_base64, public_key_base64 = generate_key_pair_base64()

    # Mensagem a ser assinada
    message = "Esta é uma mensagem secreta."

    # Assina a mensagem
    signature_base64 = sign_message_base64(private_key_base64, message)

    # Exibe as chaves e a assinatura em Base64
    print("Chave Privada (Base64):")
    print(private_key_base64)
    print("\nChave Pública (Base64):")
    print(public_key_base64)
    print("\nMensagem:")
    print(message)
    print("\nAssinatura (Base64):")
    print(signature_base64)
    
    print({"action": "register", "key": public_key_base64, "message": message, "signature": signature_base64})
    
    print(verify_signature(message, signature_base64, public_key_base64))

if __name__ == "__main__":
    main()
