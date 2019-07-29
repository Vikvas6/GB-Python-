# Task 1
str1 = 'разработка'
str2 = 'сокет'
str3 = 'декоратор'


def type_and_content(var):
    print(type(var))
    print(var)


type_and_content(str1)
type_and_content(str2)
type_and_content(str3)

str1_u = str1.encode()
str2_u = str2.encode()
str3_u = str3.encode()

type_and_content(str1_u)
type_and_content(str2_u)
type_and_content(str3_u)

# Task 2
str4_b = b'class'
str5_b = b'function'
str6_b = b'method'


def type_and_content_len(var):
    type_and_content(var)
    print(len(var))


type_and_content_len(str4_b)
type_and_content_len(str5_b)
type_and_content_len(str6_b)

# Task 3
str7_b = b'attribute'
# str8_b = b'класс' - SyntaxError: bytes can only contain ASCII literal characters.
# str9_b = b'функция' - SyntaxError: bytes can only contain ASCII literal characters.
str10_b = b'type'

# Task 4
str11 = 'разработка'
str12 = 'администрирование'
str13 = 'protocol'
str14 = 'standard'


def enc_dec(var):
    var_enc = var.encode()
    type_and_content_len(var_enc)
    var_enc_dec = var_enc.decode()
    type_and_content_len(var_enc_dec)


enc_dec(str11)
enc_dec(str12)
enc_dec(str13)
enc_dec(str14)
