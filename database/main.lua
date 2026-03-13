-- Create log for data
-- The log name includes the versions of Tamriel Data,
-- Tamriel Rebuilt, Project:Cyrodiil, and Project:Skyrim.
-- All the official plugins, except firemoth, are included,
-- and the GOTY edition is used.
-- No other mods (should) be included in this script's output.
local log_name = "TD 25.05 TR 25.05 Cyr 21.12a Sky 24.12b"

local log_npcs = mwse.Logger.new{moduleName = "NPCs"}
log_npcs:setOutputFile(log_name)
log_npcs.level = "DEBUG"

local log_ing = mwse.Logger.new{moduleName = "Ings"}
log_npcs:setOutputFile(log_name)
log_ing.level = "DEBUG"

local log_tool = mwse.Logger.new{moduleName="Tool"}
log_npcs:setOutputFile(log_name)
log_tool.level = "DEBUG"

local log_ingre = mwse.Logger.new{moduleName="Ingre"}
log_npcs:setOutputFile(log_name)
log_ingre.level = "DEBUG"

local log_flo = mwse.Logger.new{moduleName="Flora"}
log_flo:setOutputFile(log_name)
log_flo.level = "DEBUG"

local log_temp = mwse.Logger.new{moduleName="temp"}
log_temp:setOutputFile(log_name)
log_temp.level = "DEBUG"

local log_cre = mwse.Logger.new{moduleName="Creature"}
log_cre:setOutputFile(log_name)
log_cre.level = "DEBUG"

local log_cre_l = mwse.Logger.new{moduleName="Leveled_Creature"}
log_cre_l:setOutputFile(log_name)
log_cre_l.level = "DEBUG"

local log_con = mwse.Logger.new{moduleName="Container"}
log_con:setOutputFile(log_name)
log_con.level = "DEBUG"

local log_eff = mwse.Logger.new{moduleName="Effect"}
log_eff:setOutputFile(log_name)
log_eff.level = "DEBUG"

local log_loo = mwse.Logger.new{moduleName="Loose"}
log_loo:setOutputFile(log_name)
log_loo.level = "DEBUG"

-- Source - https://stackoverflow.com/a/7927877
-- Posted by lhf, modified by community. See post 'Timeline' for change history
-- Retrieved 2026-02-16, License - CC BY-SA 3.0
-- Function to invert a table's keys and values
local function table_invert(t)
   local s={}
   for k,v in pairs(t) do
     s[v]=k
   end
   return s
end

-- Data for tools
local function toolsList(e)
    log_tool({"Name", "Quality", "Type", "Origin", "Icon"})
    for tool in tes3.iterateObjects(tes3.objectType.apparatus) do
        local tooltypename = ""
        if tool.type == 0 then
            tooltypename = "Mortar and Pestle"
        elseif tool.type == 1 then
            tooltypename = "Alembic"
        elseif tool.type == 2 then
            tooltypename = "Calcinator"
        elseif tool.type == 3 then
            tooltypename = "Retort"
        end
        local origin = tool.sourceMod
        if origin == "Morrowind.esm" then
            origin = "Base"
        elseif origin == "Bloodmoon.esm" then
            origin = "Base"
        elseif origin == "Tribunal.esm" then
            origin = "Base"
        elseif origin == "Tamriel_Data.esm" then
            origin = "Tamriel Data"
        elseif origin == "TR_Mainland.esm" then
            origin = "Tamriel Rebuilt"
        elseif origin == "Cyr_Main.esm" then
            origin = "Cyrodiil"
        elseif origin == "Sky_Main.esm" then
            origin = "Skyrim"
        end
        local toolquality = tool.quality
        toolquality = math.floor(toolquality*100 + 0.5)/100
        local tool_data = {tool.name, toolquality, tooltypename, origin, tool.icon}
        log_tool(tool_data)
    end
end

-- Credit: https://shinyu.org/en/lua/strings/capitalizing-a-string/
local function capitalize(word)
    return word:sub(1,1):upper() .. word:sub(2):lower()
end

