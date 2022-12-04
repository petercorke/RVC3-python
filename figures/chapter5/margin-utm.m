% landAreas = readgeotable("landareas.shp");
% row = landAreas.Name == "Australia";
% landAreasSubset = landAreas(row,:);
% landAreasSubset.Shape
% worldmap([-50 -10], [110, 160]);
% geoshow(landAreasSubset)
clf

load coastlines
a = axesm('mercator', MapLatLimit=[-50 -8],MapLonLimit=[90 158], Frame='off', FLineWidth = 0)
plotm(coastlat,coastlon)
a.Box='off'

hold on
for zone=49:57
    for band='GHJKL'
        fprintf('%d%c\n', zone, band)
        utm = sprintf('%d%c ', zone, band);
        [latlim,lonlim] = utmzone(utm(1:3));
        lat = [latlim(1) latlim(1) latlim(2) latlim(2) latlim(1)];
        lon = [lonlim(2) lonlim(1) lonlim(1) lonlim(2) lonlim(2)];
        plotm(lat, lon)
        textm(mean(lat), mean(lon), utm, HorizontalAlignment='center', FontWeight='bold', FontSize=14)
    end
end