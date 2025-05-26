import plotly.graph_objects as go
from numpy.typing import ArrayLike


def plot_voxels(
    voxels: list[ArrayLike],
    color=None,
    n=3,
    fig=None,
    show_coord_markers=False,
    opacity=0.4,
    cube_size=0.92,
):
    """
    Plots a 3D blokk shape using Plotly, visualizing a collection of voxel coordinates as cubes within a bounded game board.

    Args:
        voxels (list[ArrayLike]): List of (x, y, z) coordinates representing the voxels to plot.
        color (str or None, optional): Color of the cubes. If None, Plotly's default color is used.
        n (int, optional): Size of the bounding game board (default is 3).
        fig (plotly.graph_objs.Figure or None, optional): Existing Plotly figure to add traces to. If None, a new figure is created.
        show_coord_markers (bool, optional): If True, shows coordinate markers at voxel positions (default is False).
        opacity (float, optional): Opacity of the cubes (default is 0.4).
        cube_size (float, optional): Size of each cube relative to the grid cell (default is 0.92).

    Returns:
        plotly.graph_objs.Figure: The Plotly figure object containing the 3D plot.
    """
    xs, ys, zs = zip(*voxels)
    if fig is None:
        fig = go.Figure()

    if show_coord_markers:
        fig.add_trace(
            go.Scatter3d(
                x=xs,
                y=ys,
                z=zs,
                mode="markers",
                marker=dict(
                    size=10, color=color, opacity=1, line=dict(width=2, color="black")
                ),
            )
        )

    offset = (1 - cube_size) / 2
    # Draw cubes for each block
    for x, y, z in voxels:
        fig.add_trace(
            go.Mesh3d(
                x=[
                    x + offset,
                    x + cube_size + offset,
                    x + cube_size + offset,
                    x + offset,
                    x + offset,
                    x + cube_size + offset,
                    x + cube_size + offset,
                    x + offset,
                ],
                y=[
                    y + offset,
                    y + offset,
                    y + cube_size + offset,
                    y + cube_size + offset,
                    y + offset,
                    y + offset,
                    y + cube_size + offset,
                    y + cube_size + offset,
                ],
                z=[
                    z + offset,
                    z + offset,
                    z + offset,
                    z + offset,
                    z + cube_size + offset,
                    z + cube_size + offset,
                    z + cube_size + offset,
                    z + cube_size + offset,
                ],
                color=color,
                opacity=opacity,
                alphahull=1,
                showscale=False,
            )
        )
    # Draw the bounding game board (transparent)
    fig.add_trace(
        go.Mesh3d(
            x=[0, n, n, 0, 0, n, n, 0],
            y=[0, 0, n, n, 0, 0, n, n],
            z=[0, 0, 0, 0, n, n, n, n],
            color="lightgray",
            opacity=0.1,
            alphahull=0,
            showscale=False,
        )
    )
    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectratio=dict(x=1, y=1, z=1),
            xaxis=dict(range=[0, n]),
            yaxis=dict(range=[0, n]),
            zaxis=dict(range=[0, n]),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
    )
    return fig
