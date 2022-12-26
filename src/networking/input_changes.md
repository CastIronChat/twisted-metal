# Input Logic Changes

`PlayerInput`:
    generic interface
    gameplay is coded against this

`PlayerInputSnapshot`:
    snapshot of inputs
    can be captured from physical controller
    can be injected into the simulation each frame
    can be marshalled to/from packet

When networked:
    at start of frame
    the network controller captures inputs for all local players
    broadcasts them on the network
    the network controller then injects inputs previously-received from the network
    If it does not have enough data, it tells the game update loop to skip this frame
        This causes a noticable hitch, but the logic is simple

`InputUpdater`?
    Swappable implementation, can be a `NetworkedInputUpdater` or a `LocalInputUpdater`
    Currently, `PlayerManager` and `NetworkManager` are kinda filling this role
