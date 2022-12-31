import re
#資料預處理
def dataPreProcessing(data):
    ProcessedData = re.sub('[：「『《（」』》）]|\[.*?\]', '', data)
    dataReg = re.compile(r'(.*?)[；|，|、|。]+')
    listProcessedData = dataReg.findall(ProcessedData)
    return listProcessedData

#N-gram
def ngram(data,n):
    model = []
    idx = -1
    for d in data:
        for i in range(len(d)-n):
            curStr = d[i:i+n]
            nextStr = d[i+n]
            idx = isAppend(model,curStr)
            if idx!=-1:
                if nextStr in model[idx][1]:
                    model[idx][1][nextStr]+=1
                else:
                    model[idx][1][nextStr]=1
            else:
                l = list()
                l.append(curStr)
                l.append({nextStr:1})
                model.append(l);
    return model

def isAppend(l,s):
    for i in range(len(l)):
        if l[i][0] == s:
            return i
    return -1

def findWord(model,word):
    for i in range(len(model)):
        if model[i][0]==word:
            return i
    return -1
        
#機率模型的建立
def modelProbability(model):
    prob_model = model[:]
    for i in range(len(model)):
        total = 0
        for j in model[i][1]:
            total += model[i][1][j]
        for j in model[i][1]:
            prob_model[i][1][j] = round(model[i][1][j]/total,4)
    return prob_model
        


filename = 'data.txt'
f = open('./'+filename,'r',encoding="utf-8")
text = f.read()
f.close()
ProcessedText = dataPreProcessing(text)
#bigram 可修改ngram中的第二個參數來修該所使用的N-gram
text_model = ngram(ProcessedText,2)
text_model_prob = modelProbability(text_model)
print("按下CTRL+C來進行結束")
try:
    while True:
        #使用者須輸入與N-gram相同字元的字詞
        word = input("請輸入欲查詢的字：")
        idx = findWord(text_model_prob,word)
        if idx == -1:
            print("查無此字")
        else:
            print("最有可能的下一個字與其機率為：")
            l = text_model_prob[idx][1]
            l = sorted(l.items(),key=lambda s:s[1],reverse=True)
            for i in range(min(5,len(l))):
                print(l[i][0],":",end=" ")
                print(l[i][1])
        print()
except KeyboardInterrupt:
    print("\n結束")
