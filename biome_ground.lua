file = GetString("file", "testground.png", "script png")
grassMap = GetString("grass", "", "script png")
heightScale = GetInt("scale", 64)
tileSize = GetInt("tilesize", 128)
hollow = GetInt("hollow", 0)
local biome = string.lower(GetString("biome", "default"))

function getDefaultGradient()
    return {
        black = {0.27, 0.34, 0.23},
        white = {0.45, 0.41, 0.26},
        endColor = {0.3, 0.45, 0.15}
    }
end

function getDesertGradient()
    return {
        black = {0.7, 0.6, 0.4},
        white = {0.9, 0.8, 0.6},
        endColor = {0.95, 0.85, 0.4}
    }
end

function getSnowyGradient()
    return {
        black = {0.85, 0.85, 0.85},
        white = {0.95, 0.95, 0.95},
        endColor = {1.0, 1.0, 1.0}
    }
end

function getSwampGradient()
    return {
        black = {0.1, 0.2, 0.1},
        white = {0.2, 0.3, 0.2},
        endColor = {0.3, 0.4, 0.3}
    }
end

function getForestGradient()
    return {
        black = {0.39608, 0.56078, 0.28627},  -- Forest green
        white = {0.55686, 0.74902, 0.38824},  -- Light green
        endColor = {0.35, 0.45, 0.2}         -- Shaded forest floor
    }
end

function getVolcanoGradient()
    return {
        black = {0.7, 0.0, 0.0},     -- Dark red
        white = {1.0, 0.3, 0.0},     -- Bright red
        endColor = {0.1, 0.0, 0.0}  -- Burnt lava black
    }
end

function getTundraGradient()
    return {
        black = {0.7, 0.8, 0.9},     -- Icy blue
        white = {0.95, 0.95, 1.0},   -- White-blue
        endColor = {0.9, 1.0, 1.0}  -- Bright icy surface
    }
end

function getAlienGradient()
    return {
        black = {0.1, 0.8, 0.1},     -- Alien green
        white = {0.5, 0.1, 0.5},     -- Purple
        endColor = {0.9, 0.0, 0.6}  -- 	Exotic bioluminescence
    }
end

function getCrystalGradient()
    return {
        black = {0.3, 0.6, 0.9},     -- Blue crystal
        white = {0.6, 0.3, 0.9},     -- Purple crystal
        endColor = {0.9, 0.6, 1.0}  -- Magical pastel sheen
    }
end

function getBeachGradient()
    return {
        black = {0.6, 0.8, 0.5},     
        white = {1.0, 1.0, 0.9},
        endColor = {0.7, 0.9, 0.6}  -- Soft green sea foam
    }
end

function getCoralGradient()
    return {
        black = {0.6, 0.8, 0.5},     -- Reef plants
        white = {1.0, 1.0, 0.9},     -- Seaweed
        endColor = {1.0, 0.7, 0.5}  -- Coral orange-pink
    }
end

function getSavannaGradient()
    return {
        black = {0.8, 0.7, 0.3},     -- Golden grass
        white = {0.6, 0.5, 0.3},     -- Dry earth
        endColor = {1.0, 0.9, 0.6}  -- 	Sunset savanna glow
    }
end

function getCanyonGradient()
    return {
        black = {0.8, 0.4, 0.2},     -- Red canyon
        white = {0.9, 0.6, 0.3},     -- Orange sandstone
        endColor = {1.0, 0.7, 0.5}  -- Rich terracotta fade
    }
end

function getMushroomGradient()
    return {
        black = {0.5, 0.3, 0.5},     -- Purple mushroom surface
        white = {0.8, 0.5, 0.8},     -- Light pink spores
        endColor = {0.3, 0.2, 0.3}  -- Fungal underbrush
    }
end

function getCaveGradient()
    return {
        black = {0.2, 0.2, 0.3},     -- Dark cave floor
        white = {0.4, 0.4, 0.5},     -- Cave moss
        endColor = {0.1, 0.1, 0.2}  -- Subsurface dark
    }
end

function getAlpineGradient()
    return {
        black = {0.4, 0.5, 0.3},     -- Alpine grass
        white = {0.7, 0.8, 0.7},     -- Rocky mountain surface
        endColor = {0.6, 0.7, 0.5}  -- Dusty green slope
    }
end

function getBambooGradient()
    return {
        black = {0.3, 0.5, 0.2},     -- Bamboo green
        white = {0.7, 0.8, 0.5},     -- Light bamboo
        endColor = {0.5, 0.6, 0.3}  -- Bamboo leaf green
    }
end

function getMeadowGradient()
    return {
        black = {0.5, 0.7, 0.3},     -- Lush meadow
        white = {0.9, 0.9, 0.6},     -- Wildflowers
        endColor = {0.95, 1.0, 0.8} -- Bright flower tip highlight
    }
end

function getIceGradient()
    return {
        black = {0.8, 0.9, 0.95},    -- Glacial ice
        white = {0.6, 0.7, 0.9},     -- Deep ice crevasse
        endColor = {0.7, 0.8, 1.0}  -- Polar shimmer
    }
