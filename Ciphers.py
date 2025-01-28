import re
import numpy as np

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
        def make_key_matrix(key):
            key=key.upper()
            matrix=list(ord(i)-65 for i in key)
            if(len(key)==9):
                return np.array(matrix).reshape(3,3)
            elif(len(key)==4):
                return np.array(matrix).reshape(2,2)
            else:
                raise ValueError("Invalid key length. Use 4 (2x2) or 9 (3x3) characters.")


        def make_plaintext_matrix():
            self.text=self.text.upper()
            key_size=3 if len(key)==9 else 2
            while(len(self.text)%key_size!=0):
                self.text+='X'
            self.text=np.array([ord(i) - 65 for i in self.text])
            return self.text.reshape(-1,key_size)

        def mod_inverse(a):
            a%=26
            for x in range(1,26):
                if(a*x)%26==1:
                    return x
            raise ValueError("Modular inverse does not exist")

        def make_inverse(matrix):
            det = int(round(np.linalg.det(matrix)))
            det%=26
            det_inv = mod_inverse(det)
            adjugate = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix)).astype(int) % 26
            return (det_inv * adjugate) % 26

        key_matrix = make_key_matrix(key)
        plaintext_matrix = make_plaintext_matrix()

        if(encrypt):
            result=np.dot(key_matrix,plaintext_matrix.T).T%26
            result="".join(chr(val+65) for row in result for val in row)
            print(result)
        else:
            inverse_key_matrix=make_inverse(key_matrix)
            result=np.dot(inverse_key_matrix,plaintext_matrix.T).T%26
            result = "".join(chr(val+65) for row in result for val in row)
            print(result)

    def railfenceCipher(self, depth, encrypt=True):
        matrix=np.full((depth, len(self.text)),'')
        i,j=0,0
        if(encrypt):
            while(j<len(self.text)):
                while(i<depth and j<len(self.text)):
                    matrix[i,j]=self.text[j]
                    i+=1
                    j+=1

                else:
                    i-=2
                    while(i>0 and j<len(self.text)):
                        matrix[i, j] = self.text[j]
                        i-=1
                        j+=1
        else:


        result="".join(val for row in matrix for val in row).strip()
        print(result)



c=ClassicCiphers("paymore")
c.railfenceCipher(3, encrypt=True)