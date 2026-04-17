var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};
var dmc = window.dash_mantine_components;

dmcfuncs.renderOptionSelect = function ({ option }, { appa_ids }) {

  var icon = React.createElement(dmc.Image, { src: "assets/icons/"+appa_ids[option.value].replace(/\\/g, "/")+".png", w: 24 });

  return React.createElement(
    dmc.Group,
    { flex: "1", gap: "xs" },
    icon,
    option.label
  );
};