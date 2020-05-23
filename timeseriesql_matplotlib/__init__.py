import matplotlib.pyplot as plt
from matplotlib.dates import (
    DayLocator,
    HourLocator,
    MonthLocator,
    YearLocator,
    MinuteLocator,
    DateFormatter,
)
import numpy as np
import math
from timeseriesql.plot import Plot

DEFAULT_FIGURE_SIZE = (20, 10)

FIGURE_COUNTER = 1

def init_ax_if_none(func):
    def inner(*args, **kwargs):
        if 'ax' not in kwargs or kwargs['ax'] == None:
            global FIGURE_COUNTER
            fig = plt.figure(FIGURE_COUNTER, figsize=DEFAULT_FIGURE_SIZE)
            fig.autofmt_xdate()
            ax = fig.add_subplot(111)
            print(id(ax))
            kwargs['ax'] = ax
            FIGURE_COUNTER += 1
        return func(*args, **kwargs)
    
    return inner

def auto_plot(ts):
    diff = ts.time[-1] - ts.time[0]
    if diff > 31536000:
        return "y"
    elif diff > 2678400:
        return "mth"
    elif diff > 604800:
        return "dow"
    elif diff > 86400:
        return "h"
    elif diff > 3600:
        return "m"
    return "s"

timebox_funcs = {
    "s": ["second", 60, None],
    "m": ["minute", 60, None],
    "h": ["hour", 24, None],
    "dow": ["weekday", 7, ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]],
    "d": ["day", 31, None],
    "mth": [
        "month",
        12,
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    ],
}
 
