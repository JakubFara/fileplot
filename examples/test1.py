from fileplot import Plot, SubPlot


files = [
    'examples/data/test1/data1.txt',
    'examples/data/test1/data2.txt',
]

labels = [
    'data 1',
    'data 2',
]

fig_param = {
    'top': 0.9,
    'bottom': 0.1,
    'left': 0.1,
    'right': 0.99,
    'hspace': 0.25,
    'fig_size': (8, 8),
    'dpi': 200
}

# xlim = [0, 2.0]
# ylim = [0, 1.0]
xlim = None
ylim = None
plot1 = SubPlot(
    files,
    [('time', 'val1')] * len(files),
    xtitle=r'time $[s]$',
    ytitle=(r'$\chi$'),
    labels=labels,
    style=None,
    legend_title='method',
    title='x displacement',
    xlim=xlim,
    ylim=ylim,
    colors=None,
    grid=True,
    show_legend=False,
    line_wide=2,
)

plot2 = SubPlot(
    files,
    [('time', 'val2')] * len(files),
    xtitle=r'time $[s]$',
    ytitle=(r'$\mu$'),
    labels=labels,
    style=None,
    legend_title='method',
    title='x displacement',
    xlim=xlim,
    ylim=ylim,
    colors=None,
    grid=True,
    show_legend=False,
    line_wide=2,
)

title = None

plottool = Plot()

plottool.plot(
    title,
    [[plot1, plot2], [plot2, plot1]],
    legend=labels, ncol=6
)
plottool.save_fig('examples/results/test1.png', fig_param)
plottool.show()