local ing_table = {
    cureCommonDisease = "Cure Common Disease",
    cureParalyzation = "Cure Paralyzation",
    curePoison = "Cure Poison",
    damageagility = "Damage Agility",
    damageendurance = "Damage Endurance",
    damageintelligence = "Damage Intelligence",
    damageluck = "Damage Luck",
    damagepersonality = "Damage Personality",
    damagespeed = "Damage Speed",
    damagestrength = "Damage Strength",
    damagewillpower = "Damage Willpower",
    damageFatigue = "Damage Fatigue",
    damageHealth = "Damage Health",
    damageMagicka = "Damage Magicka",
    detectAnimal = "Detect Animal",
    detectEnchantment = "Detect Enchantment",
    detectKey = "Detect Key",
    drainagility = "Drain Agility",
    drainalteration = "Drain Alteration",
    drainendurance = "Drain Endurance",
    drainintelligence = "Drain Intelligence",
    drainluck = "Drain Luck",
    drainpersonality = "Drain Personality",
    drainsneak = "Drain Sneak",
    drainspeed = "Drain Speed",
    drainstrength = "Drain Strength",
    drainwillpower = "Drain Willpower",
    drainFatigue = "Drain Fatigue",
    drainHealth = "Drain Health",
    drainMagicka = "Drain Magicka",
    fireDamage = "Fire Damage",
    fireShield = "Fire Shield",
    fortifyagility = "Fortify Agility",
    fortifyalchemy = "Fortify Alchemy",
    fortifyendurance = "Fortify Endurance",
    fortifyintelligence = "Fortify Intelligence",
    fortifyluck = "Fortify Luck",
    fortifypersonality = "Fortify Personality",
    fortifyspeechcraft = "Fortify Speechcraft",
    fortifyspeed = "Fortify Speed",
    fortifystrength = "Fortify Strength",
    fortifywillpower = "Fortify Willpower",
    fortifyFatigue = "Fortify Fatigue",
    fortifyHealth = "Fortify Health",
    fortifyMagicka = "Fortify Magicka",
    frostDamage = "Frost Damage",
    frostShield = "Frost Shield",    
    lightningShield = "Lightning Shield",
    nightEye = "Night Eye",
    resistCommonDisease = "Resist Common Disease",
    resistFire = "Resist Fire",
    resistFrost = "Resist Frost",
    resistMagicka = "Resist Magicka",
    resistNormalWeapons = "Resist Normal Weapons",
    resistParalysis = "Resist Paralysis",
    resistPoison = "Resist Poison",
    resistShock = "Resist Shock",
    restoreagility = "Restore Agility",
    restoreendurance = "Restore Endurance",
    restoreintelligence = "Restore Intelligence",
    restoreluck = "Restore Luck",
    restorepersonality = "Restore Personality",
    restorespeed = "Restore Speed",
    restorestrength = "Restore Strength",
    restorewillpower = "Restore Willpower",
    restoreFatigue = "Restore Fatigue",
    restoreHealth = "Restore Health",
    restoreMagicka = "Restore Magicka",
    shockDamage = "Shock Damage",
    spellAbsorption = "Spell Absorption",
    swiftSwim = "Swift Swim",
    waterBreathing = "Water Breathing",
    waterWalking = "Water Walking",
    weaknesstoCommonDisease = "Weakness to Common Disease",
    weaknesstoFire = "Weakness to Fire",
    weaknesstoFrost = "Weakness to Frost",
    weaknesstoMagicka = "Weakness to Magicka",
    weaknesstoNormalWeapons = "Weakness to Normal Weapons",
    weaknesstoPoison = "Weakness to Poison",
    weaknesstoShock = "Weakness to Shock",
    cureBlightDisease = "Cure Blight Disease",
    divineIntervention = "Divine Intervention",
    fortifyathletics = "Fortify Athletics",
    fortifyAttack = "Fortify Attack",
    fortifylightArmor = "Fortify Light Armor",
    fortifyunarmored = "Fortify Unarmored",
    restoredestruction = "Restore Destruction",
    stuntedMagicka = "Stunted Magicka",
    disintegrateArmor = "Disintegrate Armor",
    disintegrateWeapon = "Disintegrate Weapon",
    drainmysticism = "Drain Mysticism",
    fortifyacrobatics = "Fortify Acrobatics",
    fortifyconjuration = "Fortify Conjuration",
    fortifymarksman = "Fortify Marksman",
    fortifyMaximumMagicka = "Fortify Maximum Magicka",
    fortifyrestoration = "Fortify Restoration",
    resistBlightDisease = "Resist Blight Disease",
    restorerestoration = "Restore Restoration",
    restorespeechcraft = "Restore Speechcraft",
    fortifybluntWeapon = "Fortify Blunt Weapon",
    fortifymysticism = "Fortify Mysticism",
    restoreathletics = "Restore Athletics",
    summonScamp = "Summon Scamp"
}

