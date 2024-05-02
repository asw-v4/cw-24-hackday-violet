import numpy as np
import streamlit as st
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap


def createDummyData():
    # create 3 * 24 data points
    rawdata = np.random.randn(24, 3)
    tagsList = ["Python", "C++", "Java", "JavaScript", "Rust"]
    # select a random sample of tags
    numTags = np.random.randint(1, 5)
    tags = np.random.choice(tagsList, numTags, replace=False)

    dummyData = {
        "data": rawdata,
        "tags": tags,
    }
    return dummyData


def getDummyRepoInformation():
    dummyData = {
        "repo1": createDummyData(),
        "repo2": createDummyData(),
        "repo3": createDummyData(),
        "repo4": createDummyData(),
    }
    return dummyData


def individualDataDisplay(dummyRepoJSON):
    # 1 chart per repo, 3 charts per row
    columns = st.columns(3)
    for i, (repo, data) in enumerate(dummyRepoJSON.items()):
        col = columns[i % 3]
        col.title(repo)
        col.line_chart(data["data"])


def main():
    sideBar()
    dummyRepoJSON = getDummyRepoInformation()
    # show overall data
    overallDataDisplay(dummyRepoJSON)
    st.title("RSE Software Community Health")
    st.divider()

    # show individual data

    # layout is a grid with 3 columns, with 1 chart in each column
    individualDataDisplay(dummyRepoJSON)


def overallDataDisplay(dummyRepoJSON):
    """Full Width chart showing aggregated data"""
    # # collate all data points and average
    allData = np.array([data["data"] for data in dummyRepoJSON.values()])
    avgData = np.mean(allData, axis=0)
    # average into 1 axis
    avgData = np.mean(avgData, axis=1)
    # expand dims to 2D
    avgData = np.expand_dims(avgData, axis=1)
    # rotate to horizontal
    avgData = np.transpose(avgData)

    st.write(st.session_state.goodColour)
    # create continuous cmap from good and bad colours in session state
    cmap = LinearSegmentedColormap.from_list(
        name="custom",
        colors=[st.session_state.badColour, "white", st.session_state.goodColour],
    )

    # display seaborn heatmap on streamlit
    hmp = sns.heatmap(
        avgData,
        annot=False,
        fmt=".2f",
        cmap=cmap,
        cbar=False,
        xticklabels=False,
        yticklabels=False,
        square=False,
        linewidths=0,
        linecolor="black",
    )

    st.pyplot(hmp.get_figure())


def sideBar():
    """Side bar for user input"""
    st.sidebar.title("User Input")
    # Porivde 2 colour pickers for a 'Good/Positive' and 'Bad/Negative' colour
    goodColour = st.sidebar.color_picker("Good Colour", "#00FF00")
    badColour = st.sidebar.color_picker("Bad Colour", "#FF0000")

    # add to session states
    st.session_state.goodColour = goodColour
    st.session_state.badColour = badColour


if __name__ == "__main__":
    main()