end

function getJungleGradient()
    return {
        black = {0.1, 0.5, 0.1},     -- Dark jungle green
        white = {0.3, 0.7, 0.3},     -- Vibrant jungle foliage
        endColor = {0.2, 0.6, 0.2}  -- Shaded foliage base
    }
end

function getAshGradient()
    return {
        black = {0.3, 0.3, 0.3},     -- Ash gray
        white = {0.5, 0.5, 0.5},     -- Light ash
        endColor = {0.2, 0.2, 0.2}  -- Charcoal dust 
    }
end

function getMangroveGradient()
    return {
        black = {0.3, 0.4, 0.3},     -- Mangrove green
        white = {0.5, 0.4, 0.2},     -- Muddy water
        endColor = {0.4, 0.3, 0.2}  -- Mud-rich sediment
    }
end

function getCherryGradient()
    return {
        black = {0.3, 0.6, 0.3},     -- Green grass
        white = {0.9, 0.7, 0.8},     -- Cherry blossom pink
        endColor = {1.0, 0.8, 0.9}  -- Blush petals
    }
end

function getHighGradient()
    return {
        black = {0.3, 0.5, 0.3},     -- Highland grass
        white = {0.6, 0.6, 0.5},     -- Highland rock
        endColor = {0.4, 0.4, 0.3}  -- Rocky soil tone
    }
end

function getMesaGradient()
    return {
        black = {0.6, 0.3, 0.2},     -- Red mesa clay
        white = {0.9, 0.6, 0.4},     -- Light mesa surface
        endColor = {1.0, 0.8, 0.6}  -- Bright clay dust
    }
end

function getWasteGradient()
    return {
        black = {0.5, 0.5, 0.4},     -- Dead grass
        white = {0.6, 0.5, 0.4},     -- Dusty soil
        endColor = {0.3, 0.3, 0.2}  -- Barren cracked land
    }
end

function getTaigaGradient()
    return {
        black = {0.4, 0.5, 0.4},     -- Conifer green
        white = {0.6, 0.7, 0.5},     -- Forest floor
        endColor = {0.3, 0.4, 0.3}  -- Pine shadow
    }
end

function getCorruptionGradient()
    return {
        black = {0.4, 0.0, 0.6},     -- Deep purple corruption
        white = {0.8, 0.0, 1.0},     -- Bright magenta energy
        endColor = {0.6, 0.0, 0.9}  -- Dark magic
    }
end

function getCandyGradient()
    return {
        black = {0.9, 0.5, 0.9},     -- Cotton candy pink
        white = {0.5, 0.9, 1.0},     -- Blue raspberry
        endColor = {1.0, 1.0, 1.0}  -- Frosted sugar
    }
end

function getEtherealGradient()
    return {
        black = {0.6, 0.9, 1.0},     -- Light ethereal blue
        white = {1.0, 1.0, 0.8},     -- Glowing light
        endColor = {0.8, 0.6, 1.0}  -- Dreamy pastel purple
    }
end

function getCyberGradient()
    return {
        black = {0.0, 0.6, 0.9},     -- Neon blue
        white = {1.0, 0.0, 0.6},     -- Hot pink
        endColor = {0.2, 1.0, 1.0}  -- Electric cyan pulse
    }
end

function getCrimsonGradient()
    return {
        black = {1.0, 0.0, 0.0},     -- Deep blood red
        white = {0.7, 0.0, 0.0},     -- Fiery orange
        endColor = {0.4, 0.0, 0.0}  -- Blood-drenched red
    }
end

function getVaporGradient()
    return {
        black = {0.4, 0.0, 0.8},     -- Deep purple
        white = {0.0, 0.8, 0.8},     -- Teal/cyan
        endColor = {1.0, 0.7, 1.0}  -- Bubblegum nostalgia
    }
end

function getNeonGradient()
    return {
        black = {0.0, 1.0, 0.0},     -- Electric green
        white = {1.0, 1.0, 0.0},     -- Bright yellow
        endColor = {1.0, 0.0, 1.0}  -- Bright pink zap
    }
end

function getToxicGradient()
    return {
        black = {0.2, 0.8, 0.0},     -- Toxic green
        white = {0.9, 1.0, 0.0},     -- Radioactive yellow
        endColor = {0.1, 0.6, 0.0}  -- 	Oozing slime base
    }
end

function getGlitchGradient()
    return {
        black = {0.0, 0.0, 0.0},     -- Black void
        white = {1.0, 0.0, 1.0},     -- Hot magenta
        endColor = {0.0, 1.0, 1.0}  -- Broken cyan pixel flash
    }
end

function getUnderGradient()
    return {
        black = {0.2, 0.0, 0.3},     -- Deep underworld purple
        white = {0.5, 0.0, 0.8},     -- Glowing arcane energy
        endColor = {0.1, 0.0, 0.2}  -- Abyss shadow deep
    }
end

