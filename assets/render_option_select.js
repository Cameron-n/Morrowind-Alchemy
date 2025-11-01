var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};
var dmc = window.dash_mantine_components;

dmcfuncs.renderOptionSelect = function ({ option }) {

  var icon = React.createElement(dmc.Image, { src: "assets/icons/MW-icon-tool-"+option.value.replace(/ /g,"_")+".png", w: 24 });
  
  if (option.value === "Journeyman's Calcinator") {
      icon = React.createElement(dmc.Image, { src: "assets/icons/MW-icon-tool-Apprentice's_Calcinator.png", w: 24 });
  }

  return React.createElement(
    dmc.Group,
    { flex: "1", gap: "xs" },
    icon,
    option.label
  );
};