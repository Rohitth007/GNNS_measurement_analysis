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
            lat_vector = [0]
            long_vector = [0]
            satellites_used = [0]
            avg_SNR = [0]
            is_fix = False
            fix_time = -1

            for line in f:
                if line.startswith('Fix'):
                    # When there are 2 fixes one
                    # after the other (missing status)
                    if satellites_used[-1] == 0:
                        satellites_used.pop(-1)
                        lat_vector.pop(-1)
                        long_vector.pop(-1)
                        avg_SNR.pop(-1)
                    else:
                        avg_SNR[-1] /= satellites_used[-1]

                    l = list(map(float, line.split()[1:]))
                    lat_vector.append(l[0])
                    long_vector.append(l[1])
                    fix_time = l[-1]

                    satellites_used.append(0)
                    avg_SNR.append(0)
                    is_fix = True

                elif line.startswith('Status'):
                    l = list(map(float, line.split()[1:]))
                    # Handles case when there is a missing Fix
                    if satellites_used[-1] == 0:
                        first_index = l[0]
                    if (l[0] == first_index and satellites_used[-1] != 0) or fix_time != l[-1]:
                        is_fix = False

                    if is_fix:
                        avg_SNR[-1] += l[1]
                        satellites_used[-1] += 1

            # If the last Fix doesn't have Status
            if satellites_used[-1] == 0:
                satellites_used.pop(-1)
                lat_vector.pop(-1)
                long_vector.pop(-1)
                avg_SNR.pop(-1)
            else:
                avg_SNR[-1] /= satellites_used[-1]

        fix_count = len(lat_vector)
        mean_lat = sum(lat_vector) / fix_count
        mean_long = sum(long_vector) / fix_count
        groundtruth_lat = np.full(fix_count, mean_lat)
        groundtruth_long = np.full(fix_count, mean_long)

        dist_errors = haversine(
            long_vector, lat_vector,
            groundtruth_long, groundtruth_lat
        )

        print('Mean Latitude:', mean_lat)
        print('Mean Longitude:', mean_long)
        print('Median # of Satellites:', np.median(satellites_used))

        # Plot CDF and PDF of dist_errors
        error_counts, error_bins = np.histogram(dist_errors, bins=50)
        pdf = error_counts / fix_count  # Normalise
        cdf = np.cumsum(pdf)
        plt.plot(error_bins[1:], pdf, label=f"PDF{log.name}")
        plt.plot(error_bins[1:], cdf, label=f"CDF{log.name}")
        plt.legend()
        plt.show()

        # Scatter-Plot: Corellation b/w dist_errors and satellites_used
        e_min = min(dist_errors)
        e_max = max(dist_errors)
        plt.scatter(
            satellites_used, dist_errors,
            c=dist_errors, cmap='viridis',
            alpha=0.5
        )
        plt.ylim(e_min - (e_max-e_min)/10, e_max + (e_max-e_min)/10)
        plt.show()

        # Scatter-Plot: Corellation b/w dist_errors and avg_SNR_per_fix
        plt.scatter(
            avg_SNR, dist_errors,
            c=dist_errors, cmap='viridis',
            alpha=0.5, label=f"{log.name}"
        )
        # e_max & e_min already calculated
        plt.ylim(e_min - (e_max-e_min)/10, e_max + (e_max-e_min)/10)
        plt.legend()
        plt.show()


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    Source: https://stackoverflow.com/questions/29545704/fast-haversine-approximation-python-pandas
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km


if __name__ == '__main__':
    make_tmp()
    main()
    distroy_tmp()