class MatplotlibTQL(Plot):

    def _create_xaxis_date(self, ax, date_index):
        """  Uses buest guess for x axis labels """
        window = (date_index[-1] - date_index[0]).astype(int)

        interval=5

        xlabel = ""
        if window <= 3600:
            minor_locator = MinuteLocator(interval=interval)
            minor_formatter = DateFormatter("%M")
            major_locator = HourLocator()
            major_formatter = DateFormatter("\n%Y-%m-%d %H:%M")
            xlabel = "Minute"
        elif window <= 86400:
            minor_locator = HourLocator(interval=interval)
            minor_formatter = DateFormatter("%H:%M")
            major_locator = DayLocator()
            major_formatter = DateFormatter("\n%Y-%m-%d")
            xlabel = "Hour"
        elif window <= (7 * 86400):
            minor_locator = HourLocator(interval=6)
            minor_formatter = DateFormatter("%H:%M")
            major_locator = DayLocator()
            major_formatter = DateFormatter("\n%Y-%m-%d")
            xlabel = "Hour"
        elif window <= (60 * 86400):
            #if len(date_index) > 30:
            #    interval = 2
            minor_locator = DayLocator(interval=interval)
            minor_formatter = DateFormatter("%m-%d")
            major_locator = YearLocator()
            major_formatter = DateFormatter("\n%Y")
            xlabel = "Day"
        else:
            minor_locator = MonthLocator(interval=interval)
            minor_formatter = DateFormatter("%B")
            major_locator = YearLocator()
            major_formatter = DateFormatter("\n%Y")
            xlabel = "Month"

        ax.xaxis.set_minor_locator(minor_locator)
        ax.xaxis.set_minor_formatter(minor_formatter)
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
        ax.fmt_xdata = DateFormatter("%Y-%m-%d %H:%M:%S")
        
        ax.set_xlabel(xlabel)


    def subplot(self, func, ts, **kwargs):
        """ 
        Plot each column in it's own chart

        func: function
            The plotting function
        ts:  TimeSeries
            the time series
        kwargs: arguement list
            this will be pass to the plotting function

        Example
        -------
        subplot(dist_plot,ts, percentiles=[50, 99])
        >>>
        """



        size = ts.shape[1]
        fig, ax = plt.subplots(
            size, 1, figsize=DEFAULT_FIGURE_SIZE, sharex="col", sharey="row"
        )
        for i, col in enumerate(ax):
            func(ts[:, i], ax=col, **kwargs)


    @init_ax_if_none
    def line_plot(self, ts, ax=None, legend=True, labels=None, ylabel=None, **kwargs):
        """Plot charts using sane time series defaults with Matplotlib.

        Parameters
        ----------
        ts:  TimeSeries
            time series to plot
        ax : matplotlib.axes.Axes
            an Axes to plot against.  One will be created if not included
        legend: Boolean
            Decision to generate a legend
        labels: list
            A list of labels to use instead of generated labels
        ylabel: string
            yaxis_label

        Returns
        -------
        None

        Example
        -------
        line_plot(ts)
        >>>
        """
        ylabel = self.ylabel_func(ts) if ylabel is None else ylabel

        date_index = ts.time.dt
        self._create_xaxis_date(ax, date_index)
        ax.set_title(self.title_func(ts), fontsize=18)

        ax.plot(date_index, ts.data, **kwargs)
        ax.set_ylabel(ylabel)
        if legend:
            if not labels:
                labels = self.legend_labels_func(ts)
            if labels != [""]:
                ax.legend(title="Streams", labels=labels[:5])


    @init_ax_if_none
    def dist_plot(self, ts, ax=None, percentiles=None, xlabel=None, **kwargs):
        """ 
        Create a distribution plot

        Parameters
        ----------
        ts:  TimeSeries
            time series to plot
        ax : matplotlib.axes.Axes
            an Axes to plot against.  One will be created if not included
        percentiles: list
            an array of percentiles to plot
        xlabel: string
            xaxis_label

        Returns
        -------
        None

        Example
        -------
        dist_plot(ts, percentiles=[50, 99])
        >>>
        """
        xlabel = self.xlabel_func(ts) if xlabel is None else xlabel
        hist = ax.hist(ts.data.flatten(), bins="auto", rwidth=0.99)
        ax.set_title("Distribution for " + self.title_func(ts), fontsize=18)
        ax.set_ylabel("Count")
        ax.set_xlabel(xlabel)
        if percentiles:
            m = max(hist[0])
            for p in percentiles:
                value = np.percentile(ts.data.flatten(), p)
                ax.axvline(value, color="r", linestyle="--", ymax=0.95)
                ax.text(x=value, y=m, s=f"p{p}")


    @init_ax_if_none
    def stacked_plot(self, ts, ax=None, ylabel=None, **kwargs):
        """Plot stacked charts using sane time series defaults with Matplotlib.

        Parameters
        ----------
        ts:  TimeSeries
            time series to plot
        ax : matplotlib.axes.Axes
            an Axes to plot against.  One will be created if not included
        ylabel: string
            yaxis_label

        Returns
        -------
        None

        Example
        -------
        stacked_plot(ts)
        >>>
        """
        ylabel = self.ylabel_func(ts) if ylabel is None else ylabel
        date_index = ts.time.dt
        self._create_xaxis_date(ax, date_index)
        labels = self.legend_labels_func(ts)
        ax.set_title(self.title_func(ts), fontsize=18)
        ax.stackplot(date_index, ts.data.T, labels=labels[:5])
        ax.set_ylabel(ylabel)
        ax.legend(title="Streams", labels=labels[:5])


    @init_ax_if_none
    def timebox_plot(self, ts, ax=None, plot="auto", ylabel=None, **kwargs):
        """
        A time boxplot for time series EDA.

        plot: string
            options
            -------
            auto - find the best possible time range
            s    - second buckets
            m    - minute buckets
            h    - hour buckets
            d    - day buckets
            mth  - month buckets
            y    - year buckets
        ax:  axes 
            to use for plotting.  One is generated if not passed
        ylabel: string
            yaxis_label
        kwargs: kwargs
            pass to the axes as options
        """

        ylabel = self.ylabel_func(ts) if ylabel is None else ylabel

        if plot == "auto":
            plot = auto_plot(ts)


        func, max_size, labels = timebox_funcs[plot]
        dates = ts.time.dt
        if plot == "dow":  # <-----:puke:
            dates = np.array([getattr(x.tolist(), func)() for x in dates])
        else:
            dates = np.array([getattr(x.tolist(), func) for x in dates])

        max_count = 0
        for i in range(max_size):
            l = len(np.argwhere(dates == i))
            if l > max_count:
                max_count = l
        data = np.empty((max_count, max_size))
        data[:] = np.nan
        for i in range(max_size):
            row_slice = slice(None, None, None)
            temp = ts.data[np.argwhere(dates == i)[:, 0]][:, 0]
            if temp.shape != data[:, i].shape:
                row_slice = slice(None, temp.shape[0], None)
            data[row_slice, i] = temp

        # drop nan
        new_data = []
        for col in data.T:
            new_data.append(col[~np.isnan(col)])
        ax.boxplot(new_data, **kwargs)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(func[0].upper() + func[1:])
        ax.set_title(self.title_func(ts), fontsize=18)
        if labels:
            ax.set_xticklabels(labels)


    @init_ax_if_none
    def correlogram_plot(self, ts, ax=None, **kwargs):
        """Plot stacked charts using sane time series defaults with Matplotlib.

        Parameters
        ----------
        ts:  TimeSeries
            time series to plot
        ax : matplotlib.axes.Axes
            an Axes to plot against.  One will be created if not included

        Returns
        -------
        None

        Example
        -------
        correlogram_plot(ts)
        >>>
        """
        ax.acorr(ts.data.flatten(), usevlines=True, normed=True, lw=2, **kwargs)
        ax.set_ylabel("Correlation")
        ax.set_xlabel("Lag")


    def lag_plot(self, ts, lags=12, max_per_row=3, **kwargs):
        """Plot lag plots

        Parameters
        ----------
        ts: TimeSeries
            time series to plot
        lags: int or iterable
            the lags to plot.  If an iterable, a custom lag configuration with be used
        ax : matplotlib.axes.Axes
            an Axes to plot against.  One will be created if not included
        max_per_row : int
            the maximum charts in a row

        Returns
        -------
        None

        Example
        -------
        lag_plot(ts)
        >>>
        """
        if isinstance(lags, int):
            obj = range(1, lags+1)
        else:
            obj = lags
        try:
            iter(obj)
        except TypeError:
            raise TypeError("Expecting lags to be either an int or an iterable")
        
        s = {}
        l = len(ts)
        for i in obj:
            if isinstance(i, int):
                original_slice = slice(0, -(i))
                lag_slice = slice(i, l)
                s[i] = [original_slice, lag_slice]

        size = len(s)
        fig, ax = plt.subplots(
            math.ceil(size / max_per_row), max_per_row, figsize=DEFAULT_FIGURE_SIZE, sharex="col", sharey="row"
        )
        for index, (key, (original,compare)) in enumerate(s.items()):
            if max_per_row == 1:
                ax[index].scatter(ts.data[original],ts.data[compare])
                ax[index].set_title(f"lag -{key}")
            else:
                ax[index // max_per_row][index % max_per_row].scatter(ts.data[original],ts.data[compare])
                ax[index // max_per_row][index % max_per_row].set_title(f"lag -{key}")
        
        return None


    @init_ax_if_none
    def heatmap_plot(self, ts, ax=None, plot="auto", cmap="Blues", title="", ylabel=None, **kwargs):
        """
        A heatmap for time series EDA.

        plot: string
            options
            -------
            auto - find the best possible time range
            s    - second buckets
            m    - minute buckets
            h    - hour buckets
            d    - day buckets
            mth  - month buckets
            y    - year buckets
        ax:  axes 
            to use for plotting.  One is generated if not passed
        cmap : string
            the value to use for the coloring.  see https://matplotlib.org/tutorials/colors/colormaps.html
        ylabel: string
            yaxis_label
        kwargs: kwargs
            pass to the axes as options
        """
        
        ylabel = self.ylabel_func(ts) if ylabel is None else ylabel

        if plot == "auto":
            plot = auto_plot(ts)

        func, max_size, labels = timebox_funcs[plot]
        hist, bins = np.histogram(ts)
        
        new_ts = np.zeros((len(bins)-1, max_size))
        dates = ts.time.dt
        if plot == "dow":  # <-----:puke:
            dates = np.array([getattr(x.tolist(), func)() for x in dates])
        else:
            dates = np.array([getattr(x.tolist(), func) for x in dates])
        for i in range(max_size):    
            new_ts[:,i] = np.histogram(ts[np.argwhere(dates==i)], bins)[0]
            

        im = ax.imshow(new_ts, cmap=cmap, interpolation='nearest')
        plt.colorbar(im, ax=ax)
        test = ax.get_xticklabels()
        ax.set_ylabel(ylabel)
        ax.set_xlabel(func[0].upper() + func[1:])
        ax.set_title(self.title_func(ts), fontsize=18)
        if labels:
            labels = [labels[int(x)] for x in ax.get_xticks() if x < len(labels)]
            ax.set_xticklabels(labels)
        ax.set_yticklabels([math.ceil(x) for x in bins])
        return None
    
    @init_ax_if_none
    def text_plot(self, value, ax=None, title="", fontsize=48, thresholds=None, **kwargs):
        """ 
        Plot a single value

        Parameters
        ----------
        value:  number
            a value to display
        ax : matplotlib.axes.Axes
            an Axes to plot against.  One will be created if not included
        title: string
            title for box
        fontsize: int
            size for the text
        thresholds: list(tuple)
            tuples that colorize the text and background color based on the value of the numer
            The format is (threshold, background color, font color).  Based on the color palette at:
            https://matplotlib.org/3.1.0/gallery/color/named_colors.html
            If threshold is None, then the condition is considered met.  The default background color
            is 'white' and the font color is 'black'

        Returns
        -------
        None

        Example
        -------
        text_plot(value, title="A Nice Text Box", thresholds=[(0, 'green', 'white'), (20, 'cornflowerblue', 'white'), (None, 'darkorange', 'white')])
        >>>

        """
        fontcolor = 'black'
        facecolor = 'white'

        if thresholds:
            for t in thresholds:
                if t[0] is not None:
                    if value < t[0]:
                        if t[1]:
                            facecolor = t[1]
                        if t[2]:
                            fontcolor = t[2]
                        break
                else:
                    if t[1]:
                        facecolor = t[1]
                    if t[2]:
                        fontcolor = t[2]
                    break
        ax.text(0.5, 0.5, "%.2f" % (value), va="center", ha="center", fontsize=fontsize, color=fontcolor)
        ax.set_title(title)
        ax.set_facecolor(facecolor)
        ax.tick_params(labelbottom=False, labelleft=False)
        ax.grid(False)
