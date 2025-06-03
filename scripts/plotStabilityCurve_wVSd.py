import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Example data
data = np.array(
    [
        [1, 10, -1, True],
        [1, 20, -1, True],
        [1, 30, -1, True],
        [1, 34, -1, True],
        [1, 38, -1, True],
        [1, 50, -1, True],
        [1, 60, -1, True],
        [1, 70, -1, True],
        [1, 80, -1, True],
        [1, 90, -1, True],
        [1, 110, -1, True],
        [1, 130, -1, True],
        [1.25, 10, -1, True],
        [1.25, 20, -1, True],
        [1.25, 30, -1, True],
        [1.25, 40, -1, True],
        [1.25, 50, -1, True],
        [1.25, 60, -1, True],
        [1.25, 70, -1, True],
        [1.25, 80, -1, True],
        [1.25, 90, -1, True],
        [1.25, 110, -1, True],
        [1.25, 130, -1, True],
        [1.5, 10, -1, True],
        [1.5, 20, -1, True],
        [1.5, 30, -1, True],
        [1.5, 45, -1, True],
        [1.5, 50, -1, True],
        [1.5, 55, -1, True],  # I think it starts absolute instability but very slightly
        [1.5, 58, 0.5, True],
        [1.5, 60, 1, True],
        # I am not sure, looks a mix between nonlinear and absolute instability, because the instability is conevected downstream with a lot of energy, but it differs from the initial transient effects.
        [1.5, 65, 1, True],  # I am not sure. same as above d1.5_w60
        [1.5, 70, 1, True],
        [1.5, 75, 1, True],
        [1.5, 80, 1, True],
        [1.5, 100, 1, True],
        [1.5, 120, 1, True],
        [1.75, 10, -1, True],
        [1.75, 20, -1, True],
        [1.75, 30, -1, True],
        [1.75, 40, -1, True],
        [1.75, 43, -1, True],
        [1.75, 45, -1, True],
        # Looks marginally stable, on the limit of absolute instability (check history points)
        [1.75, 47, 0.5, True],
        [1.75, 50, 0.5, True],
        [1.75, 53, 0.5, True],
        [1.75, 55, 0.75, True],  # transition point, ordered convectively unstable
        [1.75, 57, 1, True],
        [1.75, 60, 1, True],
        [1.75, 70, 1, True],
        [1.75, 90, 1, True],
        [1.75, 110, 1, True],
        [1.75, 130, 1, True],
        [2, 10, -1, True],
        [2, 16, -1, True],
        [2, 24, -1, True],
        [2, 28, -1, True],
        [2, 32, -1, True],
        [2, 36, -1, True],
        [2, 38, -1, True],
        # Looks marginally stable, on the limit of absolute instability (check history points)
        [2, 40, 0.5, True],  # several frequencies coupled
        [2, 42, 0.5, True],
        [2, 44, 0.5, True],
        [2, 46, 0.5, True],
        [2, 48, 0.5, True],
        [2, 50, 0.5, True],
        [2, 51, 0.5, True],
        [2, 52, 1, True],  # smthing else
        [2, 53, 1, True],
        [2, 54, 1, True],
        [2, 56, 1, True],
        [2, 58, 1, True],
        [2, 60, 1, True],
        [2, 65, 1, True],
        [2, 70, 1, True],
        [2, 80, 1, True],
        [2.25, 10, -1, True],
        [2.25, 16, -1, True],
        [2.25, 25, -1, True],
        [2.25, 30, -1, True],
        [2.25, 31, -1, True],
        [2.25, 32, 0.5, True],
        [2.25, 33, 0.5, True],
        [2.25, 35, 0.5, True],
        [2.25, 40, 0.5, True],
        [2.25, 43, 0.5, True],
        # this one is very interesting. we have an absolute instability that existes a freqeuncy convectively unstable, but then in the middle of the domain that frequency is not small enough, and so it becomes convectively stable (check neutral stability curve for blasius)
        [2.25, 45, 0.75, True],
        [2.25, 47, 1, True],
        [2.25, 50, 1, True],
        [2.25, 55, 1, True],
        [2.25, 60, 1, True],
        [2.5, 10, -1, True],
        [2.5, 20, -1, True],
        [2.5, 21, 1, False],  # It looks like a transient state, not chaotic at all
        [2.5, 22, 1, True],
        [2.5, 23, 1, True],
        [2.5, 24, 1, True],
        [2.5, 25, 1, True],
        [2.5, 30, 1, True],
        [2.5, 35, 1, True],
        [2.5, 40, 1, True],
        [2.5, 45, 1, True],
        [2.75, 10, -1, True],
        [2.75, 15, -1, True],
        [2.75, 15.5, 1, True],
        [2.75, 16, 1, True],
        [2.75, 16.5, 1, True],
        [2.75, 17, 1, True],
        [2.75, 18, 1, True],
        [2.75, 19, 1, True],
        [2.75, 20, 1, True],
        [3, 10, -1, True],
        [3, 15, -1, True],
        [3, 15.5, 1, True],
        [3, 16, 1, True],
        [3, 17, 1, True],
        [3, 18, 1, True],
        [3, 22, 1, True],
        [3, 26, 1, True],
        [3.25, 10, -1, True],
        [3.25, 15, -1, True],
        [3.25, 15.5, 1, True],
        [3.25, 16, 1, True],
        [3.25, 16.5, 1, True],
        [3.5, 10, -1, True],
        [3.5, 15, -1, True],
        [3.5, 15.5, 1, True],
        [3.5, 16, 1, True],
        [3.75, 10, -1, True],
        [3.75, 15, -1, True],
        [3.75, 15.5, -1, True],
        [3.75, 16, 1, True],
        [3.75, 16.5, 1, True],
        [4, 10, -1, True],
        [4, 14, -1, True],
        [4, 15, -1, True],
        [4, 16, -1, True],
        [4, 16.5, 1, True],
        [4, 17, 1, True],
        [4, 18, 1, True],
        [4, 19, 1, True],
    ]
)
# Separamos
depths = data[:, 0]
widths = data[:, [1, 3]]
labels = data[:, 2]

