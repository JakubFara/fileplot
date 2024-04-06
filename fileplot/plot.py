from matplotlib import pyplot as plt
import matplotlib
import re
print(matplotlib.matplotlib_fname())
# import scienceplots
import numpy as np
from matplotlib.ticker import AutoMinorLocator, FixedLocator


SPLITTING = r"  |,|\*| |\n"
DEFAULT_FIG_PARAM = {
    "top": 0.95,
    "bottom": 0.8,
    "left": 0.035,
    "right": 0.99,
    "hspace": 0.25,
    "wspace": 0.15,
    "fig_size": (15, 8),
    "dpi": 200,
}
DEFAULT_TITLE = {"name": "My Title", "fontsize": 20, "y": 1.0}

# plt.rcParams["font.family"] = ""
plt.rcParams.update({
    # "text.usetex": False,
    "font.family": "sans-serif",
    # "font.sans-serif": "Helvetica",
    # 'text.latex.preamble': r'\usepackage{amsfonts}'
})
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["text.usetex"] = True
# plt.rcParams['font.family'] = 'Noto Sans Gurmukhia'
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsfonts}'
plt.rcParams["font.sans-serif"] = "Helvetica"
# plt.rcParams["font.family"] = "monospace"
# plt.rcParams["font.family"] = "Helvetica"
# matplotlib.rcParams['mathtext.fontset'] ='custom'
# matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
# matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
# matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
# matplotlib.rcParams["legend.framealpha"] = 0.8
# matplotlib.rcParams["legend.shadow"] = False


def load_array_from_file(filename: str, split_by=SPLITTING):
    if isinstance(filename, dict):
        return filename
    arrays = {}
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        column_names = [x.strip() for x in re.split(split_by, lines[0]) if x != ""]
        for column_name in column_names:
            arrays.update({column_name: []})
        for line in lines[1:]:
            for val, name in zip(re.split(split_by, line), column_names):
                if val != "":
                    arrays[name].append(float(val))
    return arrays


class Plot(object):
    def __init__(self):
        # self.fig = None
        self.fig = plt.figure()
        self.style = ["science", "ieee"]

    def plot(
        self, title, subplots: list, legend=None, legend_loc="lower center", ncol=4
    ):
        if not isinstance(subplots[0], list) and not isinstance(subplots[0], tuple):
            subplots = [subplots]
        shape = [len(subplots), max([len(s) for s in subplots])]
        axs = self.fig.add_gridspec(shape[0], shape[1])
        if title:
            if isinstance(title, str):
                title = {"name": title}
            for def_key, def_val in DEFAULT_TITLE.items():
                if not title.get(def_key):
                    title[def_key] = def_val
            # with plt.style.context(self.style):
            self.fig.suptitle(title["name"], fontsize=title["fontsize"], y=title["y"])
        for posy in range(shape[0]):
            for posx in range(shape[1]):
                if posx >= len(subplots[posy]):
                    continue
                subplot = subplots[posy][posx]
                # with plt.style.context(subplot.style) as style:
                ax = self.fig.add_subplot(axs[posy, posx])
                subplot.plot(ax)
        if legend:
            # with plt.style.context(subplot.style):
            self.fig.legend(legend, loc=legend_loc, fontsize=8, ncol=ncol, shadow=False)

    def save_fig(self, figname, fig_param: dict):
        for def_key, def_val in DEFAULT_FIG_PARAM.items():
            if not fig_param.get(def_key):
                fig_param[def_key] = def_val

        self.fig.subplots_adjust(
            hspace=fig_param["hspace"],
            wspace=fig_param["wspace"],
            top=fig_param["top"],
            left=fig_param["left"],
            right=fig_param["right"],
            bottom=fig_param["bottom"],
        )
        # print(fig_param["fig_size"][0], fig_param["fig_size"][1])
        self.fig.set_size_inches(fig_param["fig_size"][0], fig_param["fig_size"][1])
        self.fig.savefig(figname, dpi=fig_param["dpi"])

    def show(self):
        plt.show()