local gradientPresets = {
    default = getDefaultGradient,
    desert = getDesertGradient,
    snowy = getSnowyGradient,
    swamp = getSwampGradient,
    forest = getForestGradient,
    volcano = getVolcanoGradient,
    tundra = getTundraGradient,
    alienjungle = getAlienGradient,
    crystalfields = getCrystalGradient,
    beach = getBeachGradient,
    coralreef = getCoralGradient,
    savanna = getSavannaGradient,
    canyon = getCanyonGradient,
    mushroom = getMushroomGradient,
    cave = getCaveGradient,
    alpine = getAlpineGradient,
    bambooforest = getBambooGradient,
    meadow = getMeadowGradient,
    icelands = getIceGradient,
    jungle = getJungleGradient,
    ashlands = getAshGradient,
    mangrove = getMangroveGradient,
    cherry = getCherryGradient,
    highlands =  getHighGradient,
    mesa = getMesaGradient,
    wasteland = getWasteGradient,
    taiga = getTaigaGradient,
    corruption = getCorruptionGradient,
    candyland = getCandyGradient,
    ethereal = getEtherealGradient,
    cyberpunk = getCyberGradient,
    crimson = getCrimsonGradient,
    vaporwave = getVaporGradient,
    neon = getNeonGradient,
    toxic = getToxicGradient,
    glitch = getGlitchGradient,
    underdark = getUnderGradient
}

function init()

    DebugPrint("Biome: " .. biome)

    local biomeInitializers = {
        default = initDefault,
        desert = initDesert,
        snowy = initSnowy,
        swamp = initSwamp,
        forest = initForest,
        volcano = initVolcano,
        tundra = initTundra,
        alienjungle = initAlienJungle,
        crystalfields = initCrystalFields,
        beach = initBeach,
        coralreef = initCoralReef,
        savanna = initSavanna,
        canyon = initCanyon,
        mushroom = initMushroom,
        cave = initCave,
        alpine = initAlpine,
        bambooforest = initBambooForest,
        meadow = initMeadow,
        icelands = initIcelands,
        jungle = initJungle,
        ashlands = initAshlands,
        mangrove = initMangrove,
        cherry = initCherry,
        highlands = initHighlands,
        mesa = initMesa,
        wasteland = initWasteland,
        taiga = initTaiga,
        corruption = initCorruption,
        candyland = initCandyland,
        ethereal = initEthereal,
        cyberpunk = initCyberpunk,
        crimson = initCrimson,
        vaporwave = initVaporwave,
        neon = initNeon,
        toxic = initToxic,
        glitch = initGlitch,
        underdark = initUnderdark
    }

    local initializer = biomeInitializers[biome]
    if initializer then
        DebugPrint("Using initializer for biome: " .. biome)
        initializer()
    else
        DebugPrint("Unknown biome selected: " .. biome .. ", using default")
        initDefault()
    end

    -- Handle grassMap loading
    if grassMap == "" then
        LoadImage(file)
    else
        createGrassGradient()
        LoadImage(file, grassMap)
    end

    local w,h = GetImageSize()
    local maxSize = tileSize

    local y0 = 0
    while y0 < h-1 do
        local y1 = y0 + maxSize
        if y1 > h-1 then y1 = h-1 end

        local x0 = 0
        while x0 < w-1 do
            local x1 = x0 + maxSize
            if x1 > w-1 then x1 = w-1 end
            Vox(x0, 0, y0)
            Heightmap(x0, y0, x1, y1, heightScale)
            x0 = x1
        end
        y0 = y1
    end
end

DebugPrint("Using biome: " .. biome)
DebugPrint("Gradient preset: " .. tostring(gradientPresets[biome]))

function createGrassGradient()
    local preset = gradientPresets[biome] or getDefaultGradient
    local gradient = preset()

    local black = gradient.black
    local white = gradient.white
    local endColor = gradient.endColor

    for i = 1, 8 do
        local t = (i - 1) / 7.0
        local r, g, b

        if t < 0.5 then
            local t2 = t / 0.5
            r = black[1] * (1 - t2) + white[1] * t2
            g = black[2] * (1 - t2) + white[2] * t2
            b = black[3] * (1 - t2) + white[3] * t2
        else
            local t2 = (t - 0.5) / 0.5
            r = white[1] * (1 - t2) + endColor[1] * t2
            g = white[2] * (1 - t2) + endColor[2] * t2
            b = white[3] * (1 - t2) + endColor[3] * t2
        end

        CreateMaterial("unphysical", r, g, b, 1, 0, 0.2)
    end
end

function initDefault()
    CreateMaterial("rock", 0.41569, 0.40784, 0.37647)
    CreateMaterial("dirt", 0.34118, 0.30588, 0.25098, 1, 0, 0.1)
    CreateMaterial("unphysical", 0.27451, 0.34510, 0.23137, 1, 0, 0.2)
    CreateMaterial("unphysical", 0.28235, 0.38824, 0.22745, 1, 0, 0.2)
	CreateMaterial("unphysical", 0.3, 0.45, 0.15, 1, 0, 0.2)
    CreateMaterial("masonry", 0.39608, 0.39216, 0.38824, 1, 0, 0.4)

    -- Call to create grass gradient
    createGrassGradient()
