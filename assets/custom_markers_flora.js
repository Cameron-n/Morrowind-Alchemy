window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {
        pointToLayer: function(feature, latlng) {
            const flag = L.icon({
                iconUrl: `assets/icons/${feature.properties.icon}.png`,
                iconSize: [32, 32]
            });
            return L.marker(latlng, {
                icon: flag
            });
        }
    }
});