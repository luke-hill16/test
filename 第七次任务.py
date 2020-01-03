#!python3
#-*-encoding=utf-8 -*-



import re,os,random,math

os.chdir(r'C:\Users\Administrator\Desktop\第五次任务\分词结果')
filelist=r'C:\Users\Administrator\Desktop\第五次任务\分词结果'
files=os.listdir(filelist)

content=''
for eachfile in files:
    with open(eachfile,'r',encoding='utf-8',errors='ignore')as f_obj:
        content_obj1=f_obj.read()
        content=content+content_obj1
sp=r'([。？！……]/?…?/?”?/?)'  
content1=re.split(sp,content)      #利用正则表达式把 /！/”   /……/”   /…/…   /？/”  /。/”等组合符号的内容进行split切分。
content2=[''.join(i).strip() for i in zip(content1[0::2],content1[1::2])]  #利用zip函数把字和标点组合在一起
random.shuffle(content2)                    #打乱句序       #得到一个随机句子的列表

#todo:按照9:1的比例分为训练语料与测试语料，分别储存为train.txt和test.txt两个文本文档
#一共8293句。
testnum=math.ceil(len(content2)/10) #830
trainnum=len(content2)-testnum  #7463


#新建txt文件，按比例写入得到的句子
os.chdir(r'C:\Users\Administrator\Desktop\卢雪晖 任务5-8\第七次任务')
with open('train1.txt','w',encoding='utf-8',errors='ignore') as f1: 
    for i in content2[0:trainnum]:
        f1.write(i+'\n')
        #f1.write('\n'.join(i))#这样的话，train和test都是一个字一行
with open('test1.txt','w',encoding='utf-8',errors='ignore') as f2:
    for i in content2[trainnum:testnum+trainnum]:
        f2.write(i+'\n')
        #f2.write('\n'.join(i))
#得到训练语料与测试语料

#todo:
#将每句话按照每个字占一行进行标注，并且每一行格式为“单字+\t+标注”
#下一步：我们使用Python对其以词为单位进行标注，规则为：
#对于两字词，第一个字标B（begin），第二个字标E（end）
#对于三字或多字词，第一个字标B（begin），最后一个字标E（end），中间字全标M（middle）
#对于单字或者标点符号标BE
#同时，句子与句子之间加上一个空格作为分隔
def middle(word):  #定义一个中间项的函数。
    wordlist1=''
    for i in word[1:-1]:
        wordlist2=i+'\t'+'M'+'\n'
        wordlist1=wordlist1+wordlist2
    return wordlist1
with open('train1.txt','r',encoding='utf-8',errors='ignore') as f1: 
    sentence=f1.read()
    sentence=sentence.replace('\n',' /')#句子与句子之间加上一个空格作为分隔，将转行符替换为一个空格加一个斜杠。
    word=re.findall('(.*?)/',sentence)
    words=''
    for eachword in word[::]:  #下面进行分类讨论
        if len(eachword)>2: #情况一：词长大于2，头尾标B/E,中间标M
            wordlist=eachword[0]+'\t'+'B'+'\n'+middle(eachword)+eachword[-1]+'\t'+'E'+'\n'
            words=words+wordlist
        elif len(eachword)>1:#情况二：词长为2，头尾标B/E
            wordlist=eachword[0]+'\t'+'B'+'\n'+eachword[-1]+'\t'+'E'+'\n'
            words=words+wordlist
        elif len(eachword)==1:#情况二：词长为1，标BE，空格略过不标
            if eachword==' ':
                wordlist=eachword[0]+'\t'+'\n'
                words=words+wordlist
            else:
                wordlist=eachword[0]+'\t'+'BE'+'\n'
                words=words+wordlist
        else:
            pass
with open('train.txt','w',encoding='utf-8',errors='ignore') as f2:
    f2.write(words)   #得到使用Python对其以词为单位进行标注的最终train文件

with open('test1.txt','r',encoding='utf-8',errors='ignore') as f3:   #方法同写入train文件一样。
    sentence=f3.read()
    sentence=sentence.replace('\n',' /')
    word=re.findall('(.*?)/',sentence)
    words=''
    for eachword in word[::]:
        if len(eachword)>2:
            wordlist=eachword[0]+'\t'+'B'+'\n'+middle(eachword)+eachword[-1]+'\t'+'E'+'\n'
            words=words+wordlist
        elif len(eachword)>1:
            wordlist=eachword[0]+'\t'+'B'+'\n'+eachword[-1]+'\t'+'E'+'\n'
            words=words+wordlist
        elif len(eachword)==1:
            if eachword==' ':
                wordlist=eachword[0]+'\t'+'\n'
                words=words+wordlist
            else:
                wordlist=eachword[0]+'\t'+'BE'+'\n'
                words=words+wordlist
        else:
            pass
with open('test.txt','w',encoding='utf-8',errors='ignore') as f4:
    f4.write(words)   #得到使用Python对其以词为单位进行标注的最终test文件