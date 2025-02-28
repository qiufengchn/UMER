import geopandas as gpd

# 读取建筑和土地利用数据
buildings_path = r"F:\ScientificDatabase\paper03\wuhan_district\Wuhan_Building_GloBFP_cleaned.shp"
landuse_path = r"F:\ScientificDatabase\paper03\wuhan_district\Wuhan_block_function_2018\wuhan_block_function.shp"

buildings_gdf = gpd.read_file(buildings_path) 
landuse_gdf = gpd.read_file(landuse_path)

# 确保两个数据集使用相同的坐标系
if buildings_gdf.crs != landuse_gdf.crs:
    buildings_gdf = buildings_gdf.to_crs(landuse_gdf.crs)

# 要保留的土地利用字段
landuse_fields = ['F_AREA', 'City_CODE', 'UUID', 'Level1', 'Level2', 'Level1_cn', 'Level2_cn']

# 进行空间连接
buildings_with_landuse = gpd.sjoin(buildings_gdf, 
                                  landuse_gdf[landuse_fields + ['geometry']], 
                                  how="left", 
                                  predicate="within")

# 检查结果
print("原始建筑数据字段:", list(buildings_gdf.columns))
print("合并后数据字段:", list(buildings_with_landuse.columns))
print("总建筑数量:", len(buildings_with_landuse))
print("未分类建筑数量:", buildings_with_landuse['Level1_cn'].isna().sum())
success_rate = ((len(buildings_with_landuse) - buildings_with_landuse['Level1_cn'].isna().sum()) 
                / len(buildings_with_landuse) * 100)
print(f"分类成功率: {success_rate:.2f}%")

# 保存结果
output_path = r"F:\ScientificDatabase\paper03\wuhan_district\buildings_with_landuse_full.shp"
buildings_with_landuse.to_file(output_path)

print(f"\n结果已保存至: {output_path}")

# 显示分类统计
print("\n一级用地类型建筑数量统计:")
print(buildings_with_landuse['Level1_cn'].value_counts())
print("\n二级用地类型建筑数量统计:") 
print(buildings_with_landuse['Level2_cn'].value_counts())
