# GNSS_measurement_analysis
This is a project done as a part of an IoT course, which analyses data collected from
Google’s GNSSLogger Android App in various environments (indoor, outdoor, partial sky, etc)

Various parameters; like Distance Errors, Average SNR, No. of Satellites, Average Elevation, Average Azimuth,
are then checked against each other for any correlation.

<img src='https://user-images.githubusercontent.com/64144419/126344348-a808b061-0bf8-48e4-b31d-e5da4af0a227.png' width=240> <img src='https://user-images.githubusercontent.com/64144419/126344490-97d14fc4-029a-425a-8d18-89f372aedd87.png' width=300>

<img src='https://user-images.githubusercontent.com/64144419/126344816-98f5dac0-df0b-42c1-a31d-50bdef0d089b.png' width=340> <img src='https://user-images.githubusercontent.com/64144419/126344925-6fd9228b-40b8-48d1-9269-835874c6143e.png' width=450>

<img src='https://user-images.githubusercontent.com/64144419/126344880-86d332b1-065d-405c-9fed-39adb380f14f.png' width=200>

More details on the process and observations can be found [here](./GNSS_Measurement_Analysis__ED18B027_Report.pdf)

Below is a short description of what each file does.
## parse.py

Parses logfiles in raw_logs and temporarily puts them in `./tmp`
These are then deleted by the main program. This is NOT to be run to
is used by the other 2 programs.

## distribution_per_fix.py

How to run: `python3 distribution_per_fix.py` in terminal

Terminal Output for each logfile:

	parsing <logfile>.txt
	Mean Latitude: 17.50333544537816
	Mean Longitude: 78.33146113058821
	Median # of Satellites: 5.0
  
Then:
1. Shows CDF & PDF of dist_errors
1. Shows Scatter-Plot: Corellation b/w dist_errors and satellites_used
1. Shows Scatter-Plot: Corellation b/w dist_errors and avg_SNR_per_fix

## distribution_per_satellite.py

How to run: `python3 distribution_per_satellite.py` in terminal

Terminal Output for each logfile:

```
parsing gnss_log_2_partial_sky.txt
svid  | avg_snr           | avg_azimuth      | avg_elevation
a     | xx.xxxxxxxxxxxxxx | xx.xxxxxxxxxxxxx | xx.xxxxx
b     | xx.xxxxxxxxxxxxxx | xxx.xxxxxxxxxxxx | xx.xxxxx
```

Then:
1. Shows Avg_Elevation vs Average_SNR Plot
2. Shows Avg_Azimuth vs Average_SNR Plot
