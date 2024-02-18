import pandas as pd
import matplotlib.pyplot as plt
import argparse


def show_one(data, house_names, x_course, y_course):
    for house in house_names:
        plt.scatter(data[house][x_course], data[house][y_course], alpha=0.25, label=house)

        plt.xlabel(str(x_course))
        plt.ylabel(str(y_course))

    plt.legend(frameon=False)
    plt.title('Relationship between ' + str(x_course) + ' and ' + str(y_course))
    plt.show()


def show_all(data, house_names):
    fig, ax = plt.subplots(len(house_data[house_names[0]].columns), len(house_data[house_names[0]].columns))

    i = 0
    j = 0

    for row in data[house_names[0]].columns:
        for column in house_data[house_names[0]].columns:
            subplot = ax[j, i]

            for house in house_names:
                subplot.scatter(data[house][column], data[house][row], alpha=0.25, label=house)

            if j == len(data[house_names[0]].columns) - 1:
                subplot.set_xlabel(str(column), fontsize=8)
            if i == 0:
                subplot.set_ylabel(str(row), fontsize=8, rotation=0, horizontalalignment='right')
            subplot.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
            handles, labels = subplot.get_legend_handles_labels()
            i += 1

        i = 0
        j += 1

    plt.legend(handles, labels, loc='upper center', prop={'size': 6})
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Settings for the scatter plot')
    parser.add_argument('--show_all', type=bool, required=False, default=False,
                        help='If true, shows scatter plots of all combinations of courses')
    args = parser.parse_args()

    data = pd.read_csv('datasets/dataset_train.csv')
    data.drop(['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand'], axis=1, inplace=True)

    house_names = data['Hogwarts House'].unique()
    house_data = {}
    for house in house_names:
        house_data[house] = data[data['Hogwarts House'] == house]
        house_data[house].drop('Hogwarts House', axis=1, inplace=True)

    if args.show_all:
        show_all(house_data, house_names)
    else:
        show_one(house_data, house_names, 'Defense Against the Dark Arts', 'Astronomy')
