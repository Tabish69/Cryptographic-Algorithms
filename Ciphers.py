import re
import numpy as np
import math

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
        dir_down=False
        row,col=0,0
        for i in range(len(self.text)):
            if(row==0) or (row==depth-1):
                dir_down=not dir_down
            matrix[row,col]=self.text[i] if(encrypt) else '*'
            col+=1
            if(dir_down):
                row+=1
            else:
                row-=1

        if(encrypt):
            result="".join(val for row in matrix for val in row).strip()
            print(matrix)
            print(result)

        else:
            k=0
            for i in range(depth):
                for j in range(len(self.text)):
                    if(matrix[i,j]=='*') and k<len(self.text):
                        matrix[i,j]=self.text[k]
                        k+=1
            print(matrix)
            dir_down = False
            row, col = 0, 0
            for i in range(len(self.text)):
                if (row == 0) or (row == depth - 1):
                    dir_down = not dir_down
                print(matrix[row,col], end='')
                col += 1
                if (dir_down):
                    row += 1
                else:
                    row -= 1


    def columnarTransposition(self,keyword,encrypt=True):

        if(encrypt):
            self.text=list(self.text)
            row=math.ceil(len(self.text)/len(keyword))
            col=len(keyword)
            key=sorted(list(keyword))
            result=""
            self.text.extend('_'*int((row*col)-len(self.text)))
            matrix=[self.text[i:i+col] for i in range(0,len(self.text),col)]
            for i in range(col):
                curr_index=keyword.index(key[i])
                result+= "".join([row[curr_index] for row in matrix])
            print(result)

        else:
            self.text = list(self.text)
            row = math.ceil(len(self.text) / len(keyword))
            col = len(keyword)
            key =sorted(list(keyword))
            k=0
            m=0
            result = ""
            matrix=[]
            for _ in range(row):
                matrix += [[None]*col]

            for _ in range(col):
                curr_index=keyword.index(key[k])
                for j in range(row):
                    matrix[j][curr_index]=self.text[m]
                    m+=1
                k+=1
            try:
                result="".join(sum(matrix,[]))
            except TypeError:
                raise TypeError("Do not have same letters in key")

            result=result.strip('_')
            print(result)





c=ClassicCiphers("aoann eti_pm eoyrtt_")
c.columnarTransposition("CADB",encrypt=False)
