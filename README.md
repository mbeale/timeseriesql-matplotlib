<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">TimeSeriesQL-Matplotlib</h3>

  <p align="center">
    A plotting backend for the TimeSeriesQL library
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

This project adds a matplotlib plotting backend for the TimeSeriesQL project.

### Built With

* [TimeSeriesQL](https://github.com/mbeale/timeseriesql)
* [Matplotlib](https://matplotlib.org)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

The requirements are in the [requirements.txt](requirements.txt) file.

### Installation

#### pip

```sh
pip install timeseriesql-matplotlib
```

#### manual

1. Clone the timeseriesql-matplotlib
```sh
git clone https:://github.com/mbeale/timeseriesql-matplotlib.git
```
2. Install library
```sh
cd timeseriesql-matplotlib
python setup.py install 
```

<!-- USAGE EXAMPLES -->
## Usage

The charting library operates on TimeSeries objects.  The Axes can be overriden to control the placement of the charts.  All the below examples use the following code:

```python
import matplotlib.pyplot as plt

from timeseriesql_matplotlib import MatplotlibTQL as mp
from timeseriesql.backends.csv_backend import CSVBackend

data = CSVBackend(x for x in "AAPL.csv")[:] #CSV of AAPL stock data header = (open, close, high, low, adj close)
```


### Line Plot

```python
mp().line_plot(data)
plt.show()
```

![Line Plot Example](examples/line_plot.png?raw=true "Title")

### Stacked Plot

```python
mp().stacked_plot(data)
plt.show()
```

![Stacked Plot Example](examples/stacked_plot.png?raw=true "Title")

### Timebox Plot

```python
mp().line_plot(data)
timebox_plot(data[:,0])
"""
the plot arguement defaults to auto but you can set a specific period
s    - second buckets
m    - minute buckets
h    - hour buckets
d    - day buckets
mth  - month buckets
y    - year buckets
"""
```

![Timebox Plot Example](examples/timebox_plot.png?raw=true "Title")

### Distribution Plot

```python
mp().dist_plot(data[:,0], percentiles=[25,75]) #percentiles are optional
plt.show()
```

![Distribution Plot Example](examples/dist_plot.png?raw=true "Title")

### Correlogram Plot

```python
mp().correlogram_plot(data)
plt.show()
```

![Correlogram Plot Example](examples/correlogram_plot.png?raw=true "Title")

### Text Plot

```python
mp().line_plot(data)
mp().text_plot(data[-1,0], title="A Nice Text Box", thresholds=[(0, 'green', 'white'), (20, 'cornflowerblue', 'white'), (None, 'darkorange', 'white')])
```

![Text Plot Example](examples/text_plot.png?raw=true "Title")

### Layout Example

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(constrained_layout=True, figsize=(20,20))

gs = GridSpec(4, 4, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])
ax4 = fig.add_subplot(gs[0, 3])
ax5 = fig.add_subplot(gs[1:3, :3])
ax6 = fig.add_subplot(gs[1, 3])
ax7 = fig.add_subplot(gs[2, 3])
ax8 = fig.add_subplot(gs[3, :2])
ax9 = fig.add_subplot(gs[3, 2:])


mp().text_plot(data[:,0].mean(), ax=ax1, title="Avg Close")
mp().text_plot(data[:,1].mean(), ax=ax2, title="Avg High")
mp().text_plot(data[:,2].mean(), ax=ax3, title="Avg Low")
mp().line_plot(data[:,0], ax = ax4)
mp().line_plot(data, ax=ax5)
mp().line_plot(data[:,1], ax=ax6)
mp().line_plot(data[:,2], ax=ax7)
mp().line_plot(data[:,3], ax=ax8)
mp().line_plot(data[:,4], ax=ax9)
```

![Text Plot Example](examples/layout_plot.png?raw=true "Title")

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/mbeale/timeseriesql-matplotlib/issues) for a list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Michael Beale - michael.beale@gmail.com

Project Link: [https://github.com/mbeale/timeseriesql-matplotlib](https://github.com/mbeale/timeseriesql-matplotlib)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mbeale/timeseriesql-matplotlib.svg?style=flat-square
[contributors-url]: https://github.com/mbeale/timeseriesql-matplotlib/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mbeale/timeseriesql-matplotlib.svg?style=flat-square
[forks-url]: https://github.com/mbeale/timeseriesql-matplotlib/network/members
[stars-shield]: https://img.shields.io/github/stars/mbeale/timeseriesql-matplotlib.svg?style=flat-square
[stars-url]: https://github.com/mbeale/timeseriesql-matplotlib/stargazers
[issues-shield]: https://img.shields.io/github/issues/mbeale/timeseriesql-matplotlib.svg?style=flat-square
[issues-url]: https://github.com/mbeale/timeseriesql-matplotlib/issues
[license-shield]: https://img.shields.io/github/license/mbeale/timeseriesql-matplotlib.svg?style=flat-square
[license-url]: https://github.com/mbeale/timeseriesql-matplotlib/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/michael-beale-163a4670