end

function initDesert()
    CreateMaterial("rock", 0.8, 0.7, 0.5)
    CreateMaterial("dirt", 0.7, 0.6, 0.4, 1, 0, 0.1)
    CreateMaterial("unphysical", 0.9, 0.8, 0.6, 1, 0, 0.2)
    CreateMaterial("unphysical", 0.95, 0.85, 0.65, 1, 0, 0.2)
	CreateMaterial("unphysical", 0.95, 0.85, 0.4, 1, 0, 0.2)
    CreateMaterial("masonry", 0.6, 0.5, 0.4, 1, 0, 0.4)

    -- Call to create grass gradient
    createGrassGradient()
end

function initSnowy()
    CreateMaterial("rock", 0.7, 0.7, 0.8)
    CreateMaterial("dirt", 0.6, 0.6, 0.7, 1, 0, 0.1)
    CreateMaterial("unphysical", 0.9, 0.9, 1.0, 1, 0, 0.2)
    CreateMaterial("unphysical", 0.85, 0.85, 0.95, 1, 0, 0.2)
	CreateMaterial("unphysical", 0.8, 0.9, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.8, 0.8, 0.9, 1, 0, 0.4)

    -- Call to create grass gradient
    createGrassGradient()
end

function initSwamp()
    CreateMaterial("rock", 0.3, 0.4, 0.3)
    CreateMaterial("dirt", 0.2, 0.3, 0.2, 1, 0, 0.1)
    CreateMaterial("unphysical", 0.25, 0.35, 0.25, 1, 0, 0.2)
    CreateMaterial("unphysical", 0.3, 0.4, 0.3, 1, 0, 0.2)
	CreateMaterial("unphysical", 0.2, 0.3, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.3, 0.3, 0.3, 1, 0, 0.4)

    -- Call to create grass gradient
    createGrassGradient()
end

function initForest()
    CreateMaterial("rock", 0.37647, 0.54118, 0.32941) -- dark green rock
    CreateMaterial("dirt", 0.39608, 0.26667, 0.18824, 1, 0, 0.1) -- forest soil brown
    CreateMaterial("unphysical", 0.55686, 0.74902, 0.38824, 1, 0, 0.2) -- grass green
    CreateMaterial("unphysical", 0.39608, 0.56078, 0.28627, 1, 0, 0.2) -- forest leaves
	CreateMaterial("unphysical", 0.35, 0.45, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.3, 0.3, 0.3, 1, 0, 0.4) -- stone paths

    -- Call to create grass gradient
    createGrassGradient()
end

function initVolcano()
    CreateMaterial("rock", 0.5, 0.0, 0.0) -- blood rock
    CreateMaterial("dirt", 0.6, 0.1, 0.0, 1, 0, 0.1) -- crimson soil
    CreateMaterial("unphysical", 0.7, 0.0, 0.0, 1, 0, 0.2) -- deep blood red
    CreateMaterial("unphysical", 1.0, 0.3, 0.0, 1, 0, 0.2) -- fiery orange
	CreateMaterial("unphysical", 0.1, 0.0, 0.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.8, 0.2, 0.2, 1, 0, 0.4) -- crimson structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initTundra()
    CreateMaterial("rock", 0.7, 0.7, 0.8) -- icy rocks
    CreateMaterial("dirt", 0.9, 0.9, 0.9, 1, 0, 0.1) -- frozen snow dirt
    CreateMaterial("unphysical", 0.95, 0.95, 1.0, 1, 0, 0.2) -- snow
    CreateMaterial("unphysical", 0.7, 0.8, 0.9, 1, 0, 0.2) -- light ice
	CreateMaterial("unphysical", 0.9, 1.0, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.8, 0.8, 0.9, 1, 0, 0.4) -- frosty paths

    -- Call to create grass gradient
    createGrassGradient()
end

function initAlienJungle()
    CreateMaterial("rock", 0.4, 0.6, 0.2) -- alien rocks
    CreateMaterial("dirt", 0.2, 0.3, 0.1, 1, 0, 0.1) -- alien jungle dirt
    CreateMaterial("unphysical", 0.1, 0.8, 0.1, 1, 0, 0.2) -- glowing plants
    CreateMaterial("unphysical", 0.5, 0.1, 0.5, 1, 0, 0.2) -- glowing purple plants
	CreateMaterial("unphysical", 0.9, 0.0, 0.6, 1, 0, 0.2)
    CreateMaterial("masonry", 0.6, 0.6, 0.3, 1, 0, 0.4) -- alien stone  

    -- Call to create grass gradient
    createGrassGradient()
end

