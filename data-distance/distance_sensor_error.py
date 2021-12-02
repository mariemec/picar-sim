import numpy as np
import matplotlib.pyplot as plt


def analyze_raw_data(show=False):
    print(f'distance\t\tmoyenne\t\técart-type\t\t% erreur\t\tremoved data')
    distances = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80])
    means = np.array([])
    std_devs = np.array([])
    percent_errors = np.array([])

    for dist in distances:
        filename = f'{dist}cm_expected_with_1000_values.txt'
        myfile = open(filename, "r")
        myline = myfile.readline()

        data = np.array([])
        removed_data = np.array([])
        while myline:
            line_data = myline.split(';')
            measured_distance = float(line_data[1].strip())

            # remove noise
            if dist+10 > measured_distance > dist-10:
                data = np.append(data, measured_distance)
            else:
                removed_data = np.append(removed_data, measured_distance)
            myline = myfile.readline()
        myfile.close()

        # Stats
        mean = np.mean(data)
        std_dev = np.std(data)
        percent_error = abs((mean-dist))/dist * 100

        means = np.append(means, mean)
        std_devs = np.append(std_devs, std_dev)
        percent_errors = np.append(percent_errors, percent_error)
        print(f'{dist}\t\t\t{mean:.2f}\t\t\t{std_dev:.2f}\t\t\t{percent_error}\t\t\t{len(data)}/{len(removed_data)}')

        if show:
            plt.hist(data, bins='auto')
            plt.title(f'Histogramme Capteur de distance = {dist} cm')
            plt.xlabel('Distance mesurée (cm)')
            plt.ylabel('Fréquence absolue')
            plt.show()
    return distances, means, std_devs, percent_errors


if __name__ == '__main__':
    distances, means, std_devs, percent_errors = analyze_raw_data(show=True)
    N = 10000
    for dist, mean, std_dev, percent_error in zip(distances, means, std_devs, percent_errors):
        u1 = np.random.uniform(0, 1, N)
        np.random.seed()
        u2 = np.random.uniform(0, 1, N)
        normal_distribution = mean+std_dev*np.sin(2*np.pi*u1)+np.sqrt(-2*np.log(u2))
        plt.hist(normal_distribution, label=f'{dist}')

    plt.legend()
    plt.show()