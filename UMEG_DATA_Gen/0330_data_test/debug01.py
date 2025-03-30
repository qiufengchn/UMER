import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, MultiLineString
import numpy as np
from shapely.ops import unary_union
import random
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, box  # 添加 Point 导入

def create_road_network(buildings_gdf, study_area):
    # 道路类型及其参数
    road_types = {
        'primary': {
            'width': (20, 30),  # 米
            'probability': 0.1,
            'min_length': 500,
            'max_length': 2000,
            'speed_limit': 60  # km/h
        },
        'secondary': {
            'width': (15, 20),
            'probability': 0.3,
            'min_length': 300,
            'max_length': 1000,
            'speed_limit': 50
        },
        'local': {
            'width': (8, 15),
            'probability': 0.6,
            'min_length': 100,
            'max_length': 500,
            'speed_limit': 30
        }
    }

    # 添加节点
    nodes = []
    buildings_union = unary_union(buildings_gdf.geometry)
    for x in x_points:
        for y in y_points:
            # 将坐标元组转换为 Point 对象
            point = Point(x, y)
            # 确保节点不在建筑物内部
            if not buildings_union.contains(point):
                nodes.append((x, y))  # 仍然存储为元组用于后续使用
                G.add_node((x, y))
    
    # 添加边（道路）
    roads = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1, node2 = nodes[i], nodes[j]
            # 计算两点间距离
            distance = ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5
            
            # 选择道路类型
            road_type = random.choices(list(road_types.keys()),
                                     [t['probability'] for t in road_types.values()])[0]
            params = road_types[road_type]
            
            # 检查距离是否在允许范围内
            if params['min_length'] <= distance <= params['max_length']:
                road = LineString([node1, node2])
                # 创建道路缓冲区
                road_width = random.uniform(*params['width'])
                road_buffer = road.buffer(road_width/2)
                
                # 检查是否与建筑物或现有道路重叠
                if not road_buffer.intersects(buildings_union):
                    roads.append({
                        'geometry': road,
                        'type': road_type,
                        'width': road_width,
                        'length': distance,
                        'speed_limit': params['speed_limit']
                    })
                    G.add_edge(node1, node2)
    
    # 创建GeoDataFrame
    roads_gdf = gpd.GeoDataFrame(roads)
    
    # 保存为shapefile
    roads_gdf.to_file('roads.shp')
    
    return roads_gdf

    # 创建网格点作为可能的道路节点
    grid_size = 100  # 米
    minx, miny, maxx, maxy = study_area.bounds
    x_points = np.arange(minx, maxx, grid_size)
    y_points = np.arange(miny, maxy, grid_size)
    
    # 创建图形对象
    G = nx.Graph()
    
    # 添加节点
    nodes = []
    buildings_union = unary_union(buildings_gdf.geometry)
    for x in x_points:
        for y in y_points:
            point = (x, y)
            # 确保节点不在建筑物内部
            if not buildings_union.contains(point):
                nodes.append(point)
                G.add_node(point)
    
    # 添加边（道路）
    roads = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1, node2 = nodes[i], nodes[j]
            # 计算两点间距离
            distance = ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5
            
            # 选择道路类型
            road_type = random.choices(list(road_types.keys()),
                                     [t['probability'] for t in road_types.values()])[0]
            params = road_types[road_type]
            
            # 检查距离是否在允许范围内
            if params['min_length'] <= distance <= params['max_length']:
                road = LineString([node1, node2])
                # 创建道路缓冲区
                road_width = random.uniform(*params['width'])
                road_buffer = road.buffer(road_width/2)
                
                # 检查是否与建筑物或现有道路重叠
                if not road_buffer.intersects(buildings_union):
                    roads.append({
                        'geometry': road,
                        'type': road_type,
                        'width': road_width,
                        'length': distance,
                        'speed_limit': params['speed_limit']
                    })
                    G.add_edge(node1, node2)
    
    # 创建GeoDataFrame
    roads_gdf = gpd.GeoDataFrame(roads)
    
    # 保存为shapefile
    roads_gdf.to_file('roads.shp')
    
    return roads_gdf

def visualize_buildings_and_roads(buildings_gdf, roads_gdf):
    # 创建图形
    fig, ax = plt.subplots(figsize=(15, 15))
    
    # 绘制建筑物
    buildings_gdf.plot(column='type', categorical=True, 
                      legend=True, ax=ax, alpha=0.6)
    
    # 绘制道路网络
    roads_gdf.plot(column='type', categorical=True, 
                  legend=True, ax=ax, linewidth=1)
    
    plt.title('建筑物和道路网络分布图')
    plt.xlabel('X (米)')
    plt.ylabel('Y (米)')
    plt.show()

# 主函数
def main():
    # 读取之前生成的建筑物数据
    buildings_gdf = gpd.read_file('buildings.shp')
    study_area = buildings_gdf.unary_union.convex_hull
    
    # 生成道路网络
    roads_gdf = create_road_network(buildings_gdf, study_area)
    
    # 可视化
    visualize_buildings_and_roads(buildings_gdf, roads_gdf)

if __name__ == "__main__":
    main()