function initCrystalFields()
    CreateMaterial("rock", 0.5, 0.5, 1.0) -- blue crystals
    CreateMaterial("dirt", 0.8, 0.6, 1.0, 1, 0, 0.1) -- crystal dirt
    CreateMaterial("unphysical", 0.3, 0.6, 0.9, 1, 0, 0.2) -- light blue crystals
    CreateMaterial("unphysical", 0.6, 0.3, 0.9, 1, 0, 0.2) -- purple crystals
	CreateMaterial("unphysical", 0.9, 0.6, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.9, 0.7, 0.9, 1, 0, 0.4) -- sparkling paths

    -- Call to create grass gradient
    createGrassGradient()
end

function initBeach()
    CreateMaterial("rock", 0.8, 0.8, 0.5) -- light beach rocks
    CreateMaterial("dirt", 1.0, 0.9, 0.7, 1, 0, 0.1) -- light sand
    CreateMaterial("unphysical", 0.6, 0.8, 0.5, 1, 0, 0.2) -- beach grass
    CreateMaterial("unphysical", 0.2, 0.6, 0.9, 1, 0, 0.2) -- water-like color
	CreateMaterial("unphysical", 0.7, 0.9, 0.6, 1, 0, 0.2)
    CreateMaterial("masonry", 0.8, 0.8, 0.5, 1, 0, 0.4) -- driftwood

    -- Call to create grass gradient
    createGrassGradient()
end

function initCoralReef()
    CreateMaterial("rock", 0.3, 0.6, 0.7) -- coral rock
    CreateMaterial("dirt", 0.4, 0.7, 0.8, 1, 0, 0.1) -- sandy sea floor
    CreateMaterial("unphysical", 0.1, 0.5, 0.3, 1, 0, 0.2) -- deep reef plants
    CreateMaterial("unphysical", 1.0, 0.7, 0.1, 1, 0, 0.2) -- coral
	CreateMaterial("unphysical", 1.0, 0.7, 0.5, 1, 0, 0.2)
    CreateMaterial("masonry", 0.7, 0.7, 0.7, 1, 0, 0.4) -- reef rock

    -- Call to create grass gradient
    createGrassGradient()
end

function initSavanna()
    CreateMaterial("rock", 0.6, 0.5, 0.3) -- savanna rock
    CreateMaterial("dirt", 0.5, 0.4, 0.25, 1, 0, 0.1) -- dry earth
    CreateMaterial("unphysical", 0.8, 0.7, 0.3, 1, 0, 0.2) -- golden grass
    CreateMaterial("unphysical", 0.6, 0.5, 0.3, 1, 0, 0.2) -- dry brush
	CreateMaterial("unphysical", 1.0, 0.9, 0.6, 1, 0, 0.2)
    CreateMaterial("masonry", 0.7, 0.6, 0.4, 1, 0, 0.4) -- weathered stone

    -- Call to create grass gradient
    createGrassGradient()
end

function initCanyon()
    CreateMaterial("rock", 0.8, 0.4, 0.2) -- red canyon rock
    CreateMaterial("dirt", 0.7, 0.5, 0.3, 1, 0, 0.1) -- canyon soil
    CreateMaterial("unphysical", 0.9, 0.6, 0.3, 1, 0, 0.2) -- orange sandstone
    CreateMaterial("unphysical", 0.7, 0.4, 0.2, 1, 0, 0.2) -- red rock
	CreateMaterial("unphysical", 1.0, 0.7, 0.5, 1, 0, 0.2)
    CreateMaterial("masonry", 0.8, 0.5, 0.3, 1, 0, 0.4) -- striated rock layers

    -- Call to create grass gradient
    createGrassGradient()
end

function initMushroom()
    CreateMaterial("rock", 0.5, 0.4, 0.5) -- mushroom base rock
    CreateMaterial("dirt", 0.4, 0.3, 0.4, 1, 0, 0.1) -- dark mycelium dirt
    CreateMaterial("unphysical", 0.5, 0.3, 0.5, 1, 0, 0.2) -- purple mushroom surface
    CreateMaterial("unphysical", 0.8, 0.5, 0.8, 1, 0, 0.2) -- pink spores
	CreateMaterial("unphysical", 0.3, 0.2, 0.3, 1, 0, 0.2)
    CreateMaterial("masonry", 0.6, 0.4, 0.6, 1, 0, 0.4) -- mushroom stems

    -- Call to create grass gradient
    createGrassGradient()
end

function initCave()
    CreateMaterial("rock", 0.3, 0.3, 0.4) -- cave rock
    CreateMaterial("dirt", 0.2, 0.2, 0.3, 1, 0, 0.1) -- cave floor
    CreateMaterial("unphysical", 0.4, 0.4, 0.5, 1, 0, 0.2) -- cave moss
    CreateMaterial("unphysical", 0.2, 0.2, 0.3, 1, 0, 0.2) -- dark areas
	CreateMaterial("unphysical", 0.1, 0.1, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.5, 0.5, 0.6, 1, 0, 0.4) -- stalactites

    -- Call to create grass gradient
    createGrassGradient()
end

