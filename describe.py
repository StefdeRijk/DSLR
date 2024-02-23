import argparse
import pandas as pd
from math import sqrt, pow
pd.options.mode.chained_assignment = None


def get_count(data):
    counts = []
    for column in data.columns:
        count = 0
        for value in data[column]:
            if not pd.isnull(value):
                count += 1
        counts.append(count)
    return counts


def get_mean(data):
    means = []
    for column in data.columns:
        sum = 0
        length = 0
        for value in data[column]:
            if not pd.isnull(value):
                sum += value
                length += 1
        mean = sum / length
        means.append(mean)
    return means


def get_std(data, means):
    stds = []
    for index, column in enumerate(data.columns):
        mean = means.iloc[index]
        sum_squares = 0
        length = 0
        for value in data[column]:
            if not pd.isnull(value):
                variance = value - mean
                sum_squares += pow(variance, 2)
                length += 1
        variance = sum_squares / (length - 1)
        std = sqrt(variance)
        stds.append(std)
    return stds


def get_min(data):
    min_values = []
    for column in data.columns:
        min_value = float('inf')
        for value in data[column]:
            if not pd.isnull(value):
                if value < min_value:
                    min_value = value
        min_values.append(min_value)
    return min_values


def get_max(data):
    max_values = []
    for column in data.columns:
        max_value = float('-inf')
        for value in data[column]:
            if not pd.isnull(value):
                if value > max_value:
                    max_value = value
        max_values.append(max_value)
    return max_values


def get_percentile(data, percentile):
    percentiles = []
    data_copy = data.copy()
    for column in data.columns:
        length = 0
        sorted_column = data_copy.sort_values(by=column)
        for value in data[column]:
            if not pd.isnull(value):
                length += 1

        if length % 2 == 0:
            location_lower = int((length - 1) / (100 / percentile))
            location_higher = location_lower + 1

            value_lower = sorted_column[column].iloc[location_lower]
            value_higher = sorted_column[column].iloc[location_higher]

            fraction = ((percentile / 100) * (length - 1) - location_lower)

            percentiles.append(value_lower + (value_higher - value_lower) * fraction)
        else:
            location = int((length - 1) / (100 / percentile))
            percentiles.append(sorted_column[column].iloc[location])
    return percentiles


def describe_data(data_file):
    data = pd.read_csv(data_file)
    data = data.select_dtypes(['number'])
    data.drop(columns=['Index'], inplace=True)
    described_data = data[0:0]
    described_data.loc['count'] = get_count(data)
    described_data.loc['mean'] = get_mean(data)
    described_data.loc['std'] = get_std(data, described_data.loc['mean'])
    described_data.loc['min'] = get_min(data)
    described_data.loc['25%'] = get_percentile(data, 25)
    described_data.loc['50%'] = get_percentile(data, 50)
    described_data.loc['75%'] = get_percentile(data, 75)
    described_data.loc['max'] = get_max(data)
    with pd.option_context('display.width', None,
                           'display.max_columns', None,
                           'display.precision', 6,
                           ):
        print(described_data)
        # print(data.describe())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Settings for describing the data')
    parser.add_argument('--data_file', type=str, required=True,
                        help='Path to the csv file that contains the data')
    args = parser.parse_args()

    describe_data(args.data_file)
