#编程实现字符串的转换:将"adsdsfdndsdsdfsfdsdASDSDEDSFE"字符串大写变小写，
# 小写变大写,并且将字符串变为镜像 字符串,例如: 'A'变为Z', 'b'变为'y'
s = 'adsdsfdndsdsdfsfdsdASDSDEDSFE'
intab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
outtab ="ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba"
trantab = str.maketrans(intab, outtab)
s=s.swapcase()#转换大小写
print(s)
new_s=s.translate(trantab)
print("最终得到的镜像字符串为：{0}".format(new_s))