function initAlpine()
    CreateMaterial("rock", 0.6, 0.6, 0.6) -- alpine rock
    CreateMaterial("dirt", 0.5, 0.5, 0.4, 1, 0, 0.1) -- alpine soil
    CreateMaterial("unphysical", 0.4, 0.5, 0.3, 1, 0, 0.2) -- alpine grass
    CreateMaterial("unphysical", 0.7, 0.8, 0.7, 1, 0, 0.2) -- rocky mountain surface
	CreateMaterial("unphysical", 0.6, 0.7, 0.5, 1, 0, 0.2)
    CreateMaterial("masonry", 0.5, 0.5, 0.5, 1, 0, 0.4) -- mountain rock

    -- Call to create grass gradient
    createGrassGradient()
end

function initBambooForest()
    CreateMaterial("rock", 0.5, 0.6, 0.4) -- bamboo forest rock
    CreateMaterial("dirt", 0.4, 0.3, 0.2, 1, 0, 0.1) -- forest floor
    CreateMaterial("unphysical", 0.3, 0.5, 0.2, 1, 0, 0.2) -- bamboo green
    CreateMaterial("unphysical", 0.7, 0.8, 0.5, 1, 0, 0.2) -- light bamboo
	CreateMaterial("unphysical", 0.5, 0.6, 0.3, 1, 0, 0.2)
    CreateMaterial("masonry", 0.6, 0.7, 0.4, 1, 0, 0.4) -- bamboo stems

    -- Call to create grass gradient
    createGrassGradient()
end

function initMeadow()
    CreateMaterial("rock", 0.6, 0.6, 0.5) -- meadow rocks
    CreateMaterial("dirt", 0.4, 0.3, 0.2, 1, 0, 0.1) -- rich soil
    CreateMaterial("unphysical", 0.5, 0.7, 0.3, 1, 0, 0.2) -- lush meadow grass
    CreateMaterial("unphysical", 0.9, 0.9, 0.6, 1, 0, 0.2) -- wildflowers
	CreateMaterial("unphysical", 0.95, 1.0, 0.8, 1, 0, 0.2)
    CreateMaterial("masonry", 0.7, 0.7, 0.6, 1, 0, 0.4) -- flat stones

    -- Call to create grass gradient
    createGrassGradient()
end

function initIcelands()
    CreateMaterial("rock", 0.7, 0.8, 0.9) -- glacier rock
    CreateMaterial("dirt", 0.6, 0.7, 0.8, 1, 0, 0.1) -- frozen ground
    CreateMaterial("unphysical", 0.8, 0.9, 0.95, 1, 0, 0.2) -- glacial ice
    CreateMaterial("unphysical", 0.6, 0.7, 0.9, 1, 0, 0.2) -- deep ice crevasse
	CreateMaterial("unphysical", 0.7, 0.8, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.75, 0.85, 0.95, 1, 0, 0.4) -- ice formations

    -- Call to create grass gradient
    createGrassGradient()
end

function initJungle()
    CreateMaterial("rock", 0.3, 0.4, 0.2) -- jungle rock
    CreateMaterial("dirt", 0.4, 0.3, 0.2, 1, 0, 0.1) -- rich jungle soil
    CreateMaterial("unphysical", 0.1, 0.5, 0.1, 1, 0, 0.2) -- dark jungle foliage
    CreateMaterial("unphysical", 0.3, 0.7, 0.3, 1, 0, 0.2) -- vibrant jungle plants
	CreateMaterial("unphysical", 0.2, 0.6, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.5, 0.5, 0.4, 1, 0, 0.4) -- ancient stone

    -- Call to create grass gradient
    createGrassGradient()
end

function initAshlands()
    CreateMaterial("rock", 0.25, 0.25, 0.25) -- volcanic rock
    CreateMaterial("dirt", 0.3, 0.3, 0.3, 1, 0, 0.1) -- ash soil
    CreateMaterial("unphysical", 0.3, 0.3, 0.3, 1, 0, 0.2) -- ash
    CreateMaterial("unphysical", 0.5, 0.5, 0.5, 1, 0, 0.2) -- light ash
	CreateMaterial("unphysical", 0.2, 0.2, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.4, 0.4, 0.4, 1, 0, 0.4) -- ashen rock

    -- Call to create grass gradient
    createGrassGradient()
end

function initMangrove()
    CreateMaterial("rock", 0.4, 0.4, 0.3) -- mangrove rock
    CreateMaterial("dirt", 0.3, 0.25, 0.2, 1, 0, 0.1) -- muddy soil
    CreateMaterial("unphysical", 0.3, 0.4, 0.3, 1, 0, 0.2) -- mangrove foliage
    CreateMaterial("unphysical", 0.5, 0.4, 0.2, 1, 0, 0.2) -- muddy water
	CreateMaterial("unphysical", 0.4, 0.3, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.5, 0.45, 0.35, 1, 0, 0.4) -- mangrove roots

    -- Call to create grass gradient
    createGrassGradient()
end

