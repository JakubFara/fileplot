from fileplot import Plot, SubPlot


files = [
    "examples/data/test1/data1.txt",
    "examples/data/test1/data2.txt",
]

labels = [
    "data 1",
    "data 2",
]

fig_param = {
    "top": 0.9,  # start from x % from top of the page
    "bottom": 0.1,  # start from x % from bottom of the page
    "left": 0.1,  # start from x % from left of the page
    "right": 0.99,  # start from x % from top of the page
    "hspace": 0.25,  # spacing between subplots
    "fig_size": (8, 8),  # size of the figure in inches
    "dpi": 200,
}

# xlim = [0, 2.0]
# ylim = [0, 1.0]
xlim = None
ylim = None

# style = ['science']
# style = ['science', 'notebook']
# style = ['science', 'nature']
style = ["science", "ieee"]
# style = ['science', 'grid']
colors = ["red", "black"]

plot1 = SubPlot(
    files,
    [("time", "val1")] * len(files),
    xtitle=r"time $[s]$",
    ytitle=(r"$\chi$"),
    labels=labels,
    style=style,
    legend_title="method",
    title="x displacement",
    xlim=xlim,
    ylim=ylim,
    colors=None,
    grid=True,
    show_legend=False,
    line_wide=2,
    project_on_x={
        "filenames": files[0],
        "names": ("time", "val1"),
        "x": [1.1, 2.7],
        "color": "blue",
        "size": 1.5,
    },
)

plot2 = SubPlot(
    files,
    [("time", "val2")] * len(files),
    xtitle=r"time $[s]$",
    ytitle=(r"$\mu$"),
    labels=labels,
    style=style,
    legend_title="method",
    title="x displacement",
    xlim=xlim,
    ylim=ylim,
    colors=None,
    grid=True,
    show_legend=False,
    line_wide=2,
    project_on_x={
        "names": "time",
        "x": [1.4, 2.7],
        "color": "blue",
        "size": 1.5,
    },
)

title = None

plottool = Plot()

plottool.plot(title, [[plot1, plot2], [plot2, plot1]], legend=labels, ncol=6)
plottool.save_fig("examples/results/test1.png", fig_param)
plottool.show()
