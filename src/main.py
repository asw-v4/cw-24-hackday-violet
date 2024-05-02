import numpy as np
import streamlit


def createDummyData():
    # create 3 * 24 data points
    data = np.random.randn(3, 24)
    return data


def main():
    streamlit.title("Violet Hack Day")

    data = createDummyData()

    # avg data across 0 dimension
    avg_data = np.mean(data, axis=0)
    streamlit.line_chart(avg_data)

    # display 3 plots, one for each line
    for i in range(3):
        streamlit.line_chart(data[i, :])


if __name__ == "__main__":
    main()