plotargs_array = np.array(
    [
        ["Globally stable modes", "dodgerblue"],
        ["Abs unstable modes of high freq", "orange"],
        ["", "orange"],
        ["Abs + Conv unstable modes of low freq (trans region)", "red"],
        ["", "red"],
        ["Chaotic behavior", "black"],
    ]
)


def plot_lines(ax):
    # Listas donde guardaremos los resultados
    depth_list = []
    max_stable_width = []
    min_abs_unstable_width = []
    max_abs_unstable_width = []
    min_more_abs_unstable_width = []
    max_more_abs_unstable_width = []
    min_glob_unstable_width = []

    # Para cada valor único de depth
    for depth in np.unique(depths):
        mask = depths == depth
        widths_at_depth = widths[mask, :]
        labels_at_depth = labels[mask]

        # Estables
        stable_widths = widths_at_depth[labels_at_depth == -1]
        abs_unstable_widths = widths_at_depth[labels_at_depth == 0.5]
        more_abs_unstable_widths = widths_at_depth[labels_at_depth == 0.75]
        glob_unstable_widths = widths_at_depth[labels_at_depth == 1]

        if stable_widths.size > 0:
            max_stable = np.max(stable_widths, axis=0)
        else:
            max_stable = np.array([np.nan, np.nan])  # No hay estable para este depth

        if glob_unstable_widths.size > 0:
            min_glob_unstable = np.min(glob_unstable_widths, axis=0)
        else:
            min_glob_unstable = np.array(
                [np.nan, np.nan]
            )  # No hay inestable para este depth

        if abs_unstable_widths.size > 0:
            min_abs_unstable = np.min(abs_unstable_widths, axis=0)
            max_abs_unstable = np.max(abs_unstable_widths, axis=0)
        else:
            min_abs_unstable = np.array([np.nan, np.nan])
            max_abs_unstable = np.array([np.nan, np.nan])

        if more_abs_unstable_widths.size > 0:
            min_more_abs_unstable = np.min(more_abs_unstable_widths, axis=0)
            max_more_abs_unstable = np.max(more_abs_unstable_widths, axis=0)
        else:
            min_more_abs_unstable = np.array([np.nan, np.nan])
            max_more_abs_unstable = np.array([np.nan, np.nan])

        depth_list.append(depth)
        max_stable_width.append(max_stable)
        min_abs_unstable_width.append(min_abs_unstable)
        max_abs_unstable_width.append(max_abs_unstable)
        min_more_abs_unstable_width.append(min_more_abs_unstable)
        max_more_abs_unstable_width.append(max_more_abs_unstable)
        min_glob_unstable_width.append(min_glob_unstable)

    # Convertimos a arrays
    depth_list = np.array(depth_list)
    max_stable_width = np.array(max_stable_width)
    min_abs_unstable_width = np.array(min_abs_unstable_width)
    max_abs_unstable_width = np.array(max_abs_unstable_width)
    min_more_abs_unstable_width = np.array(min_more_abs_unstable_width)
    max_more_abs_unstable_width = np.array(max_more_abs_unstable_width)
    min_glob_unstable_width = np.array(min_glob_unstable_width)

    # Dibujamos

    plot_array = np.array([
        max_stable_width,
        min_abs_unstable_width,
        max_abs_unstable_width,
        min_more_abs_unstable_width,
        max_more_abs_unstable_width,
        min_glob_unstable_width,
    ])

    print(plotargs_array.shape, plot_array.shape)

    doMarks = False
    for x, (label, color) in zip(plot_array[[0,5]], plotargs_array[[0,5]]):
        doPlot(x[:, 0], depth_list, x[:, 1], color, label, ax, doMarks, doLines=True, doLabels=False)


