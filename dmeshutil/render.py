import plotly.graph_objects as go
import numpy as np
from typing import List

def render_mesh3d(vertices: List[np.ndarray], 
                faces: List[np.ndarray], 
                color: List[str],
                opacity: List[float],
                render_face: List[bool],
                render_vert: List[bool],
                path: str):

    num_mesh = len(vertices)

    mesh_go = []
    
    for i in range(num_mesh):
        t_vertices = vertices[i]
        t_faces = np.unique(faces[i], axis=0)
        t_color = color[i]
        t_opacity = opacity[i]
        t_render_face = render_face[i]
        t_render_vert = render_vert[i]

        if len(t_faces) == 0:
            continue

        if t_render_face:
            t_face_go = go.Mesh3d(
                x=t_vertices[:, 0],
                y=t_vertices[:, 1],
                z=t_vertices[:, 2],
                # i, j and k give the vertices of triangles
                i=t_faces[:, 0],
                j=t_faces[:, 1],
                k=t_faces[:, 2],
                color=t_color,
                opacity=t_opacity,
                flatshading=False,
                showscale=True
            )
            mesh_go.append(t_face_go)

        if t_render_vert:

            t_faces1 = np.unique(t_faces)
            t_vertices1 = t_vertices[t_faces1]

            t_vert_go = go.Scatter3d(
                   x=t_vertices1[:, 0].cpu().numpy(),
                   y=t_vertices1[:, 1].cpu().numpy(),
                   z=t_vertices1[:, 2].cpu().numpy(),
                   mode='markers',
                   marker=dict(color='red', size=3))

            mesh_go.append(t_vert_go)  

    # render;
    fig = go.Figure(data=mesh_go)

    xaxis = [vertices[0][:, 0].min(), vertices[0][:, 0].max()]
    yaxis = [vertices[0][:, 1].min(), vertices[0][:, 1].max()]
    zaxis = [vertices[0][:, 2].min(), vertices[0][:, 2].max()]

    fig.update_layout(
        scene = dict(
            xaxis = dict(nticks=4, range=xaxis,),
            yaxis = dict(nticks=4, range=yaxis,),
            zaxis = dict(nticks=4, range=zaxis,),),
        )
    
    fig.update_layout(scene_aspectmode='cube')

    if path[-5:] != ".html":
        path = path + ".html"
    fig.write_html(path)