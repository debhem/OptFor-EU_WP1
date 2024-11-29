library(ecmwfr)
library(dplyr)
# psw cds
# wf_set_key(service = "cds",
#            key = "47b85274-0e3f-40fa-8b3d-7e2ef2294bd9",
#            user = "9924")
# 


# # you can retrieve the key using
# wf_set_key(service = "cds")

# the output should be the key you provided
# in this case represented by the fake X string.
# "XXXXXXXXXXXXXXXXXXXXXX"
# 
# wf_get_key(user = "alexandru.dumitrescu@gmail.com")
# 
# 
# 
ani <- 1984:2021
ani_desc <-
  list.files("nc/cerra/tmax", pattern = "*.grib") |>
  strsplit("_|\\.") %>% do.call(rbind,.) |> as_tibble() |> select(V2) |> unlist() |> as.numeric()
ani <- ani[!ani %in% ani_desc]

for (i in 1:length(ani)) {
  request <- list(
    "dataset_short_name" = "reanalysis-cerra-single-levels",
    "variable" = "maximum_2m_temperature_since_previous_post_processing",
    "data_type" = "reanalysis",
    "product_type" = "forecast",
    "year"  = ani[i],
    "month" = c(1:12),
    "day" = c(1:31),
    "time" =   seq(0,21,3),
    'leadtime_hour' = '3',
    "level_type" = "surface_or_atmosphere",
    "target" = paste0("tmax_",ani[i],".grib")
  )
  
  wf_request(
    request,
    user = "9924",
    path  = "nc/cerra/tmax" 
  )
}