function initCherry()
    CreateMaterial("rock", 0.6, 0.6, 0.6) -- light stone
    CreateMaterial("dirt", 0.4, 0.3, 0.25, 1, 0, 0.1) -- rich soil
    CreateMaterial("unphysical", 0.3, 0.6, 0.3, 1, 0, 0.2) -- green grass
    CreateMaterial("unphysical", 0.9, 0.7, 0.8, 1, 0, 0.2) -- cherry blossom pink
	CreateMaterial("unphysical", 1.0, 0.8, 0.9, 1, 0, 0.2)
    CreateMaterial("masonry", 0.7, 0.6, 0.5, 1, 0, 0.4) -- cherry wood

    -- Call to create grass gradient
    createGrassGradient()
end

function initHighlands()
    CreateMaterial("rock", 0.5, 0.5, 0.45) -- highland rock
    CreateMaterial("dirt", 0.4, 0.4, 0.35, 1, 0, 0.1) -- highland soil
    CreateMaterial("unphysical", 0.3, 0.5, 0.3, 1, 0, 0.2) -- highland grass
    CreateMaterial("unphysical", 0.6, 0.6, 0.5, 1, 0, 0.2) -- highland rock surface
	CreateMaterial("unphysical", 0.4, 0.4, 0.3, 1, 0, 0.2)
    CreateMaterial("masonry", 0.55, 0.55, 0.5, 1, 0, 0.4) -- highland stone

    -- Call to create grass gradient
    createGrassGradient()
end

function initMesa()
    CreateMaterial("rock", 0.7, 0.4, 0.3) -- mesa stone
    CreateMaterial("dirt", 0.6, 0.3, 0.2, 1, 0, 0.1) -- red clay
    CreateMaterial("unphysical", 0.6, 0.3, 0.2, 1, 0, 0.2) -- red mesa clay
    CreateMaterial("unphysical", 0.9, 0.6, 0.4, 1, 0, 0.2) -- lighter mesa surface
	CreateMaterial("unphysical", 1.0, 0.8, 0.6, 1, 0, 0.2)
    CreateMaterial("masonry", 0.75, 0.5, 0.35, 1, 0, 0.4) -- layered mesa rock

    -- Call to create grass gradient
    createGrassGradient()
end

function initWasteland()
    CreateMaterial("rock", 0.45, 0.4, 0.35) -- wasteland rock
    CreateMaterial("dirt", 0.5, 0.45, 0.4, 1, 0, 0.1) -- dusty soil
    CreateMaterial("unphysical", 0.5, 0.5, 0.4, 1, 0, 0.2) -- dead grass
    CreateMaterial("unphysical", 0.6, 0.5, 0.4, 1, 0, 0.2) -- dusty surface
	CreateMaterial("unphysical", 0.3, 0.3, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.4, 0.35, 0.3, 1, 0, 0.4) -- ruins

    -- Call to create grass gradient
    createGrassGradient()
end

function initTaiga()
    CreateMaterial("rock", 0.5, 0.55, 0.5) -- taiga rock
    CreateMaterial("dirt", 0.4, 0.35, 0.3, 1, 0, 0.1) -- forest soil
    CreateMaterial("unphysical", 0.4, 0.5, 0.4, 1, 0, 0.2) -- conifer green
    CreateMaterial("unphysical", 0.6, 0.7, 0.5, 1, 0, 0.2) -- forest floor
	CreateMaterial("unphysical", 0.3, 0.4, 0.3, 1, 0, 0.2)
    CreateMaterial("masonry", 0.6, 0.5, 0.4, 1, 0, 0.4) -- pine wood

    -- Call to create grass gradient
    createGrassGradient()
end

function initCorruption()
    CreateMaterial("rock", 0.3, 0.0, 0.4) -- corrupted stone
    CreateMaterial("dirt", 0.2, 0.0, 0.3, 1, 0, 0.1) -- corrupted soil
    CreateMaterial("unphysical", 0.4, 0.0, 0.6, 1, 0, 0.2) -- corruption growth
    CreateMaterial("unphysical", 0.8, 0.0, 1.0, 1, 0, 0.2) -- magical corruption energy
	CreateMaterial("unphysical", 0.6, 0.0, 0.9, 1, 0, 0.2)
    CreateMaterial("masonry", 0.5, 0.1, 0.7, 1, 0, 0.4) -- corrupted structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initCandyland()
    CreateMaterial("rock", 0.8, 0.4, 0.8) -- rock candy
    CreateMaterial("dirt", 0.7, 0.3, 0.7, 1, 0, 0.1) -- sugar soil
    CreateMaterial("unphysical", 0.9, 0.5, 0.9, 1, 0, 0.2) -- cotton candy
    CreateMaterial("unphysical", 0.5, 0.9, 1.0, 1, 0, 0.2) -- blue raspberry
	CreateMaterial("unphysical", 1.0, 1.0, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 1.0, 0.7, 0.7, 1, 0, 0.4) -- peppermint stone

    -- Call to create grass gradient
    createGrassGradient()
end

