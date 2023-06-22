from flask import Flask,render_template,request,send_file
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvaimport matplotlib.pyplot as plt
import numpy as np
from numpy import pi
import pandas as pd
import pygal
    


app=Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')

@app.route('/cunit')
def cunit():
    return render_template('unitinput.html')

@app.route('/unit', methods=['GET', 'POST'])
def unit():
    msg=[0]*6
    detail=request.form
    type=int(detail['type'])
    val=float(detail['value'])
    dp=int(detail['round'])
    if type==1:
        msg[0]=round(val*3.2808,dp)
        msg[1]=round(val/1000,dp)
        msg[2]=round(msg[1]*1.609,dp)
        msg[3]=round(val*100,dp)
        msg[4]=round(msg[3]/2.54,dp)
        msg[5]=round(msg[0]/3,dp)
        li=['feet','kilometer','miles','centimeter','inch','yard']
        return render_template('unit1.html',msg=msg,li=li)
    elif type==2:
        msg[0]=round(val*10.7639,dp)
        msg[1]=round(val*1.1959,dp)
        msg[2]=round(msg[0]/107639,dp)
        msg[3]=round(val/4046.86,dp)
        li=['square ft','square yard','hectare','acre']
        return render_template('unit2.html',msg=msg,li=li)
    else:
        msg[0]=round(val*35.3147,dp)
        msg[1]=round(val*61023.7,dp)
        li=['cubic ft','cubic inch']
        return render_template('unit3.html',msg=msg,li=li)


@app.route('/cpaint')
def cpaint():
    return render_template('paintinput.html')

@app.route('/paint', methods=['GET', 'POST'])
def paint():
    msg=[]
    detail=request.form
    carea=float(detail['carea'])
    dh=float(detail['dhieght'])
    dw=float(detail['dwidth'])
    dn=int(detail['ndoor'])
    wh=float(detail['whieght'])
    ww=float(detail['wwidth'])
    wn=int(detail['nwindow'])

    areap=carea*3.5
    aread=dh*dw*dn
    areaw=wh*ww*wn

    apa=areap-aread-areaw
    msg.append(apa)
    paint=apa/100
    msg.append(paint)
    primer=apa/100
    msg.append(primer)
    putty=apa/40
    msg.append(putty)



    return render_template('paintoutput.html',msg=msg)

@app.route('/cbrick')
def cbrick():
    return render_template('brickinput.html')

@app.route('/brick',methods=['GET','POST'])
def brick():
    msg=[]
    wt=0
    detail=request.form
    l=float(detail['length'])
    l=l*0.3048
    h=float(detail['height'])
    h=h*0.3048
    t=int(detail['thick'])
    if t==1:
        wt=0.1
    else:
        wt=0.23
    ratio=int(detail['grade'])
    #tup=[(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9)]
    bl=float(detail['blength'])
    bl=bl/100
    bh=float(detail['bh'])
    bh=bh/100
    bw=float(detail['bwidth'])
    bw=bw/100
    vol=l*h*wt
    bvol=bl*bh*bw
    bvolm=(bl+0.01)*(bh+0.01)*(bw+0.01)
    nb=vol/bvolm
    avolbm=nb*bvol
    qm=vol-avolbm
    qm=qm+(qm*0.15)
    qm=qm+(qm*0.25)
    cem=(1/(1+ratio+2))*qm
    cbag=cem/0.035
    ckg=cbag*50
    sand=(ratio+2)/(1+ratio+2)*qm
    skg=sand*1500
    ston=skg/1000
    msg.append(round(vol,2))
    msg.append(round(nb))
    msg.append(round(cbag))
    msg.append(round(ckg,2))
    msg.append(round(ston,2))
    msg.append(round(skg,2))
    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'BRICKS MASONRY CALCULATOR'
    results=[(msg[3],'Cement'),(msg[5],'Sand')]
    for r in results:
        pie_chart.add(r[1], r[0])
    pie_chart.value_formatter = lambda x: "%.15f" % x
    piech=pie_chart.render_data_uri()

    html= render_template('brickoutput.html', msg=msg, piech=piech)
    return html


@app.route('/cconcrete')
def cconcrete():
    return render_template('concreteinput.html')

