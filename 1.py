import pikepdf #是用来读取pdf文件
from PyPDF2 import PdfReader, PdfWriter  # python2用PdfFileReader, PdfFileWriter
from tqdm import tqdm # 用来读取进度条

def userCrak(filePathName, wordPathList):
    filename = filePathName  # pdf文件路径
    wordlist = wordPathList  # 密码字典路径
    n_words = len(list(open(wordlist, 'rb')))
    fp = open(filename, "rb+")
    pdfFile = PdfReader(fp)  # python2用PdfFileReader
    with open(wordlist, "rb") as wordlist:
        if pdfFile.is_encrypted: # python2为getIsEncrypted
            for word in tqdm(wordlist, total=n_words, unit="word"): # 显示进度条
                try:
                    pikepdf.open(filename, password=word.strip()) #打开文件查看是否能打开
                except:
                    continue
                else:
                    passwords = word.decode().strip() # 得到的密码
                    print(f"已经查找到密码为:{passwords}")
                    return passwords
            return print("!密码没有找到, 请尝试使用其他的密码词典!")

def fileSavePath(filePathName, userPasswordName):
    """如果是Python2用PdfFileReader"""
    pdf_reader = PdfReader(fr'{filePathName}')  # 输入你想要操作的pdf加密的文档的位置/名称
    pdf_reader.decrypt(f'{userPasswordName}') # 加入解密的密码
    """如果是Python2用PdfFileWriter"""
    pdf_writer = PdfWriter()
    """如果是python2将append_pages_from_reader改为appendPagesFromReader"""
    pdf_writer.append_pages_from_reader(pdf_reader)

    pdf_writer.write(open(filePathName, 'wb')) # 写文件
    print("！！！原PDF文件打开密码已去除！！！")


if __name__ == '__main__':
    filenamePath = r"C:\Users\Lenovo\Desktop\破解pdf\1.pdf"  # pdf文件路径
    wordlistPath = r"C:\Users\Lenovo\Desktop\破解pdf\rockyou_6digits.txt"  # 密码字典路径
    userPassword = userCrak(filenamePath, wordlistPath) # 得到解密的密码
    fileSavePath(filenamePath, userPassword) # 将解密的密码和文件路径填入

