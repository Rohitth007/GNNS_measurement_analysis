import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

from parse import make_tmp, parse, distroy_tmp


def main():
    current_path = os.path.abspath(os.path.dirname(__file__))
    log_files = Path(current_path + '/raw_logs/').rglob('*.txt')

    for log in log_files:
        print(f'\nparsing {log.name}')
        parse(log.name)

        with open(f'tmp/{log.name}', mode='r', encoding='utf-8') as f:
            satellite_info = {}

            for line in f:
                if line.startswith('Status'):
                    l = list(map(float, line.split()[1:]))

                    if satellite_info.get(l[0]) is None:
                        satellite_info[l[0]] = [np.array([0, 0, 0, 0])]

                    satellite_info[l[0]] += np.array([l[1], l[2], l[3], 1])

        for svid, info in satellite_info.items():
            samples = info[0][3]
            satellite_info[svid] = info[0]/samples

        # Draw Table
        print('svid  | avg_snr           | avg_azimuth      | avg_elevation')
        for svid, info in satellite_info.items():
            print(f'{svid}  | {info[0]} | {info[1]} | {info[2]}')

        # Plot Avg_Elevation vs Average_SNR
        for svid, info in satellite_info.items():
            plt.scatter(info[2], info[0], label=svid)
        plt.legend()
        plt.show()

        # Plot Avg_Azimuth vs Average_SNR
        fig = plt.figure()
        ax = fig.add_subplot(projection='polar')
        for svid, info in satellite_info.items():
            ax.set_theta_zero_location("N", offset=35)
            ax.set_theta_direction(-1)
            ax.scatter(info[1], info[0], label=svid)
        plt.legend()
        plt.show()


if __name__ == '__main__':
    make_tmp()
    main()
    distroy_tmp()
