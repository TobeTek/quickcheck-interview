from typing import Any
import string

class VignetteCipher:
    @staticmethod
    def create_key(keyword, keyletter: str ="a") -> str:
        keyword = [i for i in keyword.upper() if str.isalnum(i)]
        unique_keyletters = []
        for i in keyword:
            if i not in unique_keyletters:
                unique_keyletters.append(i)
        keyword = unique_keyletters
        others = [i for i in string.ascii_uppercase if i not in keyword]
        key_indx = string.ascii_uppercase.index(keyletter.upper())
        print(keyword)
        key = others[:key_indx] + keyword + others[key_indx:]
        return "".join(key)

    @staticmethod
    def encrypt(plain_text, key):
        plain_text = [i for i in plain_text.upper() if str.isalnum(i)]
        result = []
        for elem in plain_text:
            indx = string.ascii_uppercase.index(elem)
            r = key[indx]
            result.append(r)
        
        return "".join(result)

    @staticmethod
    def decrypt(cipher_text, key):
        cipher_text = [i for i in cipher_text.upper() if str.isalnum(i)]
        result = []
        for elem in cipher_text:
            indx = key.index(elem)
            r = string.ascii_uppercase[indx]
            result.append(r)
        
        return "".join(result)


    def __call__(self, *args: Any, **kwds: Any) -> Any:    
        encrypted = "VIAGUIGTLBILOCSDQN"
        keywords = ["SHOPIFY COMMERCE", "TOBI LUTKE"]
        for keyword in keywords:
            for i, letter in enumerate(string.ascii_uppercase):
            
            # plain_text = "Welcome all children to the lighthouse"

                key = self.create_key(keyword=keyword, keyletter=letter)
                # cipher_text = encrypt(plain_text, key=key)
                plain = self.decrypt(cipher_text=encrypted, key=key)
                print(f"{i}#: {letter=}, {key=}, {encrypted=}, {plain=}")
            

class PlayfairCipher:
    @staticmethod
    def create_key(keyword):
        ...
    
    @staticmethod
    def encrypt(plain_text, key):
        ...
        
    @staticmethod
    def decrypt(cipher_text, key):
        ...
    