import re

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


    def playfairCipher(self, key, encrypt=True):
        def make_matrix(key):
            key = key.upper().replace("J", "I")
            matrix = "".join(dict.fromkeys(key + "ABCDEFGHIKLMNOPQRSTUVWXYZ"))
            return list(matrix[i:i + 5] for i in range(0, 25, 5))

        def create_groups():
            self.text = re.sub(r'[^A-Z]', '', self.text.upper().replace("J", "I"))
            grouped_text = ""
            i = 0
            while i < len(self.text):
                a = self.text[i]
                b = self.text[i + 1] if i + 1 < len(self.text) else 'X'
                if a == b:
                    grouped_text += a + 'X'
                    i += 1
                else:
                    grouped_text += a + b
                    i += 2
            if len(grouped_text) % 2 != 0:
                grouped_text += "X"
            return grouped_text

        def find_pos(matrix, val):
            for i in range(5):
                for j in range(5):
                    if(matrix[i][j]==val):
                        return i,j
            return None

        matrix = make_matrix(key)
        self.text=create_groups()
        result=""
        shift=1 if encrypt else -1
        for i in range(0, len(self.text), 2):
            a, b=self.text[i], self.text[i+1]
            r1, c1 = find_pos(matrix, a)
            r2, c2 = find_pos(matrix, b)
            if(r1==r2):
                result+= matrix[r1][(c1+shift)%5] + matrix[r2][(c2+shift)%5]
            elif(c1==c2):
                result+= matrix[(r1+shift)%5][c1] + matrix[(r2+shift)%5][c2]
            else:
                result+=matrix[r1][c2] + matrix[r2][c1]
        print(result)

    def hillCipher(self, key, encrypt=True):
        return 0

c=ClassicCiphers("HELLO")
c.playfairCipher("MONARCHY")