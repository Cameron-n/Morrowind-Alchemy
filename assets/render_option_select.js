var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};
var dmc = window.dash_mantine_components;

dmcfuncs.renderOptionSelect = function ({ option }, { appa_ids }) {

  // Need to somehow access data from JavsScript to get image file names
  var icon = React.createElement(dmc.Image, { src: "assets/icons/"+appa_ids[option.value].replace(/ /g,"_")+".png", w: 24 });
  
  if (option.value === "Journeyman's Calcinator") {
      icon = React.createElement(dmc.Image, { src: "assets/icons/m/tx_calcinator_01.png", w: 24 });
  }

  return React.createElement(
    dmc.Group,
    { flex: "1", gap: "xs" },
    icon,
    option.label
  );
};