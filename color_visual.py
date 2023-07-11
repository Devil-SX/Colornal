import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objs as go
import plotly.graph_objs.layout as la
import colorsys

file = st.file_uploader("Chose an image file", type=["jpg", "png"])

if file:
    # 读取图片并转换为RGB格式
    img = Image.open(file).convert("RGB")

    # Subsampling
    height, width = img.size
    scale = np.sqrt(height*width/1e3)

    new_width = int(width / scale)
    new_height = int(height / scale)

    img = img.resize((new_width, new_height), Image.LANCZOS)


    # 将图片数据转换为numpy数组
    img_data = np.array(img)

    # 将RGB值归一化到0-1范围内
    img_data = img_data / 255.0

    # 使用numpy的vectorize函数创建一个向量化版本的rgb_to_hls函数
    vec_rgb_to_hls = np.frompyfunc(colorsys.rgb_to_hls, 3, 3)
    # 将RGB值转换为HLS值
    h, l, s = vec_rgb_to_hls(
        img_data[..., 0].flatten(), img_data[..., 1].flatten(), img_data[..., 2].flatten()
    )


    # 绘图
    # 创建一个三维图形
    color = [f"hsl({x[0]*360:.0f},{x[1]:.0%},{x[2]:.0%})" for x in zip(h,s,l)]
    marker_data = go.Scatter3d(
        x=h, 
        y=s, 
        z=l, 
        marker=go.scatter3d.Marker(size=2,
                                   opacity=0.8,
                                   color=color), 
        mode='markers'
    )
    layout = go.Layout(
        showlegend=True,
        scene=la.Scene(
            xaxis=la.scene.XAxis(title='Hue'),
            yaxis=la.scene.YAxis(title='Saturation'),
            zaxis=la.scene.ZAxis(title='Lightness')
        )
    )

    fig=go.Figure(data=marker_data,layout=layout)


    # Image Layout
    col1, col2 = st.columns(2)
    col1.header("Image")
    col1.image(file)

    col2.header("Chart")
    col2.plotly_chart(fig)