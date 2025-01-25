class ClassicCiphers:
    def __init__(self, text):
        self.text=text

    def caesarCipher(self, shift, encrypt=True):
        result=""
        shiftamt=shift if encrypt else -shift
        for char in self.text:
            if char.isalpha():
                result+=chr((ord(char)-65+shiftamt)%26+65) if char.isupper() else chr((ord(char)-97+shiftamt)%26+97)
            else:
                result+=char
        print(result)

    def vigenereCipher(self, key, encrypt=True):
        key=key.strip()
        keyval=""
        result=""
        keylen=len(key)
        k=0
        for i in range(0, len(self.text)):
            if(self.text[i].isalpha()):
                keyval += key[k % keylen]
                k += 1
            else:
                keyval+=" "

        for i in range(0, len(self.text)):
            if(self.text[i].isalpha()):
                shift = ((ord(keyval[i]) - 65) if encrypt else -(ord(keyval[i]) - 65)) if keyval[i].isupper() else ((ord(keyval[i]) - 97) if encrypt else -(ord(keyval[i]) - 97))
                result += chr((ord(self.text[i]) - 65 + shift) % 26 + 65) if self.text[i].isupper() else chr((ord(self.text[i]) - 97 + shift) % 26 + 97)
            else:
                result+=self.text[i]
        print(result)

    def playfairCipher(self):
        return 0


