-- This script is used to gather data from the game. The data gathered
-- is 'raw' and thus requires some edits before it is database ready.
-- It is made available for completeness, but using it is not advised
-- as the edits are not well documented. The usable data is supplied
-- as SQL files in the /database folder.
-- The basic flow is:
-- 1. Run these scripts
-- 2. Convert logs to csv files using Libreoffice Calc/Excel
-- 3. Convert csv files to sql using https://www.convertcsv.com/csv-to-sql.htm
local data = require("DataMine.data")

-- Create log for data
-- The log name includes the versions of Tamriel Data,
-- Tamriel Rebuilt, Project:Cyrodiil, and Project:Skyrim.
-- All the official plugins, except firemoth, are included,
-- and the GOTY edition is used.
-- No other mods (should) be included in this script's output.
local log_name = "TD 25.05 TR 25.05 Cyr 21.12a Sky 24.12b" -- <<< UPDATE THIS

-- List of names to differentiate database tables in the logs.
-- Probably a better way but oh well...
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

--#region Helper functions

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

-- Credit: https://shinyu.org/en/lua/strings/capitalizing-a-string/
local function capitalize(word)
    return word:sub(1,1):upper() .. word:sub(2):lower()
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

-- Recursively exhausts leveled lists in containers (e.g. lists within lists)
local function allLevelLayersContainer(t, container, count)
    for _, l in pairs(t) do
        if l.list then
            allLevelLayersContainer(l.list)
        elseif l.object.objectType == tes3.objectType.ingredient then
            local info = {container.id, container.name, l.object.id, count}
            if container.organic then
                log_flo(info)
            else
                log_con(info)
            end
        end
    end
end

-- Recursively exhauts leveled lists in lvl'd creatures (e.g. lists within lists)
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

-- Check if value in table
local function has_value (tab, val)
    for index, value in ipairs(tab) do
        if value == val then
            return true
        end
    end
    return false
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

--#endregion

--#region variables

local ing_table = data.ing_table
local esms = data.esms
local unusedNPCs = data.unusedNPCs
local listofplaces = data.listofplaces
local esms_rev = table_invert(esms)

--#endregion

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

-- Data for Ingredients
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
            -- elseif ing.icon:sub(1,2):lower() == "pi" then
            --     origin = "Cyrodiil"
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

-- Data for Flora, Fauna, loose samples, and container locations
-- Need to:
-- Add NPCs locations
-- Rerun all cells for creatures (not lvl'd creatures)
-- Find way to include ingredients added by scripts?
-- PROBLEM: Does this not collect *all* e.g. containers?
-- Shouldn't we only find ones in our containers list?
local function cellLooper(e, sourceMod, isInterior, gridxLower, gridxUpper)
    log_flo({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_cre({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_cre_l({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_con({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    log_loo({"ID", "Origin", "CellName", "CellX", "CellY", "IsInterior"})
    local objecttypes = {
        tes3.objectType.creature,
        tes3.objectType.leveledCreature,
        tes3.objectType.container,
        tes3.objectType.ingredient,
        -- tes3.objectType.npc
    }
    local count = 0
    for k, cell in pairs(tes3.dataHandler.nonDynamicData.cells) do
        if cell.sourceMod == sourceMod and (not cell.isInterior == not isInterior) and cell.gridX >= gridxLower and cell.gridX < gridxUpper then
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
                elseif object.object.objectType == tes3.objectType.npc then
                    -- Edit this to add NPC location logic
                end
            end
        end
    end
end

-- Get NPC locations.
-- Should move functionality into CellLooper
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

-- Get list of NPCs who sell ingredients
-- Should revisit with what to do about NPCs who have ingredients but
-- don't trade them, and move functionality into CellLooper and a new
-- function for ing->NPC (NPC->Cell goes in CellLooper)
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

-- Main
-- Use on a new game for best results.
-- Problem: What about scripts that add stuff?
-- What about NPCs who drop ingredients?
local function Looper(e)
    local combo = {mouseButton = 0, isAltDown = true, isControlDown = false, isShiftDown = false,}
    if not tes3.isKeyEqual({ expected = combo, actual = e}) then
        return
    end
    local sourceMod = "Tribunal.esm" -- <<< CHANGE THESE
    local isInterior = true -- <<<
    local gridxLower = -10000 -- <<<
    local gridxUpper = 10000 -- <<<
    cellLooper(e, sourceMod, isInterior, gridxLower, gridxUpper)
end

local function initData(e)
    toolsList(e)
    ingredientsList(e)
    floraList(e)
    faunaList(e)
    getNPCLocations(e)
end

-- Event to run the code
-- For code that does not require looping through cells
-- event.register(tes3.event.initialized, initData)
-- For code that *does* require looping through cells
-- event.register(tes3.event.mouseButtonDown, Looper)

-- Morrowind.ini settings for more stable CreateMap
-- Interior Cell Buffer=10 normal, 0 for map creation
-- Exterior Cell Buffer=32 normal, 0 for map creation