-- Data for Ingredients
-- Problem: How do we determine if the ingredient is from
-- the Mainland, Skyrim, or Cyrodiil? (and unique/special/quest/cursed)
local function ingredientsList(e)
    log_ingre({"ID", "Name", "Weight", "Value", "Origin", "Icon", "Effect 1", "Effect 2", "Effect 3", "Effect 4"})
    for ing in tes3.iterateObjects(tes3.objectType.ingredient) do
        local name = ing.name
        local origin = ing.sourceMod
        if origin == "Morrowind.esm" then
            origin = "Base"
        elseif origin == "Bloodmoon.esm" then
            origin = "Bloodmoon"
        elseif origin == "Tribunal.esm" then
            origin = "Tribunal"
        elseif origin == "Tamriel_Data.esm" then
            origin = "Tamriel Data"
            if ing.icon:sub(1,2):lower() == "pc" then
                origin = "Cyrodiil"
            elseif ing.icon:sub(1,2):lower() == "pi" then
                origin = "Cyrodiil"
            elseif ing.icon:sub(1,3):lower() == "sky" then
                origin = "Skyrim"
            elseif ing.icon:sub(1,2):lower() == "tr" then
                origin = "Tamriel Rebuilt"
            end
        elseif origin == "TR_Mainland.esm" then
            origin = "Tamriel Rebuilt Special"
            name = name .. " (Quest)"
        elseif origin == "Cyr_Main.esm" then
            origin = "Cyrodiil Special"
            name = name .. " (Quest)"
        elseif origin == "Sky_Main.esm" then
            origin = "Skyrim Special"
            name = name .. " (Quest)"
        end
        if ing.script and string.sub(origin, -7) ~= "Special" then
            origin = origin .. " Special"
            name = name .. " (Cursed)"
        end
        local ingweight = math.floor(ing.weight*1000 + 1/2)/1000
        local numToName = table_invert(tes3.effect)
        local attToName = table_invert(tes3.attribute)
        local skiToName = table_invert(tes3.skill)
        local effectArray = {}
        for index, effect in ipairs(ing.effects) do
            if effect ~= -1 then
                local effectName = ""
                local effectAttributeName = ""
                local effectSkillName = ""
                effectName = numToName[effect]
                if string.sub(effectName, -9) == "Attribute" then
                    local effectAttribute = ing.effectAttributeIds[index]
                    effectAttributeName = attToName[effectAttribute]
                    effectName = string.sub(effectName, 1, -10) .. effectAttributeName
                elseif string.sub(effectName, -5) == "Skill" then
                    local effectSkill = ing.effectSkillIds[index]
                    effectSkillName = skiToName[effectSkill]
                    effectName = string.sub(effectName, 1, -6) .. effectSkillName
                end
                effectArray[index] = ing_table[effectName] or capitalize(effectName) or effectName .. " ???"
            else
                effectArray[index] = ""
            end
        end
        local ingre_data = {ing.id, name, ingweight, ing.value, origin, ing.icon, effectArray[1], effectArray[2], effectArray[3] , effectArray[4]}
        log_ingre(ingre_data)
    end
end

--- This is a generic iterator function that is used
--- to loop over all the items in an inventory
---@param actor tes3actor
---@return fun(): tes3item, integer, tes3itemData|nil
local function iterItems(actor)
    local function iterator()
        for _, stack in pairs(actor.inventory) do
            local item = stack.object
            -- Skip uncarryable lights. They are hidden from the interface. A MWSE mod
            -- could make the player glow from transferring such lights, which the player
            -- can't remove. Some creatures like atronaches have uncarryable lights
            -- in their inventory to make them glow that are not supposed to be looted.
            if item.canCarry == false then
                goto continue
            end

            local count = stack.count

            -- First yield stacks with custom data
            for _, data in pairs(stack.variables or {}) do
                coroutine.yield(item, data.count, data)
                count = count - data.count
            end

            -- Then yield all the remaining copies
            if count ~= 0 then
                coroutine.yield(item, count)
            end

            :: continue ::
        end
    end
    return coroutine.wrap(iterator)
end

local function allLevelLayersContainer(t, container, count)
    for _, l in pairs(t) do
        if l.list then
            allLevelLayersContainer(l.list)
        elseif l.object.objectType == tes3.objectType.ingredient then
            local data = {container.id, container.name, l.object.id, count}
            if container.organic then
                log_flo(data)
            else
                log_con(data)
            end
        end
    end
end

-- Data for Flora (and non-organic containers?)
local function floraList(e)
    log_flo({"ID", "Name", "Ingredient", "Count"})
    log_con({"ID", "Name", "Ingredient", "Count"})
    for container in tes3.iterateObjects(tes3.objectType.container) do
        for item, count, itemData in iterItems(container) do
            local flo_data = {}
            if item.list then
                allLevelLayersContainer(item.list, container, count)
            elseif item.objectType == tes3.objectType.ingredient then
                flo_data = {container.id, container.name, item.id, count}
                if container.organic then
                    log_flo(flo_data)
                else
                    log_con(flo_data)
                end
            end
        end
    end
end

-- Data for Fauna
local function faunaList(e)
    log_cre({"ID", "Name", "Ingredient", "Count"})
    for creature in tes3.iterateObjects(tes3.objectType.creature) do
        for item, count, itemData in iterItems(creature) do
            local cre_data = {}
            if item.list then
                for _, l in pairs(item.list) do
                    if l.object.objectType == tes3.objectType.ingredient then
                        cre_data = {creature.id, creature.name, l.object.id, count}
                        log_cre(cre_data)
                    end
                end
            elseif item.objectType == tes3.objectType.ingredient then
                cre_data = {creature.id, creature.name, item.id, count}
                log_cre(cre_data)
            end
        end
    end
end

local esms = {
    "Morrowind.esm",
    "Sky_Main.esm",
    "Cyr_Main.esm",
    "TR_Mainland.esm",
    "Bloodmoon.esm",
    "Tribunal.esm",
}

local esms_rev = table_invert(esms)