@app.route('/concrete', methods=['GET', 'POST'])
def concrete():
    msg=[]
    detail=request.form
    sr=0
    cr=0
    ar=0
    grade=int(detail['grade'])
    l=float(detail['length'])
    w=float(detail['width'])
    d=float(detail['depth'])
    if grade==1:
        cr=1
        sr=1.5
        ar=3

    elif grade==2:
        cr=1
        sr=2
        ar=4
    elif grade==3:
        cr=1
        sr=3
        ar=6
    else:
        cr=1
        sr=4
        ar=8
    sumr=ar+cr+sr
    vol=l*d*w
    volm=vol*0.0283
    msg.append(vol)
    wvol=volm+(volm*(0.524))
    cvol= (cr/sumr)*wvol

    svol=(sr/sumr)*wvol

    avol=(ar/sumr)*wvol

    cbag=cvol/0.035
    msg.append(round(cbag))
    ckg=cbag*50
    msg.append(round(ckg,2))
    skg=svol*1550
    msg.append(round(skg,2))
    ston=skg/1000
    msg.append(round(ston,2))
    akg=avol*1350
    msg.append(round(akg,2))
    aton=akg/1000 
    msg.append(round(aton,2))

    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'Approx. cost on various work of materials'
    results=[(msg[2],'Cement'),(msg[3],'Sand'),(msg[5],'Aggregate')]
    for r in results:
        pie_chart.add(r[1], r[0])
    pie_chart.value_formatter = lambda x: "%.15f" % x
    piech=pie_chart.render_data_uri()

    html= render_template('concoutput.html', msg=msg, piech=piech)
    return html
    
    
    

@app.route('/ccost')
def ccost():
    return render_template('main.html')

@app.route('/cfloor')
def floor():
    return render_template('floorinput.html')

@app.route('/floor',methods=['GET','POST'])
def costfloor():
    li=[]
    detail=request.form
    l=float(detail['length'])
    w=float(detail['width'])
    tl=float(detail['tlength'])
    tw=float(detail['twidth'])
    area=l*w
    aream=area*0.02831
    am=aream*0.07
    cbag=(am/7)/0.035
    ckg=cbag*50
    ntile=area/(tl*tw)
    skg=((am*6)/7)*1550
    ston=skg/1000
    li.append(l)
    li.append(w)
    li.append(tl)
    li.append(tw)
    li.append(area)
    li.append(round(cbag))
    li.append(round(ckg,2))
    li.append(ntile)
    li.append(round(skg,2))
    li.append(round(ston,2))

    pie_chart = pygal.Pie(height=300)
    results=[(li[6],'Cement'),(li[8],'Sand')]
    pie_chart.title = 'Flooring quantity'
    for r in results:
        pie_chart.add(r[1], r[0])
    pie_chart.value_formatter = lambda x: "%.15f" % x
    piech=pie_chart.render_data_uri()

    html= render_template('flooroutput.html',msg=li, piech=piech)

    return html


@app.route('/input',methods=['GET','POST'])
def input():
    msg=[]
    detail=request.form
    builtup=int(detail['builtup'])
    cost=int(detail['cost'])
    msg.append(builtup)
    msg.append(cost)
    tot=cost*builtup
    msg.append(tot)
    msg.append(0.164*tot)
    msg.append(0.123*tot)
    msg.append(0.0742*tot)
    msg.append(0.246*tot)
    msg.append(0.165*tot)
    msg.append(0.228*tot)
    msg.append(0.4*builtup)
    msg.append(0.816*builtup)
    msg.append(0.608*builtup)
    msg.append(4*builtup)
    msg.append(0.18*builtup)
    msg.append(8*builtup)
    msg.append(1.3*builtup)
    msg.append(0.27*tot)
    msg.append(0.184*tot)
    msg.append(0.111*tot)
    msg.append(0.169*tot)
    msg.append(0.178*tot)
    msg.append(0.139*tot)





    results = [(msg[3],'Cement'),(msg[4],'Sand'),(msg[5],'Aggregate'),(msg[6],'Steel'),(msg[7],'Finishers'),(msg[8],'Fittings')]

    pie_chart = pygal.Pie(height=500)
    pie_chart.title = 'Approx. cost on various work of materials'
    for r in results:
        pie_chart.add(r[1], r[0])
    pie_chart.value_formatter = lambda x: "%.15f" % x
    piech=pie_chart.render_data_uri()


    bar_chart = pygal.Bar(height=500)  # instance of Bar class
    bar_chart.title = 'Construction cost Splitup for 6 months'  # title of bar chart
    bar_chart.add('cost', [msg[16],msg[17],msg[18],msg[19],msg[20],msg[21]])  # add fibo data to chart
    bar_chart.x_labels = 'Month 1','Month 2','Month 3','Month 4','Month 5','Month 6'
    chart = bar_chart.render_data_uri()  

    
    html = render_template(
    'output.html',
    msg=msg,
    piech=piech,
    chart=chart   
    )
    return (html)


if __name__=='__main__':
    app.run(debug=True)
