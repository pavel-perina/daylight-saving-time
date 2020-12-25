# matplotlib, pandas, suntime, ipykernel (vscode)
# https://www.nordtheme.com


#%%
import datetime
from suntime import Sun
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np


#%%
# Brno, CZ
locName = "Brno"
sun = Sun(49.2030375, 16.5828792)
print("{} sunrise {}, sunset {}".format(locName, sun.get_sunrise_time().strftime("%H:%M UTC"), sun.get_sunset_time().strftime("%H:%M UTC") ))

#for day in pd.date_range(date(2020,1,1), date(2020,12,31)):
#    print ("{}".format(day.strftime("%Y-%m-%d")))


#%%
def createUtcData(sun):
    dateRange = pd.date_range(datetime.date(2020,1,1), datetime.date(2020,12,31))
    rises = []
    sets = []
    risesF = []
    setsF = []
    for d in dateRange:
        srise = sun.get_sunrise_time(d).time()
        sset  = sun.get_sunset_time(d).time()
        rises.append(srise)
        sets.append(sset)
        risesF.append(srise.hour + srise.minute/60.0 + srise.second/3600.0)
        setsF.append (sset.hour  + sset.minute/60.0  + sset.second/3600.0)
    df = pd.DataFrame({"Date" : dateRange, "Sunrise": rises, "Sunset": sets, "SunriseF": risesF, "SunsetF":setsF}, index=dateRange)
    return df


#%%    
def createWinter(dfUtc):
    df = dfUtc.copy()
    df.SunriseF = dfUtc.SunriseF+1
    df.SunsetF  = dfUtc.SunsetF +1
    return df


def createSummer(dfUtc):
    df = dfUtc.copy()
    df.SunriseF = dfUtc.SunriseF+2
    df.SunsetF  = dfUtc.SunsetF +2
    return df


def createDst(dfUtc):
    df = dfUtc.copy()
    for i in range(0, 366):
        inc = 1
        if (i > 87 and i < 298):
            inc = 2
        df.SunriseF[i] += inc
        df.SunsetF[i]  += inc
    return df


#%%
def plotRiseSetLeft(df, ax1):
    #ax1.set_facecolor("#eceff4")
    ax1.set_title("Východ a západ slunce")
    ax1.set_ylim([0,24])
    ax1.set_yticks(range(0,25,1))
    ax1.set_yticks(np.arange(0.0, 24, 0.25), minor=True)
    ax1.set_ylabel("Čas")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%02d:00"))
    ax1.set_xlim([datetime.date(2020,1,1), datetime.date(2020,12,31)])
    ax1.set_xlabel("Datum")
    ax1.grid(True)
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax1.fill_between(df["Date"], df["SunriseF"], df["SunsetF"], facecolor="#EBCB8B", alpha=0.2)
    ax1.plot(df["Date"], df["SunriseF"], color="#D08770")
    ax1.plot(df["Date"], df["SunsetF"], color="#5E81AC")


def makeHist(df):
    nBins = 24*4
    sr_hist, sr_edges = np.histogram(df.SunriseF, bins=nBins, range=(0,24))
    ss_hist, ss_edges = np.histogram(df.SunsetF,  bins=nBins, range=(0,24))
    dfHist =pd.DataFrame({"Bin" : ss_edges[:-1], "Sunsets" : ss_hist, "Sunrises" : sr_hist})
    return dfHist


def plotRiseSetRight(dfHist, ax2):
    ax2.set_title("Histogram")
    ax2.set_ylim([0,24])
    ax2.set_yticks(range(0,25,1))
    ax2.set_yticks(np.arange(0.0, 24, 0.25), minor=True)
    ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter("%02d:00"))
    ax2.set_ylabel("Čas")
 
    ax2.set_xlim([0,50])
    ax2.set_xlabel("Počet dní, kdy východ/západ připadá na čtvrthodinu")
    ax2.barh(dfHist["Bin"], dfHist["Sunrises"], align="edge", color="#D08770", height=0.25)
    ax2.barh(dfHist["Bin"], dfHist["Sunsets"],  align="edge", color="#5E81AC", height=0.25)
    ax2.grid(True)


def plotRiseSet1(df, filename = "", title=""):
    fig,(ax1,ax2) = plt.subplots(1,2)
    plotRiseSetLeft(df, ax1)
    dfHist = makeHist(df)
    #dfHist.to_csv("c:\\temp\\hist.csv")
    plotRiseSetRight(dfHist, ax2)
    if (title != ""):
        fig.suptitle(title)
    if (filename != ""):
        plt.savefig(filename)
    else:
        plt.show()


def plotRiseSetCompare(dfWin, dfSum, dfDst, filename = ""):
    fig,(ax1,ax2,ax3) = plt.subplots(1,3)
    plotRiseSetRight(makeHist(dfWin), ax1)
    plotRiseSetRight(makeHist(dfSum), ax2)
    plotRiseSetRight(makeHist(dfDst), ax3)
    ax1.set_title("Standardní/zimní čas")
    ax2.set_title("Letní čas")
    ax3.set_title("Střídání času")
    fig.suptitle("{} - Srovnání".format(locName))
    if (filename != ""):
        plt.savefig(filename)
    else:
        plt.show()
    

#%%
# does not work :-(
def plotRiseSet2(df):
    plt.ylim([datetime.time.min, datetime.time.max]) 
    # The above y limits do not force the y axis to run a full 24 hours, so force manual axes tick values.
    # Give a range of values in seconds and matplotlib is clever enough to work it out:
    plt.yticks(range(0, 60*60*25, 2*60*60))


#%%
dfUtc = createUtcData(sun)
dfSum = createSummer(dfUtc)
dfWin = createWinter(dfUtc)
dfDst = createDst(dfUtc)
#%%
plt.rcParams["figure.figsize"] = (19.2, 10.8)
#plt.rcParams["savefig.facecolor"] = "#D8DEE9"
plt.rcParams["axes.facecolor"] = "#eceff4"
plotRiseSet1(dfSum, filename="c:\\temp\\cas-{}-letni.png".format(locName), title="{} - Letní čas celý rok".format(locName))
plotRiseSet1(dfWin, filename="c:\\temp\\cas-{}-zimni.png".format(locName), title="{} - Standardní čas celý rok".format(locName))
plotRiseSet1(dfDst, filename="c:\\temp\\cas-{}-stridani.png".format(locName), title="{} - Střídání času".format(locName))
plotRiseSetCompare(dfWin, dfSum, dfDst, "c:\\temp\\cas-{}-srovnani.png".format(locName))
