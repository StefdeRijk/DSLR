import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data = pd.read_csv('datasets/dataset_train.csv')
    data.drop(['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand'], axis=1, inplace=True)

    house_names = data['Hogwarts House'].unique()
    house_data = {}
    for house in house_names:
        house_data[house] = data[data['Hogwarts House'] == house]
        house_data[house].drop('Hogwarts House', axis=1, inplace=True)

    fig, ax = plt.subplots(3, 5)

    i = 0
    j = 0

    for column in house_data[house_names[0]].columns:
        if i > 4:
            i = 0
            j += 1

        subplot = ax[j, i]

        for house in house_names:
            subplot.hist(house_data[house][column], alpha=0.25, label=house)

        subplot.set_title(str(column))
        handles, labels = subplot.get_legend_handles_labels()
        i += 1

    plt.legend(handles, labels, loc='upper center')
    plt.subplots_adjust(left=0.06, right=0.94, top=0.94, bottom=0.06)
    plt.show()
