import merge_subarea_lvr_land as export_service


data_a = export_service.merge_subarea("./temp/h_lvr_land_a.xls")
data_b = export_service.merge_subarea("./temp/h_lvr_land_b.xls")
data_all = data_a + data_b
export_service.data_export(data_all)