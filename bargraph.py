import matplotlib.pyplot as plt
import os
# positive = 50
# negative = 50


def barchartgenerator(positivecount, negativecount,hotelname):
    figure =plt.figure(figsize=(7,5))
    filename =hotelname+'.png'
    path = os.path.abspath(os.curdir)+'/static/images/'+ filename
    names = ["positive Tweets","Negative Tweets"]
    
    scores = [positivecount,negativecount]
    total = positivecount+negativecount
    scores2 =[total, total]
    positions = [0,1]
    positions2 = [0.3,1.3]
    colors =['green','red'] 
    # if(positive>negative):
    #     height1 = positive +50
    # else:
    #     height1 = negative +50
    plt.bar(positions,scores,width =0.3, color =['red','green'])
    plt.bar(positions2, scores2, width=0.3)
    plt.xticks(positions, names)
    plt.ylabel('Number of Tweets')
    figure.savefig(path)
    print("Bar graph generated !")

    return filename
    # plt.show()

# barchartgenerator(200,100,'hyatthotel')