from TableRule import tableRule
import operator

class evaluate():

    def __init__(self,dictionary,moveHead,tim):
        self.time=tim
        self.body=moveHead
        self.move=dictionary
        self.direction = {'F': 0, 'R': 0, 'L': 0, 'U': 0, 'D': 0}

    def calc(self):
        self.direction['F']=self.move['F']
        self.direction['R']=self.move['R']+self.move['Rp']
        self.direction['L'] = self.move['L'] + self.move['Lp']
        self.direction['U'] = self.move['U']
        self.direction['D'] = self.move['D']


    def MaxMin(self):
        sum=0
        dic={}



        for key, value in self.direction.items():
            sum+=value

        maxKey = ""
        minKey = ""
        up = False
        down = False

        if sum!=0:
            for key, value in self.direction.items():
                dic[key]=(value/sum)*100


            min=9999



            for key, value in dic.items():
                if value>50 :
                    maxKey=key

                if value<25 and value<min and key!='U' and key!='D' and value!=0:
                    min=value
                    minKey=key

                if key=='D' and value>25 and value<50:
                    down=True

                if key=='U' and value>25 and value<50:
                    up=True

        return maxKey,minKey,up,down

    def evaluate_body(self):
        hour,minite,sec=self.time.split(":")

        print (hour,minite,sec)
        hourtom=int(float(hour)*60)
        sectom=int(float(sec)/60)
        total=hourtom+sectom+int(float(minite))
        total=int(total/2)
        if total==self.body:
            return True
        elif total<self.body:
            return "more"
        elif total>self.body:
            return "less"



    def result(self):

        listMessage=[]
        mistake=False


        for key,value in self.move.items():
            if value ==0 and key!='LError' and key!='RError':
                mistake=True
        numOfMove = self.evaluate_body()
        if not mistake and numOfMove==True :
            listMessage.append(tableRule["goodAllDirection"])

        if self.move['L']==0 and self.move['Lp']==0:
            listMessage.append(tableRule["L0"])

        if self.move['R']==0 and self.move['Rp']==0:
            listMessage.append(tableRule["R0"])

        if self.move["U"]==0 :
            listMessage.append(tableRule["U0"])

        if self.move["D"]==0 :
            listMessage.append(tableRule["D0"])


        if self.move["F"]==0 :
            listMessage.append(tableRule["F0"])

        if self.move['L']==0 and self.move['Lp']!=0:
            listMessage.append(tableRule["L-Lp0"])

        if self.move['R']==0 and self.move['Rp']!=0:
            listMessage.append(tableRule["R-Rp0"])

        self.calc()

        max,min,up,down=self.MaxMin()
        if max!=min:
            if max!='':
                listMessage.append(tableRule[max+"m"])
            if min!='':
                listMessage.append(tableRule[min + "f"])


        if self.move['RError']!=0:
            listMessage.append(tableRule["RError"])

        if self.move['LError']!=0:
            listMessage.append(tableRule["LError"])

        if up :
            listMessage.append(tableRule["U"])

        if down :
            listMessage.append(tableRule["D"])

        if numOfMove=="more":
            listMessage.append(tableRule["M"])
        elif numOfMove=="less":
            listMessage.append(tableRule["Lm"])

        return listMessage
