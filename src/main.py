import numpy as np
import streamlit as st
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import PIL.Image as Image


def createDummyData():
    # create 3 * 24 data points
    rawdata = np.random.randn(24, 2)
    tagsList = ["Python", "C++", "Java", "JavaScript", "Rust", "Networking", "Security"]
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
    # add multiselect for the repo names
    selectedRepos = st.sidebar.multiselect(
        "Select Repositories to Display",
        list(dummyRepoJSON.keys()),
        default=list(dummyRepoJSON.keys()),
    )

    # filter out the selected repos
    filteredData = {k: v for k, v in dummyRepoJSON.items() if k in selectedRepos}

    # 1 chart per repo, 3 charts per row
    columns = st.columns(3)
    for i, (repo, data) in enumerate(filteredData.items()):
        col = columns[i % 3]
        col.title(repo)
        col.line_chart(data["data"])


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

    # create non-linear continuous cmap from good and bad colours in session state
    cmap = LinearSegmentedColormap.from_list(
        "custom",
        [
            st.session_state.badColour,
            st.session_state.badColour,
            "white",
            st.session_state.goodColour,
            st.session_state.goodColour,
        ],
    )
    sns.set_theme(rc={"figure.figsize": (12, 4)})

    # display seaborn heatmap on streamlit. # decrease transparency along the X-axis
    hmp = sns.heatmap(
        avgData,
        annot=False,
        cmap=cmap,
        cbar=False,
        xticklabels=False,
        yticklabels=False,
        linewidths=0,
        linecolor="black",
    )

    # save heatmap to image
    hmp.get_figure().savefig("src/overallHealth.png")
    # load with PIL
    img = Image.open("src/overallHealth.png")
    # convert to RGBA
    img = img.convert("RGBA")
    # to array
    img = np.array(img)
    # create 2D np.zeros array with same shape as image
    mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
    # set transparency of pixels to be dependent on the column
    mask[:, :, 0] = np.linspace(0, 255, img.shape[1], dtype=np.uint8)
    # set alpha channel of image to be the mask
    img[:, :, 3] = mask[:, :, 0]
    # display image
    st.image(img, caption="Overall Health", use_column_width=True)


def sideBar():
    """Side bar for user input"""
    st.sidebar.title("Customisation")
    st.sidebar.write(
        "Here you can customise the colours of the heatmap, as well as filter the data to select certain repos, tags, and metrics."
    )
    # Porivde 2 colour pickers for a 'Good/Positive' and 'Bad/Negative' colour
    cols1, cols2 = st.sidebar.columns(2)
    with cols1:
        goodColour = st.color_picker("**Good**", "#00FF00")
    with cols2:
        badColour = st.color_picker("**Bad**", "#FF0000")

    # add to session states
    st.session_state.goodColour = goodColour
    st.session_state.badColour = badColour


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


if __name__ == "__main__":
    main()
