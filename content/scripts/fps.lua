-- original script is https://raw.githubusercontent.com/CasperFlyModz/discord.gg-rips/main/FPSBooster.lua
game:GetService('UserInputService').WindowFocusReleased:Connect(function()
    RunService:Set3dRenderingEnabled(false)
end)
game:GetService('UserInputService').WindowFocused:Connect(function()
    RunService:Set3dRenderingEnabled(true)
end)

if not _G.Ignore then
    _G.Ignore = {} -- Add Instances to this table to ignore them
end
if not _G.WaitPerAmount then
    _G.WaitPerAmount = 500
end

repeat task.wait() until game:IsLoaded()

if not _G.Settings then
    _G.Settings = {
        Players = {
            ["Ignore Me"] = false,
            ["Ignore Others"] = false,
            ["Ignore Tools"] = true
        },
        Meshes = {
            NoMesh = true,
            NoTexture = true,
            Destroy = true
        },
        Images = {
            Invisible = true,
            Destroy = true
        },
        Explosions = {
            Smaller = true,
            Invisible = true,
            Destroy = true
        },
        Particles = {
            Invisible = true,
            Destroy = true
        },
        TextLabels = {
            LowerQuality = true,
            Invisible = true,
            Destroy = true
        },
        MeshParts = {
            LowerQuality = true,
            Invisible = false,
            NoTexture = true,
            NoMesh = true,
            Destroy = true
        },
        Other = {
            ["FPS Cap"] = 5,
            ["No Camera Effects"] = true,
            ["No Clothes"] = true,
            ["Low Water Graphics"] = true,
            ["No Shadows"] = true,
            ["Low Rendering"] = true,
            ["Low Quality Parts"] = true,
            ["Low Quality Models"] = true,
            ["Reset Materials"] = true,
            ["Lower Quality MeshParts"] = true
        }
    }
end

local Players, Lighting, MaterialService = game:GetService("Players"), game:GetService("Lighting"), game:GetService("MaterialService")
local ME, CanBeEnabled = Players.LocalPlayer, {"ParticleEmitter", "Trail", "Smoke", "Fire", "Sparkles"}

local function PartOfCharacter(Instance)
    for _, v in pairs(Players:GetPlayers()) do
        if v ~= ME and v.Character and Instance:IsDescendantOf(v.Character) then
            return true
        end
    end
    return false
end

local function DescendantOfIgnore(Instance)
    for _, v in pairs(_G.Ignore) do
        if Instance:IsDescendantOf(v) then
            return true
        end
    end
    return false
end

local function CheckIfBad(Instance)
    if not Instance:IsDescendantOf(Players) and not PartOfCharacter(Instance) and not DescendantOfIgnore(Instance) then
        -- Handle instance based on settings
        if Instance:IsA("DataModelMesh") and _G.Settings.Meshes.Destroy then
            Instance:Destroy()
        elseif Instance:IsA("FaceInstance") and _G.Settings.Images.Destroy then
            Instance:Destroy()
        elseif table.find(CanBeEnabled, Instance.ClassName) and _G.Settings.Particles.Destroy then
            Instance:Destroy()
        elseif Instance:IsA("PostEffect") and _G.Settings.Other["No Camera Effects"] then
            Instance.Enabled = false
        elseif Instance:IsA("Explosion") and _G.Settings.Explosions.Destroy then
            Instance:Destroy()
        elseif Instance:IsA("Clothing") and _G.Settings.Other["No Clothes"] then
            Instance:Destroy()
        elseif Instance:IsA("BasePart") and _G.Settings.Other["Low Quality Parts"] then
            Instance.Material = Enum.Material.Plastic
        elseif Instance:IsA("MeshPart") and _G.Settings.MeshParts.Destroy then
            Instance:Destroy()
        end
    end
end

game.DescendantAdded:Connect(CheckIfBad)
for _, v in pairs(game:GetDescendants()) do
    CheckIfBad(v)
end
