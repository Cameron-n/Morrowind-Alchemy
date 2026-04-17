window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {
        pointToLayer: function(feature, latlng) {
            const flag = L.icon({
                iconUrl: `assets/markers/${feature.properties.icon}.png`,
                iconSize: [16, 16],
            });
            return L.marker([latlng.lat-0, latlng.lng+0], {
                icon: flag
            });
        },
        clusterToLayer: function (feature, latlng, options) {
            const iconSize = 40;
            const classNames = [
                {minCount: 0, className: "marker-cluster marker-cluster-small"},
                {minCount: 100, className: "marker-cluster marker-cluster-medium"},
                {minCount: 1000, className: "marker-cluster marker-cluster-large"},
            ]
            const count = feature.properties.point_count;
            let className = "";
            for (let i in classNames) {
                if (count > classNames[i]["minCount"]) {
                    className = classNames[i]["className"]
                }
            }
            const icon = L.divIcon({
                html: '<div><span>' + feature.properties.point_count_abbreviated + '</span></div>',
                className: className,
                iconSize: L.point(iconSize, iconSize),
            });
            return L.marker([latlng.lat-0, latlng.lng+0], {
                icon: icon
            });
        }
    }
});