function initEthereal()
    CreateMaterial("rock", 0.8, 0.8, 1.0) -- ethereal stone
    CreateMaterial("dirt", 0.7, 0.8, 0.9, 1, 0, 0.1) -- cloud-like ground
    CreateMaterial("unphysical", 0.6, 0.9, 1.0, 1, 0, 0.2) -- light ethereal blue
    CreateMaterial("unphysical", 1.0, 1.0, 0.8, 1, 0, 0.2) -- glowing light
	CreateMaterial("unphysical", 0.8, 0.6, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.9, 0.9, 1.0, 1, 0, 0.4) -- heavenly structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initCyberpunk()
    CreateMaterial("rock", 0.1, 0.1, 0.1) -- dark city concrete
    CreateMaterial("dirt", 0.2, 0.2, 0.2, 1, 0, 0.1) -- urban ground
    CreateMaterial("unphysical", 0.0, 0.6, 0.9, 1, 0, 0.2) -- neon blue
    CreateMaterial("unphysical", 1.0, 0.0, 0.6, 1, 0, 0.2) -- hot pink
	CreateMaterial("unphysical", 0.2, 1.0, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.3, 0.3, 0.3, 1, 0, 0.4) -- futuristic structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initCrimson()
    CreateMaterial("rock", 0.2, 0.2, 0.2) -- dark lava rock
    CreateMaterial("dirt", 0.8, 0.1, 0.1, 1, 0, 0.1) -- lava red dirt
    CreateMaterial("unphysical", 1.0, 0.0, 0.0, 1, 0, 0) -- fiery lava
    CreateMaterial("unphysical", 0.7, 0.0, 0.0, 1, 1, 0, 0) -- molten magma
	CreateMaterial("unphysical", 0.4, 0.0, 0.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.6, 0.3, 0.1, 1, 0, 0.4) -- rocky volcanic surface

    -- Call to create grass gradient
    createGrassGradient()
end

function initVaporwave()
    CreateMaterial("rock", 0.2, 0.0, 0.4) -- dark synthwave rock
    CreateMaterial("dirt", 0.3, 0.0, 0.6, 1, 0, 0.1) -- purple ground
    CreateMaterial("unphysical", 0.4, 0.0, 0.8, 1, 0, 0.2) -- deep purple
    CreateMaterial("unphysical", 0.0, 0.8, 0.8, 1, 0, 0.2) -- teal/cyan
	CreateMaterial("unphysical", 1.0, 0.7, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.9, 0.0, 0.6, 1, 0, 0.4) -- retro-future structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initNeon()
    CreateMaterial("rock", 0.05, 0.05, 0.05) -- black rock
    CreateMaterial("dirt", 0.1, 0.1, 0.1, 1, 0, 0.1) -- dark soil
    CreateMaterial("unphysical", 0.0, 1.0, 0.0, 1, 0, 0.2) -- electric green
    CreateMaterial("unphysical", 1.0, 1.0, 0.0, 1, 0, 0.2) -- bright yellow
	CreateMaterial("unphysical", 1.0, 0.0, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.0, 0.0, 1.0, 1, 0, 0.4) -- blue structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initToxic()
    CreateMaterial("rock", 0.3, 0.3, 0.2) -- contaminated rock
    CreateMaterial("dirt", 0.2, 0.3, 0.1, 1, 0, 0.1) -- toxic soil
    CreateMaterial("unphysical", 0.2, 0.8, 0.0, 1, 0, 0.2) -- toxic green
    CreateMaterial("unphysical", 0.9, 1.0, 0.0, 1, 0, 0.2) -- radioactive yellow
	CreateMaterial("unphysical", 0.1, 0.6, 0.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.4, 0.7, 0.0, 1, 0, 0.4) -- contaminated structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initGlitch()
    CreateMaterial("rock", 0.0, 0.0, 0.0) -- void rock
    CreateMaterial("dirt", 0.1, 0.0, 0.1, 1, 0, 0.1) -- glitched soil
    CreateMaterial("unphysical", 0.0, 0.0, 0.0, 1, 0, 0.2) -- black void
    CreateMaterial("unphysical", 1.0, 0.0, 1.0, 1, 0, 0.2) -- hot magenta
	CreateMaterial("unphysical", 0.0, 1.0, 1.0, 1, 0, 0.2)
    CreateMaterial("masonry", 0.0, 1.0, 0.0, 1, 0, 0.4) -- glitched structures

    -- Call to create grass gradient
    createGrassGradient()
end

function initUnderdark()
    CreateMaterial("rock", 0.1, 0.0, 0.2) -- deep cavern rock
    CreateMaterial("dirt", 0.15, 0.0, 0.25, 1, 0, 0.1) -- magical soil
    CreateMaterial("unphysical", 0.2, 0.0, 0.3, 1, 0, 0.2) -- deep underworld purple
    CreateMaterial("unphysical", 0.5, 0.0, 0.8, 1, 0, 0.2) -- glowing arcane energy
	CreateMaterial("unphysical", 0.1, 0.0, 0.2, 1, 0, 0.2)
    CreateMaterial("masonry", 0.3, 0.0, 0.5, 1, 0, 0.4) -- ancient magic structures

    -- Call to create grass gradient
    createGrassGradient()
end