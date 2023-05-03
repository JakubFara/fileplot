from matplotlib import pyplot as plt
import matplotlib
import re
import scienceplots


SPLITTING = r'  |,|\*| |\n'
DEFAULT_FIG_PARAM = {
    'top': 0.95,
    'bottom': 0.12,
    'left': 0.035,
    'right': 0.99,
    'hspace': 0.25,
    'fig_size': (15, 8),
    'dpi': 200
}
DEFAULT_TITLE = {
    'name': 'My Title',
    'fontsize': 20,
    'y': 1.0
}


def load_array_from_file(filename: str, split_by=SPLITTING):
    arrays = {}
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        column_names = [
            x.strip() for x in re.split(split_by, lines[0]) if x != ''
        ]
        for column_name in column_names:
            arrays.update({column_name: []})
        for line in lines[1:]:
            for val, name in zip(re.split(split_by, line), column_names):
                if val != '':
                    arrays[name].append(float(val))
    return arrays


class Plot(object):
    def __init__(self):
        # self.fig = None
        self.fig = plt.figure()

    def plot(self, title, subplots: list, legend=None,
             legend_loc='lower center', ncol=4):
        if (not isinstance(subplots[0], list) and not
                isinstance(subplots[0], tuple)):
            subplots = [subplots]
        shape = [len(subplots), max([len(s) for s in subplots])]
        axs = self.fig.add_gridspec(shape[0], shape[1])
        if title:
            if isinstance(title, str):
                title = {'name': title}
            for def_key, def_val in DEFAULT_TITLE.items():
                if not title.get(def_key):
                    title[def_key] = def_val
            self.fig.suptitle(
                title['name'], fontsize=title['fontsize'], y=title['y']
            )
        for posy in range(shape[0]):
            for posx in range(shape[1]):
                if posx >= len(subplots[posy]):
                    continue
                subplot = subplots[posy][posx]
                with plt.style.context(subplot.style):
                    matplotlib.rcParams.update({
                        'text.usetex': False,
                        'font.family': 'stixgeneral',
                        'mathtext.fontset': 'stix',
                    }
                    )
                    ax = self.fig.add_subplot(axs[posy, posx])
                    subplot.plot(ax)
        if legend:
            self.fig.legend(legend, loc=legend_loc, ncol=ncol)

    def save_fig(self, figname, fig_param: dict):
        for def_key, def_val in DEFAULT_FIG_PARAM.items():
            if not fig_param.get(def_key):
                fig_param[def_key] = def_val

        self.fig.subplots_adjust(
            hspace=fig_param['hspace'],
            top=fig_param['top'],
            left=fig_param['left'],
            right=fig_param['right'],
            bottom=fig_param['bottom']
        )
        self.fig.set_size_inches(
            fig_param['fig_size'][0],
            fig_param['fig_size'][1]
        )
        self.fig.savefig(figname, dpi=fig_param['dpi'])

    def show(self):
        plt.show()


class SubPlot(object):
    def __init__(self, filenames: list, names: list, xtitle: str = None,
                 ytitle: str = None, split_by=SPLITTING, labels=None,
                 style=None, legend_title=None, title=None, xlim=None,
                 ylim=None, colors=None, grid=True, show_legend=True,
                 line_wide=1):
        self.labels = labels
        self.filenames = filenames
        self.names = names
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.colors = colors
        self.split_by = split_by
        self.xlim = xlim
        self.ylim = ylim
        self.title = title
        self.legend_title = legend_title
        self.grid = grid
        self.show_legend = show_legend
        self.line_wide = line_wide
        if not style:
            self.style = ['science', 'ieee']
        else:
            self.style = style

    def plot(self, ax):
        if not self.labels:
            self.labels = self.names

        with plt.style.context(self.style):
            ax.autoscale(tight=True)
            # ax.set(**pparam)
            if self.xtitle:
                ax.set_xlabel(self.xtitle)
            if self.ytitle:
                ax.set_ylabel(self.ytitle)
        if self.colors is None:
            self.colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        for filename, (xname, yname), label, color in zip(
            self.filenames, self.names, self.labels, self.colors
        ):
            arrays = load_array_from_file(filename, split_by=self.split_by)
            # print(arrays)
            if isinstance(yname, str):
                # print(arrays[xname], arrays[yname])
                with plt.style.context(self.style):
                    ax.plot(arrays[xname], arrays[yname],
                            color, linewidth=self.line_wide, label=label)
            else:
                with plt.style.context(self.style):
                    ax.plot(
                        arrays[xname], yname(arrays), color,
                        linewidth=self.line_wide, label=label
                    )

        with plt.style.context(self.style):
            ax.ticklabel_format(
                axis='y', style='sci', scilimits=(0, 0), useOffset=True
            )
            if self.xlim:
                ax.set_xlim(self.xlim[0], self.xlim[1])
            if self.ylim:
                ax.set_ylim(self.ylim[0], self.ylim[1])
            if self.title:
                ax.set_title(
                    self.title, fontweight="bold", fontsize=14, pad=10,
                )
            if self.grid:
                ax.grid(linestyle='--')
            if self.show_legend:
                ax.legend(title=self.legend_title)
