window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        customMarkersFlora: function(feature, latlng) {
            const flag = L.icon({
                iconUrl: `C:/Users/camer/Documents/Morrowind-Alchemy/assets/icons/${feature.properties.icon}.png`,
                iconSize: [32, 32],
            });
            return L.marker(latlng, {
                icon: flag
            });
        };
    }
});