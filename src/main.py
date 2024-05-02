import numpy as np
import streamlit as st
import seaborn as sns
import PIL.Image as Image
import json

from matplotlib.colors import LinearSegmentedColormap


def processuiJSON(uiJSON):
    """Process the JSON file to be used in the UI
    List of dicts (one for each Repo) containing:
    "metadata"
    "repository"["display_name"]
    "repository"["url"]
    "metrics"{} # dict of metrics

    """
    # load the JSON file
    with open(uiJSON, "r") as f:
        data = json.load(f)
    # data is list of dicts

    # reorder into dict of dicts, with display_name as key
    data = {repo["repository"]["display_name"]: repo for repo in data}

    return data


def individualDataDisplay(dummyRepoJSON):
    # add multiselect for the repo names
    selectedRepos = st.sidebar.multiselect(
        "Select Repositories to Display",
        list(dummyRepoJSON.keys()),
        default=list(dummyRepoJSON.keys()),
    )

    # filter out the selected repos
    filteredData = {k: v for k, v in dummyRepoJSON.items() if k in selectedRepos}

    # get list of metrics
    metrics = list(filteredData.values())[0]["metrics"].keys()

    # add multiselect for the metrics
    selectedMetrics = st.sidebar.multiselect(
        "Select Metrics to Display", metrics, default=metrics
    )
    # determine number of columns based on number of selected repos (max 3)
    numCols = min(len(filteredData), 3)
    cols = st.columns(numCols)
    for i, (repoName, repoData) in enumerate(filteredData.items()):
        with cols[i % numCols]:
            # for each repo, display the data
            st.header(f"**{repoName}**")
            # display metric if selected
            for metric in selectedMetrics:
                # get the data for the metric
                try:
                    data = repoData["metrics"][metric]["score"]
                    st.write(f"**{metric}**")
                    # st.metrric with random into delta
                    st.metric(label=metric, value=data, delta=np.random.uniform(-1, 1))
                except:
                    pass


def overallDataDisplay(dummyRepoJSON):
    """Full Width chart showing aggregated data"""
    # create 1*365 array of random values
    avgData = np.random.rand(1, 365)

    # create non-linear continuous cmap from good and bad colours in session state
    cmap = LinearSegmentedColormap.from_list(
        "custom",
        [
            st.session_state.badColour,
            st.session_state.goodColour,
        ],
    )
    sns.set_theme(rc={"figure.figsize": (12, 4), "figure.facecolor": "black"})

    # display seaborn heatmap on streamlit. # no surrounding whitespace
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
    hmp.get_figure().savefig("src/overallHealth.png", bbox_inches="tight")
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
    st.image(img, use_column_width=True)


def sideBar():
    """Side bar for user input"""
    st.sidebar.title("Customisation")
    st.sidebar.write(
        "Here you can customise the colours of the heatmap, as well as filter the data to select certain repos, tags, and metrics."
    )
    # Porivde 2 colour pickers for a 'Good/Positive' and 'Bad/Negative' colour
    cols1, cols2 = st.sidebar.columns(2)
    with cols1:
        goodColour = st.color_picker("**Good**", "#34C900")
    with cols2:
        badColour = st.color_picker("**Bad**", "#000000")

    # add to session states
    st.session_state.goodColour = goodColour
    st.session_state.badColour = badColour


def main():
    sideBar()
    data = processuiJSON("src/data/ui.json")
    # show overall data
    overallDataDisplay(data)
    st.title("RSE Software Community Health")
    st.divider()

    # show individual data

    # layout is a grid with 3 columns, with 1 chart in each column
    individualDataDisplay(data)


if __name__ == "__main__":
    main()
