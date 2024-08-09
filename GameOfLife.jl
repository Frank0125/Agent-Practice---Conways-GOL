# to install the library
using Pkg; Pkg.add("Agents")
using Agents, Random

# Rules definition.
# The rules of Conway's game of life are defined based on four numbers: Death, Survival, Reproduction, Overpopulation, grouped as (D, S, R, O) Cells die if the number of their living neighbors is <D or >O, survive if the number of their living neighbors is ≤S, come to life if their living neighbors are ≥R and ≤O.
rules = (2, 3, 3, 3) # (D, S, R, O)

# We don't actually need agents, just cellular automaton
@agent struct Automaton(GridAgent{2}) end

# The following function builds a 2D cellular automaton given some rules. dims is a tuple of integers determining the width and height of the grid environment. metric specifies how to measure distances in the space, and in our example it actually decides whether cells connect to their diagonal neighbors or not. :chebyshev includes diagonal, :manhattan does not.
# Initially the cells are dead. 
function build_model(rules::Tuple;
        alive_probability = 0.2,
        dims = (100, 100), metric = :chebyshev, seed = 42
    )
    space = GridSpaceSingle(dims; metric)
    properties = Dict(:rules => rules)
    status = zeros(Bool, dims)
    # We use a second copy so that we can do a "synchronous" update of the status
    new_status = zeros(Bool, dims)
    # We use a `NamedTuple` for the parameter container to avoid type instabilities
    properties = (; rules, status, new_status)
    model = StandardABM(Automaton, space; properties, model_step! = game_of_life_step!,
                rng = MersenneTwister(seed), container = Vector)
    # Turn some of the cells on
    for pos in positions(model)
        if rand(abmrng(model)) < alive_probability
            status[pos...] = true
        end
    end
    return model
end

# steps for the simulation
function game_of_life_step!(model)
    # First, get the new statuses
    new_status = model.new_status
    status = model.status
    @inbounds for pos in positions(model)
        # Convenience function that counts how many nearby cells are "alive"
        n = alive_neighbors(pos, model)
        if status[pos...] == true && model.rules[1] ≤ n ≤ model.rules[4]
            new_status[pos...] = true
        elseif status[pos...] == false && model.rules[3] ≤ n ≤ model.rules[4]
            new_status[pos...] = true
        else
            new_status[pos...] = false
        end
    end
    # Then, update the new statuses into the old
    status .= new_status
    return
end

function alive_neighbors(pos, model) # count alive neighboring cells
    c = 0
    @inbounds for near_pos in nearby_positions(pos, model)
        if model.status[near_pos...] == true
            c += 1
        end
    end
    return c
end


# Finally!
# let's run the whole thing
model = build_model(rules)

# This generates a video of the simulation, and saves it
Pkg.add("CairoMakie")
using CairoMakie

plotkwargs = (
    add_colorbar = false,
    heatarray = :status,
    heatkwargs = (
        colorrange = (0, 1),
        colormap = cgrad([:white, :black]; categorical = true),
    ),
)

abmvideo(
    "game_of_life.mp4",
    model;
    title = "Game of Life",
    framerate = 10,
    frames = 60,
    plotkwargs...,
)