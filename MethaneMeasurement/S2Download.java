**************** Sentinel-2 Imagery Download From Google Earth Engine ****************

// Import study region into GEE
var shp = ee.FeatureCollection(arizona).geometry()
Map.addLayer(shp, {}, 'Arizona')


// Import Sentinel-2 imagery
var start = ee.Date('2021-5-01');
var finish = ee.Date('2021-6-01');

var s2 = ee.ImageCollection("COPERNICUS/S2").select("B11")
  .filterBounds(arizona)
  .filter(ee.Filter.date(start, finish))
print(s2)

var clip_all = function(img){
  return img.clip(arizona)
}

var s2_clip = s2.map(clip_all)
var s2_list = s2_clip.toList(s2_clip.size())
var n = s2_list.size().getInfo()


// Display and download clipped imagery
for (var i = 0; i < n; i++){
  var img = ee.Image(s2_list.get(i))
  var date = img.date().format('yyyyMMdd').getInfo()
  var disp = {min: 0, max: 10000, palette: ['000000', 'FFFFFF']}
  Map.addLayer(img, disp, 'Image_'+date)
  
  print('Single-band GeoTIFF files wrapped in a zip file ' + date,
  img.getDownloadURL({
    name: 'Sentinel2-B11'+date,
    bands: ['B11'],
    region: shp
  }))
  }