def doPlot(x, y, marks, color, label, ax, doMarks=True, alpha=1.0, doLines=False, doLabels=True):
    markersize = 6

    omark = "-o" if doLines else "o"
    smark = "-s" if doLines else "s"
    if doMarks:
        marks = np.array(marks, dtype=bool)
        if doLabels:
            ax.plot(
                x[marks],
                y[marks],
                omark,
                color=color,
                markersize=markersize,
                label=label,
                alpha=alpha,
            )
        else:
            ax.plot(
                x[marks],
                y[marks],
                omark,
                color=color,
                markersize=markersize,
                alpha=alpha,
            )
        ax.plot(
            x[~marks], y[~marks], smark, color=color, markersize=markersize, alpha=alpha
        )
    else:
        if doLabels:
            ax.plot(x, y, omark, color=color, markersize=markersize, label=label, alpha=alpha)
        else:
            ax.plot(x, y, omark, color=color, markersize=markersize, alpha=alpha)


def plot(add_images: bool, doMarks: bool, add_lines: bool):
    # Listas donde guardaremos los resultados
    stable_values = data[data[:, 2] == -1]
    abs_unstable = data[data[:, 2] == 0.5]
    abs_conv_unstable = data[data[:, 2] == 0.75]
    nl_unstable = data[data[:, 2] == 1]

    plot_array = [stable_values, abs_unstable, abs_conv_unstable, nl_unstable]

    fig, ax = plt.subplots(figsize=(8, 5))

    for x, (label, color) in zip(plot_array, plotargs_array[[0, 1, 3, 5]]):
        if add_lines:
            # Plot lines between points
            doPlot(x[:, 1], x[:, 0], x[:, 3], color, label, ax, doMarks, alpha=0.5)
        else:
            # Plot scattered points
            doPlot(x[:, 1], x[:, 0], x[:, 3], color, label, ax, doMarks)
    if add_lines:
        plot_lines(ax)

    # Add images
    if add_images:
        addAllimages(ax)
        ax.set_xlim(-40, 140)
        ax.set_ylim(-1, 5)

    plt.xlabel("w/delta*")
    plt.ylabel("d/delta*")
    plt.legend()
    plt.grid(True)
    plt.show()


def addAllimages(ax):
    addImageToPlot(
        -25,
        3,
        "Images/d4_w15.png",
        True,
        ax,
        x_plot=15,
        y_plot=4,
        color=plotargs_array[0, 1],
        zoom=0.15,
    )
    addImageToPlot(
        10,
        -0.5,
        "Images/d1_w38.png",
        True,
        ax,
        x_plot=38,
        y_plot=1,
        color=plotargs_array[0, 1],
        zoom=0.25,
    )
    addImageToPlot(
        95,
        3,
        "Images/d2.25_w35.png",
        True,
        ax,
        x_plot=35,
        y_plot=2.25,
        color=plotargs_array[1, 1],
        zoom=0.25,
    )
    addImageToPlot(
        100,
        -0.75,
        "Images/d1.5_w80.png",
        True,
        ax,
        x_plot=80,
        y_plot=1.5,
        color=plotargs_array[5, 1],
        zoom=0.7,
    )
    addImageToPlot(
        60,
        3.75,
        "Images/d2.25_w55.png",
        True,
        ax,
        x_plot=55,
        y_plot=2.25,
        color=plotargs_array[5, 1],
        zoom=0.3,
    )


def addImageToPlot(
    img_x: float,
    img_y: float,
    pathToImg: str,
    plotArrow: bool,
    ax,
    x_plot: float = 15,
    y_plot: float = 4,
    color: str = "black",  # arrow and frame color
    zoom: float = 0.1,  # optional: control image size
):
    img = mpimg.imread(pathToImg)
    imagebox = OffsetImage(img, zoom=zoom)

    # Add arrow *first* so image is drawn on top
    if plotArrow:
        scale = 1.5
        ax.annotate(
            "",
            xy=(x_plot, y_plot),
            xytext=(img_x, img_y),
            arrowprops=dict(
                arrowstyle=f"Simple,head_length={scale},head_width={scale}",
                color=color,
            ),
            zorder=1,  # draw under image
        )

    # Add the image with colored frame
    ab = AnnotationBbox(
        imagebox,
        (img_x, img_y),
        frameon=True,
        bboxprops=dict(edgecolor=color, linewidth=1.5),
        zorder=2,  # draw on top
        
    )
    ax.add_artist(ab)


if __name__ == "__main__":
    add_images = False
    doMarks = False
    add_lines = False
    plot(add_images, doMarks, add_lines)
