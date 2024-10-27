import web_crawler_for_plvrgov as crawler_gov
import web_crawler_for_leju_subarea as crawler_leju
import merge_subarea_lvr_land as export_service

crawler_gov.web_crawler()
crawler_gov.extract_download_zip()
crawler_leju.web_crawler()

data_a = export_service.merge_subarea("./temp/h_lvr_land_a.xls")
data_b = export_service.merge_subarea("./temp/h_lvr_land_b.xls")
data_all = data_a + data_b
export_service.data_export(data_all)