local function allLevelLayers(t, origin, cell, gridx, gridy)
    for _, l in pairs(t.object.list) do
        -- Could just do l.object.list
        if l.object.objectType == tes3.objectType.leveledCreature then
            allLevelLayers(l, origin, cell, gridx, gridy)
        else
            log_cre_l({l.object.id, origin, cell.displayName, gridx, gridy, cell.isInterior})
        end
    end
end

-- Data for Flora, Fauna, loose samples, and container locations
-- Need to rerun for exterior vvardenfell cells for leveled creatures vs normal creatures
local function cellLooper(e)
    log_flo({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_cre({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_cre_l({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_con({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_loo({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    local objecttypes = {
        tes3.objectType.creature,
        tes3.objectType.leveledCreature,
        tes3.objectType.container,
        tes3.objectType.ingredient
    }
    local count = 0
    for k, cell in pairs(tes3.dataHandler.nonDynamicData.cells) do
        if cell.sourceMod == "TR_Mainland.esm" and cell.isInterior then
            -- count = count + 1
            -- if count > 10 then
            --     break
            -- end
            local gridx = nil
            local gridy = nil
            if cell.isInterior then
                tes3.positionCell{cell=cell, position={x=0,y=0,z=0}}
                local vec = tes3.getClosestExteriorPosition()
                if vec then
                    gridx = vec.x/8192
                    gridy = vec.y/8192
                end
            else
                tes3.positionCell{cell=cell, position={x=(cell.gridX+0.5)*8192,y=(cell.gridY+0.5)*8192}}
            end
            for object in cell:iterateReferences(objecttypes) do
                local origin = object.sourceMod
                if not cell.isInterior then
                    gridx = object.position.x/8192
                    gridy = object.position.y/8192
                end
                if object.object.objectType == tes3.objectType.leveledCreature then
                    allLevelLayers(object, origin, cell, gridx, gridy)
                elseif object.object.objectType == tes3.objectType.creature then
                    if not object.isLeveledSpawn then
                        log_cre({object.baseObject.id, origin, cell.displayName, gridx, gridy, cell.isInterior})
                    end
                elseif object.object.objectType == tes3.objectType.container then
                    if not object.object.organic then
                        log_con({object.id, origin, cell.displayName, gridx, gridy, cell.isInterior})
                    else
                        log_flo({object.id, origin, cell.displayName, gridx,  gridy, cell.isInterior})
                    end
                elseif object.object.objectType == tes3.objectType.ingredient then
                    log_loo({object.id, origin, cell.displayName, gridx, gridy, cell.isInterior})
                end
            end
        end
    end
end

-- Check if value in table
local function has_value (tab, val)
    for index, value in ipairs(tab) do
        if value == val then
            return true
        end
    end
    return false
end

-- Table of NPCs who can sell ingredients but are unused
local unusedNPCs = {
    "ather belden",
    "Dirver Relas",
    "TR_m1_O_Rinma",
    "TR_m3_Ilmyna Adas",
    "TR_m3_Llaynor Seryon",
    "TR_m3_Murletta Jarontus",
    "TR_m3_Raynila Indrano",
    "TR_m3_Satheri Dralam",
    "TR_m3_Sovos Ramalor",
    "TR_m3_Varn",
    "TR_m7_Dro'Dar",
}

-- Get NPC's, who sell ingredients, location and what they sell

local listofplaces = {
    "Ald-ruhn, Guild of Mages",
    "Gnisis, Fort Darius",
    "Gnisis, Fort Darius",
    "Gnisis, Temple",
    "Gnisis, Temple",
    "Pelagiad, Fort Pelagiad",
    "Ald-ruhn, Guls Llervu's House",
    "Balmora, Guild of Mages",
    "Sadrith Mora, Thervul Serethi: Healer",
    "Sadrith Mora, Anis Seloth: Alchemist",
    "Sadrith Mora, Pierlette Rostorard: Apothecary",
    "Sadrith Mora, Wolverine Hall: Mage's Guild",
    "Sadrith Mora, Wolverine Hall: Imperial Shrine",
    "Sadrith Mora, Wolverine Hall: Imperial Shrine",
    "Buckmoth Legion Fort, Interior",
    "Buckmoth Legion Fort, Interior",
    "Buckmoth Legion Fort, Interior",
    "Moonmoth Legion Fort, Interior",
    "Moonmoth Legion Fort, Interior",
    "Balmora, Nalcarya of White Haven: Fine Alchemist",
    "Ald-ruhn, Temple",
    "Ebonheart, Six Fishes",
    "Vivec, Andilu Drothan: Alchemist",
    "Vivec, Aurane Frernis: Apothecary",
    "Caldera, Guild of Mages",
    "Tel Vos, Services Tower",
    "Vivec, Redoran Temple Shrine",
    "Tel Aruhn, Tower Entry",
    "Tel Aruhn, Tower Living Quarters",
    "Tel Aruhn, Tower Entry",
    "Tel Aruhn, Bildren Areleth: Apothecary",
    "Tel Branora, Upper Tower: Therana's Chamber",
    "Tel Mora, Jolda: Apothecary",
    "Holamayan Monastery",
    "Tel Mora, Lower Tower",
    "Vos, Vos Chapel",
    "Vivec, Telvanni Apothecary",
    "Tel Vos, Services Tower",
    "Vivec, Guild of Mages",
    "Vivec, J'Rasha: Healer",
    "Maar Gan, Shrine",
    "Maar Gan, Outpost",
    "Vivec, Hlaalu Alchemist",
    "Vivec, Telvanni Alchemist",
    "Vivec, St. Olms Temple",
    "Balmora, Temple",
    "Balmora, Temple",
    "Balmora, Temple",
    "Balmora, Temple",
    "Ald-ruhn, Temple",
    "Ald-ruhn, Temple",
    "Seyda Neen, Arrille's Tradehouse",
    "Raven Rock, Bar",
    "Mournhold Temple: Infirmary",
    "Mournhold, Temple Courtyard",
    "Mournhold, The Winged Guar",
    "Anvil, Abecean Trading Company: Lower Floors",
    "Fort Heath, Iron Man Tavern",
    "Anvil, Bespoke Perfumes, Potions, and Elixirs",
    "Brina Cross, White Scarab Company",
    "Fort Heath, Chapel Tower",
    "Brina Cross, Crossing Inn",
    "Charach, Plaza Taverna",
    "Anvil, East Empire Company",
    "Anvil, Marina",
    "Brina Cross, North Wind Traders",
    "Anvil, Sailor's Fluke: Fight Pit",
    "Charach, Old Seawater Inn",
    "Anvil, Sailor's Fluke",
    "Archad, Kathrelor: General Goods",
    "Anvil, The Anchor's Rest",
    "Brina Cross, Mandilaron Sundries",
    "Fort Heath, General Quarters",
    "Brina Cross, Chapel of Crimson Strings",
    "Strident Coast Region",
    "Anvil, All Flags Inn",
    "Thresvy, The Blind Watchtower",
    "Marav, Philus Verius: Trader",
    "Anvil, Bazaar of the Abecean",
    "Anvil, Bazaar of the Abecean",
    "Charach, Sunset Hotel",
    "Thresvy, Chapel of Persisting Sustenance",
    "Brennan Bluffs Region",
    "Druadach Highlands Region",
    "Dragonstar West, Nukra-Tikil Tavern",
    "Haimtir, Jhorcian's Tradehouse",
    "Karthgad, Ywain: Trader",
    "Karthwasten, The Dancing Saber: Den",
    "Karthwasten, Bazaar",
    "Karthwasten, Lelena Aurtius: Baker",
    "Hoota's Cabin",
    "Dragonstar East",
    "Dragonstar East, Ildgar's Alehouse",
    "Dragonstar East, Abandoned Manor",
    "Karthwasten, Guild of Mages",
    "Karthwasten, Rianard Bauvrise: Alchemist",
    "Karthwasten, The Droopy Mare",
    "Firemoth Legion Fort",
    "Firemoth Legion Fort, Keep",
    "Firewatch, Beleth Bakery",
    "Sadas Plantation, Tel Sadas",
    "Bahrammu, Elammu Andrani: Trader",
    "Port Telvannis, Ferala Aranith's House",
    "Bahrammu",
    "Ranyon-ruhn, Irele Nathryon: Alchemist",
    "Nivalis, Jana Livia: Trader",
    "Firewatch, Beleth Bakery",
    "Tel Ouada, The Magic Mudcrab",
    "Firewatch, Dustmoth Legion Garrison: East Tower",
    "Port Telvannis, Tel Thenim: Lower Tower",
    "Molag Ruhn Region",
    "The Inn Between",
    "Akamora, Mines",
    "Helnim, Chapel of Kynareth",
    "Alt Bosara, Tel Vaerin",
    "Alt Bosara, Fevras Beran's General Supplies",
    "Hlersis, The Leaking Spore",
    "Akamora, Parys Manor",
    "Marog, Market",
    "Seherbal Camp, Wise Woman's Yurt",
    "Andar Mok, Andalas Tradehouse",
    "Pedivur's Tower",
    "Akamora, Guild of Mages",
    "Akamora, Underground Bazaar",
    "Akamora, Underground Bazaar",
    "Acre of Saint Meris",
    "Akamora, Parys Manor",
    "Helnim, Chapel of Kynareth",
    "Tel Gilan, The Cliff Racer's Rest",
    "Molag Ruhn Region",
    "Enamor Dayn, Tradehouse",
    "Old Ebonheart, Guild of Mages: Basement",
    "Aanthirin Region",
    "Almas Thirr, Temple",
    "Almas Thirr",
    "Almas Thirr, Infirmary of St. Meris",
    "Gorne, Bariel: Florist",
    "Dondril",
    "Old Ebonheart, The Mother Alessia",
    "Almas Thirr, Guild of Mages",
    "Darvonis, The Windbreak Hostel",
    "Old Ebonheart",
    "Almas Thirr, Darane Navur: Trader",
    "Aimrah, The Sailors' Inn",
    "Almas Thirr",
    "Vhul",
    "Roa Dyr",
    "Gorne, The Emerald Haven Inn",
    "Aimrah",
    "Bisandryon, Gardens",
    "Almas Thirr, Temple",
    "Old Ebonheart, Emaroc Harquart's Baked Goods",
    "Old Ebonheart, Emercius' Quality Wares",
    "Vhul, Falas Othril's House",
    "Fort Umbermoth, Interior",
    "Almas Thirr, Galran Darvu: Alchemist",
    "Sailen, Golveso Darys: Pawnbroker",
    "Vhul, Bakers' Hall",
    "Old Ebonheart, Gul-Ei's Pantry",
    "Vhul",
    "Almas Thirr, Underworks",
    "Felms Ithul, Jalyin's House",
    "Old Ebonheart, The Salty Futtocks",
    "Old Ebonheart, Kassad: Herbalist",
    "Bosmora",
    "Vhul, Temple",
    "Old Ebonheart",
    "Darvonis, Fari Niernis: Trader",
    "Seitur, Manus: Trader",
    "Vhul, The Howling Hound",
    "Gorne, Methalas Eves: General Trader",
    "Bosmora, Marketplace",
    "Velonith, Mudera's House",
    "Old Ebonheart, Narusya's Fine Potions",
    "Old Ebonheart, Grand Chapel of Talos: Towers",
    "Aimrah",
    "Almas Thirr, The Pious Pirate",
    "Old Ebonheart",
    "Felms Ithul, Thelin Drinith's House",
    "Old Ebonheart",
    "Ebon Tower, Legion: Headquarters",
    "Old Ebonheart, Unaarie's Elixirs",
    "Old Ebonheart, The Moth and Tiger",
    "Almas Thirr",
    "Gorne, Tribunal Chapel",
    "Almas Thirr, Thirsty Saint Cornerclub",
    "Old Ebonheart, Anjzhirra's Rare Goods",
    "Bal Foyen, Brewers and Fishmongers Hall",
    "Bal Foyen, Chapel of Mara",
    "Teyn, Cirifae's Tradehouse",
    "Volenfaryon, Thaar Hut",
    "Monastery of St. Aralor, Abbey",
    "Bal Foyen, Chapel of Mara",
    "Bal Foyen, Guild of Mages",
    "Bal Foyen, Docks",
    "The Grey Lodge",
    "Bal Foyen, Fauler's Philters",
    "The Grey Lodge",
    "Menaan",
    "Omaynis, The Kwama's Scuttle",
    "Omaynis, Egg Mine",
    "Bal Foyen, Nevusa Falen: Alchemist",
    "Bal Foyen, Chapel of Mara",
    "Ushu-Kur Mine, Company Office",
    "Omaynis, Egg Mine",
    "Indal-ruhn, Rolis Hlor: Trader",
    "Monastery of St. Felms, Infirmary",
    "Arvud, Lucky Shalaasa's Caravanserai",
    "Ishanuran Camp, Trehaddi's Yurt",
    "Ald Balaal, Shrine",
    "Ernabapalit Camp, Yakasamshi's Yurt",
    "Fort Ancylis, Main Keep",
    "Coronati Basin Region",
    "Shipal-Sharai, Adavas Faryon: General Goods",
    "Narsis, Market Quarter",
    "Coronati Basin Region",
    "Hlan Oek",
    "Hlerynhul, Annalina Conrel: Jeweler",
    "Shipal-Sharai, House of Red Wings",
    "Narsis, Market Quarter",
    "Narsis, Chapel of Zenithar",
    "Ald Iuval, Morag Tong Guildhall",
    "Narsis, Sewers: Grand Bazaar",
    "Narsis, Sewers: Grand Bazaar",
    "Narsis, Sewers: Grand Bazaar",
    "Ald Khan, Outer Halls",
    "Narsis, Belvin Uvalas: Healer",
    "Narsis, Foreign Quarter",
    "Shipal-Sharai, Caravanserai",
    "Othmura, Temple",
    "Idathren, Sadri's Cornerclub",
    "Hlerynhul, Dithisi Andral: Alchemist",
    "Hlerynhul",
    "Narsis, Market Quarter",
    "Narsis, Domican Vitresius: Alchemist",
    "Narsis, Council Quarter",
    "Hlerynhul, Temple",
    "Ald Iuval, Draren Oril's Tent",
    "Shipal-Sharai, Avilo's Gems and Metals",
    "Narsis, St. Veloth Quarter",
    "Yandaran, Scouts' Dome",
    "Narsis, Grand Bazaar: Underground",
    "Ald Marak, Elval Tradehouse",
    "Narsis, The Fortuna",
    "Othreleth Woods Region",
    "Coronati Basin Region",
    "Hlan Oek, Temple",
    "Gan-Ettu Camp, Gabezu's Tent",
    "Narsis, Grand Bazaar",
    "Narsis, Brevur Heights",
    "Narsis, Council Quarter",
    "Narsis, Council Quarter",
    "Narsis, Grand Bazaar: Underground",
    "Coronati Basin Region",
    "Narsis, Tanners and Miners Hall",
    "Uddanu, Laboratory",
    "Narsis, Arena",
    "Narsis, Irusa Sanys: Alchemist",
    "Ald Iuval, Issa Favelnim's Tent",
    "Coronati Basin Region",
    "Othmura, Jorna Amber-Throat: Trader",
    "Yandaran, Lower Level",
    "Hlerynhul, The Musty Mudcrab",
    "Narsis, Redwater Theater",
    "Narsis, The Hackle-Lounge",
    "Hlan Oek, Lantern's Depot",
    "Narsis, Brewers and Fishmongers Hall",
    "Hlerynhul, Linriah: Clothier",
    "Narsis, Lladres Sadreno: Fine Foods",
    "Ald Marak, Elval Tradehouse",
    "Shipal-Sharai, Sapphire Slouch Cornerclub",
    "Narsis, The Merchant's Purse",
    "Narsis, The Purple Lantern",
    "Hlerynhul, Chapel of Dibella",
    "Narsis, Maynas Thilarvel: Pawnbroker",
    "Narsis, Meer-Ei's Swim Shop",
    "Othmura, Muck-Raker's Hangout",
    "Hlerynhul, Myron Rothalen: Fine Outfitter",
    "Coronati Basin Region",
    "Hlerynhul, Farmers and Laborers Hall",
    "Narsis, Brevur Heights",
    "Hlan Oek, Temple",
    "Othmura",
    "Antirrhinum: Cabin",
    "Septim's Gate Pass, Main Keep",
    "Narsis, Council Quarter",
    "Hlan Oek, Morning Sun Cornerclub",
    "Ussiran Camp, Communal Tent",
    "Narsis, Rogeed: Hunter",
    "Gathram Farmhouse",
    "Shipal-Sharai, Rugalmil: Apothecary",
    "Narsis, Brevur Heights",
    "Hlerynhul, Vermilion Hound Cornerclub",
    "Narsis, Market Quarter",
    "Narsis, Sabia Bechand: Trader",
    "Narsis, Saenus Dibuntus: Western Imports",
    "Maar-Bani Crossing, Tradehouse",
    "Narsis, Bakers and Distillers Hall",
    "Adavrin Plantation",
    "Narsis, Furnishers and Caravaners Hall",
    "Shipal-Sharai",
    "Hunza Camp, Shairan's Tent",
    "Narsis, Grand Bazaar: Underground",
    "Narsis, Morag Tong Guildhall: Basement",
    "Narsis, Foreign Quarter",
    "Narsis, Bakers and Distillers Hall",
    "Sadrathim, Terenu Aryon: Trader",
    "Narsis, Backwater Cornerclub",
    "Narsis, Sewers: Market Quarter West",
    "Stormgate Pass, The Saxhleel Balladeer",
    "Narsis, Ulveni Salavel: Armorer",
    "Narsis, Canyon Air Inn",
    "Sadrathim, Chapel of Stendarr",
    "Narsis, Brewers and Fishmongers Hall",
    "Narsis, Tanners and Miners Hall",
    "Narsis, Grand Bazaar",
    "Othmura, High Wall Cornerclub",
    "Coronati Basin Region",
    "Narsis, The Fortuna: Private Rooms",
    "Narsis, Tailors and Dyers Hall",
    "Narsis, Sewers: Council Quarter Central",
    "Stormgate Pass, The Saxhleel Balladeer",
    "Sadrathim, Vulam's Net",
    "Narsis, Measurehall: Accomodations",
    "Narsis, Grand Bazaar",
    "Ussiran Camp, Communal Tent",
}

listofplaces = {
    {-120, -55},
    {-119, -54},
    {-119, -47},
    {-119, 11},
    {-113, 13},
    {-8, -11},
    {15, 26},
    {26, -5},
    {32, -11},
    {26, -3},
    {8, -26},
    {5, -28},
    {9, -22},
    {7, -19},
    {5, -28},
    {10, -24},
    {9, -27},
    {12, -34},
    {10, -24},
    {33, -30},
    {6, -19},
    {12, -34},
    {6, -19},
    {6, -19},
    {5, -28},
    {0, -16},
    {-3, -20},
    {8, -39},
    {5, -50},
    {3, -35},
    {2, -32},
    {5, -50},
    {7, -52},
    {0, -44},
    {5, -50},
    {6, -51},
    {6, -50},
    {-3, -31},
    {5, -41},
    {6, -51},
    {6, -51},
    {6, -39},
    {6, -40},
    {4, -37},
    {3, -39},
    {6, -51},
    {5, -51},
    {4, -56},
    {1, -50},
    {7, -52},
    {3, -35},
}

-- Need to get exact position. Combine with cell looper?
-- A mix of two different functions really, one for
-- exterior and one for interior cells :shrugs:
local function teleportForNPCs(e)
    for _, cellname in pairs(listofplaces) do
        local gridx = nil
        local gridy = nil
        tes3.positionCell({position={x=cellname[1]*8192, y=cellname[2]*8192, z=0}})
        -- tes3.positionCell({cell=cellname, position={x=0,y=0,z=0}})
        local cell = tes3.getPlayerCell()
        if cell.isInterior then
            local vec = tes3.getClosestExteriorPosition()
            if vec then
                gridx = vec.x/8192
                gridy = vec.y/8192
            end
            log_temp({cellname, gridx, gridy})
        else
            for object in cell:iterateReferences(tes3.objectType.npc) do
                if object.baseObject:tradesItemType(tes3.objectType.ingredient) then
                    local hasIngs = false
                    for item, count, itemData in iterItems(object.baseObject) do
                        if item.objectType == tes3.objectType.ingredient then
                            hasIngs = true
                            break
                        end
                    end
                    if hasIngs then
                        gridx = object.position.x/8192
                        gridy = object.position.y/8192
                        log_temp({object.baseObject.name, cellname, gridx, gridy})
                    end
                end
            end
        end
    end
end

local function getNPCLocations(e)
    log_npcs({"Name", "Origin", "CellName", "CellX", "CellY"})
    log_ing({"Name", "NPCName", "Count"})
    for npc in tes3.iterateObjects(tes3.objectType.npc) do
        if not has_value(unusedNPCs, npc.id) then
            if npc:tradesItemType(tes3.objectType.ingredient) then
                local npcObject = tes3.getReference(npc.id)
                local cell = npcObject.cell
                local gridx = nil
                local gridy = nil
                if not cell.isInterior then
                    gridx = cell.gridX
                    gridy = cell.gridY
                end
                local origin = npc.sourceMod
                if origin == "Morrowind.esm" then
                    origin = "Base"
                elseif origin == "Bloodmoon.esm" then
                    origin = "Bloodmoon"
                elseif origin == "Tribunal.esm" then
                    origin = "Tribunal"
                elseif origin == "Tamriel_Data.esm" then
                    origin = "Tamriel Data"
                elseif origin == "TR_Mainland.esm" then
                    origin = "Tamriel Rebuilt"
                elseif origin == "Cyr_Main.esm" then
                    origin = "Cyrodiil"
                elseif origin == "Sky_Main.esm" then
                    origin = "Skyrim"
                end
                local npc_data = {npc.name, origin, cell.displayName, gridx, gridy}
                local ing_data = {}
                for item, count, itemData in iterItems(npc) do
                    if item.objectType == tes3.objectType.ingredient then
                        ing_data = {item.id, npc.name, count}
                        log_ing(ing_data)
                    end
                end
                if next(ing_data) ~= nil then
                    log_npcs(npc_data)
                end
            end
        end
    end
end

-- This function loops over the references inside the
-- tes3referenceList and adds them to an array-style table
---@param list tes3referenceList
---@return tes3reference[]
local function referenceListToTable(list)
    local result = {}
    local i = 1
    if list.size == 0 then
        return {}
    end
    local ref = list.head

    while ref.nextNode do
        result[i] = ref
        i = i + 1
        ref = ref.nextNode
    end

    -- Add the last reference
    result[i] = ref

    return result
end

-- Data for effects (doesn't work)
-- Add manually instead
local function effectList(e)
    log_eff({"Spell Effects", "Base Cost", "Positive", "HasNoDuration", "HasNoMagnitude", "Icon"})
    for effect in tes3.iterateObjects(tes3.objectType.magicEffect) do
        log_eff(effect)
        log_eff({effect.name, effect.baseMagickaCost, not effect.isHarmful, effect.hasNoDuration, effect.hasNoMagnitude, effect.icon})
    end
end

-- Temp function for trying stuff out
local function testtest(e)
    local count = 0
    for _, cell in pairs(tes3.dataHandler.nonDynamicData.cells) do
        if not cell.isInterior then
            -- count = count + 1
            -- if count > 1000000000 then
            --     break
            -- end
            tes3.positionCell{cell=cell, position={x=0,y=0,z=0}}
            log_temp({cell.displayName, cell.gridX, cell.gridY})
        end
    end
end

-- Main
-- Problem: What about scripts that add stuff?
-- What about NPCs who drop ingredients?
-- What about leveled lists in containers (e.g. random_ingredient)
local function allOfThem(e)
    local combo = {mouseButton = 0, isAltDown = true, isControlDown = false, isShiftDown = false,}
    --[[
    if not tes3.isKeyEqual({ expected = combo, actual = e}) then
        return
    end
    --]]
    -- toolsList(e)
    -- getNPCLocations(e)
    -- ingredientsList(e)
    -- floraList(e)
    -- faunaList(e)
    -- effectList(e)
    cellLooper(e)
    -- testtest(e)
    -- teleportForNPCs(e)
end

-- Event to run the code
-- event.register(tes3.event.initialized, allOfThem)
event.register(tes3.event.mouseButtonDown, allOfThem)

-- Interior Cell Buffer=10 normal, 0 for map creation
-- Exterior Cell Buffer=32 normal, 0 for map creation
