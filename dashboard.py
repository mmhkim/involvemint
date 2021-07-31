#from altair.vegalite.v4.api import condition
from PIL import Image
import streamlit as sl
import pandas as pd
import altair as alt
import seaborn as sns

# helper function that makes bar graph
def makeBar(df, yValue, texts, width, height, scale=0):
    # if pre determined scale doesnt exist
    if(scale == 0):
        scale = df[yValue].max()
    
    # create the bars
    bar = alt.Chart(df).mark_bar().encode(
        x = alt.X("Month", sort=df["Month"].tolist()), 
        y = alt.Y(yValue, scale=alt.Scale(domain=[0, scale]))
    ).properties(
        width= width,
        height= height,
        title = texts + " vs. Months"
    )

    # create the texts
    smallText = bar.mark_text(
        align='center',
        baseline='bottom'
    ).encode(
        text= texts
    )

    return bar, smallText

sl.image(Image.open("logoimage.png"))
sl.title("Minting and Transaction Report")
sl.write(""" ### Find the minting and tranascation reports below
""")

mintOrTrx  = sl.selectbox("Choose which report to analyze", ("Minting", "Transaction")) 

if(mintOrTrx == "Minting"):
    df = pd.read_csv("julymintingreport2021.csv")
    
    # total credits minted

    totalMint, text = makeBar(df, 'Total Credits Minted', 'Total Credits Minted', 720, 480)

    sl.write(totalMint+text)

    startDate = sl.date_input("Give Start Date")
    endDate = sl.date_input("Give End Date")
    startDate = startDate.strftime('%b-%Y').replace("20", "", 1)
    endDate = endDate.strftime('%b-%Y').replace("20", "", 1)

    startIndex = df[df["Month"] == startDate].index.values[0]
    endIndex = df[df["Month"] == endDate].index.values[0]

    if(endIndex - startIndex <= 0):
        sl.write("This is not a real time frame")

    else:

        df = df.iloc[startIndex:endIndex+1]
        
        # adjust the scaling of bar chart
        cmMax = df["Avg Credits per CM"].max()


        melted = pd.melt(df, id_vars = ['Month'], value_vars=['Avg Credits per POI', 'Avg Credits per CM'])

        bar = alt.Chart(melted).mark_bar().encode(
            x = alt.X("variable"), 
            y = alt.Y("value"),
            color = 'variable',
            column= alt.Column('Month', sort=melted["Month"].tolist())
        ).properties(   
            title = " Amount vs. Months"
        )
        sl.write(bar)


        avgPOI, poiText = makeBar(df, 'Avg Credits per POI', 'Avg Credits per POI', 360, 240, cmMax)
        avgCM, cmText = makeBar(df, 'Avg Credits per CM', 'Avg Credits per CM', 360, 240)

        sl.write(avgPOI+poiText|avgCM+cmText)

else:

    trxType  = sl.selectbox("Choose which transaction report to analyze", ("Monthly Overall", "Monthly by Type", "Weekly by Type")) 

    if(trxType == "Monthly Overall"):
        monthly_df = pd.read_csv("julymonthlytxreport2021.csv")

        # make transaction count bar chart
        totalMonthly, text = makeBar(monthly_df, 'Transaction Count', 'Transaction Count', 720, 480)

        sl.write(totalMonthly+text)

        # rewrite and create total trx amount bar chart
        totalMonthly, text = makeBar(monthly_df, 'Total Trx Amount', 'Total Trx Amount', 720, 480)

        sl.write(totalMonthly+text)
    
    elif(trxType == "Monthly by Type"):
        # creates monthly by type
        monthly_df = pd.read_csv("julymonthlytxtypereport2021.csv", index_col="Month")
        sl.write(monthly_df)
    
    elif(trxType == "Weekly by Type"):
        # creates weekly by type
        weekly_df = pd.read_csv("julyweeklytxtypereport2021.csv", index_col="Month")
        sl.write(weekly_df)