class SubPlot(object):
    def __init__(
        self,
        filenames: list,
        names: list,
        xtitle: str = None,
        ytitle: str = None,
        split_by=SPLITTING,
        labels=None,
        style=None,
        legend_title=None,
        title=None,
        xlim=None,
        ylim=None,
        colors=None,
        line_types=None,
        grid=True,
        show_legend=True,
        line_wide=1,
        project_on_axes=None,
        x_ticks=None,
        y_ticks=None,
        x_grid_array=None,
        y_grid_array=None,
        yscale=None,
        xscale=None,
    ):
        self.labels = labels
        self.filenames = filenames
        self.names = names
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.colors = colors
        self.line_types = line_types
        self.split_by = split_by
        self.xlim = xlim
        self.ylim = ylim
        self.title = title
        self.legend_title = legend_title
        self.grid = grid
        self.show_legend = show_legend
        self.line_wide = line_wide
        self.project_on_axes = project_on_axes
        self.x_ticks = x_ticks
        self.y_ticks = y_ticks
        self.x_grid_array = x_grid_array
        self.y_grid_array = y_grid_array
        self.yscale=yscale
        self.xscale=xscale
        if not style:
            self.style = ["science", "ieee"]
        else:
            self.style = style

    def plot(self, ax):
        if not self.labels:
            self.labels = self.names

        # with plt.style.context(self.style):
        plt.title(
            self.title,
            # font="sans-serif",
            # fontweight="bold",
            fontsize=8,
            y=1.04,
            # pad=10,
            # **{'fontname': 'Helvetica'} #, 'size':'18', 'color':'black', 'weight':'bold',
               # 'verticalalignment':'bottom'}
        )
        # with plt.style.context(self.style):
        ax.autoscale(tight=True)
        # ax.set(**pparam)
        if self.xtitle:
            ax.set_xlabel(self.xtitle, fontsize=8)
        if self.ytitle:
            ax.set_ylabel(self.ytitle, fontsize=8)
        if self.title:
            print(self.title)

            # plt.rcParams.update({
            #     "text.usetex": True,
            #     "font.family": "sans-serif",
            #     "font.sans-serif": "Helvetica",
            #     'text.latex.preamble': r'\usepackage{amsfonts}'
            # })
            # ax.set_title(
            #     self.title,
            #     font="sans-serif",
            #     # fontweight="bold",
            #     fontsize=8,
            #     # pad=10,
            # )
        if self.colors is None:
            self.colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        if self.line_types is None:
            self.line_types = "-" * len(self.filenames)
        y_max = -1e16
        y_min = 1e16
        for filename, (xname, yname), label, color, line_type in zip(
                self.filenames, self.names, self.labels, self.colors, self.line_types
        ):
            arrays = None

            if filename is not None:
                arrays = load_array_from_file(filename, split_by=self.split_by)

            if isinstance(xname, str):
                array_x = arrays[xname]
            elif isinstance(xname, np.ndarray):
                array_x = xname
            else:
                array_x = xname(arrays)
            # print(arrays)
            if self.xlim is not None:
                indices = [i for i, x in enumerate(array_x) if self.xlim[0] < x < self.xlim[1]]
            else:
                indices = [i for i, x in enumerate(array_x)]
            array_x = [array_x[i] for i in indices]


            if isinstance(yname, str):
                if arrays.get(yname):
                    array_y = [arrays[yname][i] for i in indices]
                else:
                    array_y = [0 for i in indices]
            elif isinstance(yname, np.ndarray):
                array_y = yname[indices]
            else:
                array_y = yname(arrays)[indices]
            ax.plot(
                array_x,
                array_y,
                line_type,
                color=color,
                linewidth=self.line_wide,
                label=label,
            )
            y_max_ = max(array_y)
            y_min_ = min(array_y)
            if y_max_ > y_max:
                y_max = y_max_
            if y_min_ < y_min:
                y_min = y_min_
        if self.ylim is None:
            delta = (abs(y_min) + abs(y_max)) * 0.01
            self.ylim = [y_min - delta, y_max + delta]
        # with plt.style.context(self.style):
        ax.yaxis.offsetText.set_fontsize(6)
        ax.ticklabel_format(
            axis="y", style="sci", scilimits=(-1, 2), useOffset=True,
        )
        ax.ticklabel_format(axis="x", style="plain", scilimits=(0, 0), useOffset=True)
        # ax.ticklabel_format(
        #     axis="x", scilimits=(-1, 2), useOffset=True,
        # )
        ax.tick_params(axis='x', labelsize=6)
        ax.tick_params(axis='y', labelsize=6)
        if self.xlim:
            ax.set_xlim(self.xlim[0], self.xlim[1])
            # if self.ylim is None:
            #     self.ylim = []
        if self.xscale is not None:
            ax.set_xscale(self.xscale)
        if self.yscale is not None:
            ax.set_yscale(self.yscale)
        if self.ylim:
            ax.set_ylim(self.ylim[0], self.ylim[1])
        if self.grid:
            ax.grid(linestyle="--")
        if self.show_legend:
            ax.legend(title=self.legend_title, fontsize=8)
        if self.x_grid_array is not None:
            ax.xaxis.set_major_locator(FixedLocator(self.x_grid_array[0]))
            for i, tick in enumerate(ax.xaxis.get_major_ticks()):
                if not self.x_grid_array[1][i]:
                    tick.label1.set_visible(False)
        if self.y_grid_array is not None:
            ax.yaxis.set_major_locator(FixedLocator(self.y_grid_array[0]))
            for i, tick in enumerate(ax.yaxis.get_major_ticks()):
                if not self.y_grid_array[1][i]:
                    tick.label1.set_visible(False)
        if self.x_ticks is not None:
            ax.set_xticks(self.x_ticks)
        if self.y_ticks is not None:
            ax.set_yticks(self.y_ticks)
        if self.project_on_axes:
            x = self.project_on_axes.get("x")
            on_x = self.project_on_axes.get("on_x")
            on_y = self.project_on_axes.get("on_y")
            if x is not None:
                filenames = self.project_on_axes.get("filenames")
                names = self.project_on_axes.get("names")
                if not isinstance(x, list):
                    x = [x]
                if not isinstance(filenames, list) and filenames is not None:
                    filenames = [filenames] * len(x)
                if not isinstance(names, list):
                    names = [names] * len(x)
                linewidth = self.project_on_axes.get("linewidth")
                if linewidth is None:
                    linewidth = 1.0
                color = self.project_on_axes.get("color")
                if color is None:
                    color = "black"

                if names is not None and filenames is not None:
                    for (xname, yname), file_, x_ in zip(names, filenames, x):
                        arrays = load_array_from_file(
                            file_, split_by=self.split_by
                        )

                        if isinstance(yname, str):
                            array = arrays[yname]
                        else:
                            array = yname(
                                arrays
                            )
                        x_ind = np.abs(np.array(arrays[xname]) - x_).argmin()
                        closest_x = arrays[xname][x_ind]
                        # print(closest_x, x_ind, array[x_ind], file_)
                        if on_x:
                            plt.plot(
                                [closest_x, closest_x],
                                [0, array[x_ind]],
                                color=color,
                                linewidth=linewidth,
                                linestyle="--",
                            )
                        if on_y:
                            plt.plot(
                                [0, closest_x],
                                [array[x_ind], array[x_ind]],
                                color=color,
                                linewidth=linewidth,
                                linestyle="--",
                            )
                        if self.project_on_axes["show_labels"]:
                            if on_x:
                                ax.set_xticks(list(ax.get_xticks()) + [closest_x])
                            if on_y:
                                ax.set_yticks(
                                    list(ax.get_yticks()) + [array[x_ind]]
                                )

                elif names is not None:
                    for xname, x_ in zip(names, x):
                        arrays = load_array_from_file(
                            file_, split_by=self.split_by
                        )
                        if self.project_on_axes["show_labels"]:
                            ax.set_xticks(list(ax.get_xticks()) + [x_])
