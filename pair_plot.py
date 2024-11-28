import pandas as pd
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None


if __name__ == '__main__':
    data = pd.read_csv('datasets/dataset_train.csv')
    data.drop(['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand'], axis=1, inplace=True)

    house_names = data['Hogwarts House'].unique()
    house_data = {}
    for house in house_names:
        house_data[house] = data[data['Hogwarts House'] == house]
        house_data[house].drop('Hogwarts House', axis=1, inplace=True)

    fig, ax = plt.subplots(len(house_data[house_names[0]].columns), len(house_data[house_names[0]].columns), figsize=(30, 20))

    i = 0
    j = 0

    for row in house_data[house_names[0]].columns:
        for column in house_data[house_names[0]].columns:
            subplot = ax[j, i]

            if row == column:
                for house in house_names:
                    subplot.hist(house_data[house][column], alpha=0.25, label=house)
            else:
                for house in house_names:
                    subplot.scatter(house_data[house][column], house_data[house][row], alpha=0.25, label=house)

            handles, labels = subplot.get_legend_handles_labels()
            if j == len(house_data[house_names[0]].columns) - 1:
                subplot.set_xlabel(str(column).replace(' ', '\n'), fontsize=8)
            if i == 0:
                subplot.set_ylabel(str(row).replace(' ', '\n'), fontsize=8)
            subplot.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
            i += 1
        i = 0
        j += 1

    plt.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.tight_layout()
    plt.show()
