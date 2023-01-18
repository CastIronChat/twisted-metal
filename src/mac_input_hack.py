from __future__ import annotations

import platform

import pyglet

#
# Mac-specific hack to fix a pyglet bug for game controllers
#
# My understanding of the situation:
#
# Windows exposes a great xinput API that allows games to easily and reliably
# talk to xbox-like controllers.  The controller itself explains how its own
# buttons correspond to xbox buttons, so the game does not need to care.
#
# On Mac, without that API, games are forced to bundle a database of mappings
# between hardware GUIDs and axis/button indices.  If a controller guid is in
# the database, then the game understands how to map it onto the xbox layout.
#
# Pyglet has a bug where it does not detect the GUIDs of bluetooth controllers
# on Mac.  Additionally, it bundles an incomplete database.
#
# This file does 2x things:
# - add a more extensive database of GUID mappings
# - fix pyglet's GUID reading bug
#
# References:
#   https://github.com/pyglet/pyglet/issues/574#issuecomment-1102608401
#   https://github.com/pyglet/pyglet/issues/705
#


def apply_fix():
    if platform.system() == "Darwin":

        # Replacement implementations of two of pyglet's functions.
        # They were copy-pasted out of pyglet's source code, then modified to
        # fix the bug
        def get_guid(self):
            """Generate an SDL2 style GUID from the product guid."""

            if isinstance(self.transport, str) and self.transport.upper() == "USB":
                bustype = 0x03
                vendor = self.vendorID or 0
                product = self.productID or 0
                version = self.versionNumber or 0
                # Byte swap (ABCD --> CDAB):
                bustype = ((bustype << 8) | (bustype >> 8)) & 0xFFFF
                vendor = ((vendor << 8) | (vendor >> 8)) & 0xFFFF
                product = ((product << 8) | (product >> 8)) & 0xFFFF
                version = ((version << 8) | (version >> 8)) & 0xFFFF
                return "{:04x}0000{:04x}0000{:04x}0000{:04x}0000".format(
                    bustype, vendor, product, version
                )

            elif (
                isinstance(self.transport, str)
                and self.transport.upper() == "BLUETOOTH"
            ):
                bustype = 0x05
                # Byte swap (ABCD --> CDAB):
                bustype = ((bustype << 8) | (bustype >> 8)) & 0xFFFF

                # TODO: test fallback to vendor id if no product name:
                name = self.product or str(self.vendorID)
                name = name.encode().hex()
                return "{:04x}0000{:0<24}".format(bustype, name)

        def _create_controller(device, display):
            try:
                print(
                    device.manufacturer,
                    "-",
                    device.product,
                    device.transport,
                    device.get_guid(),
                )
            except Exception:
                print(device.transport, device.get_guid())
            if isinstance(device.transport, str) and device.transport.upper() in (
                "USB",
                "BLUETOOTH",
            ):
                mapping = pyglet.input.darwin_hid.get_mapping(device.get_guid())
                if not mapping:
                    return
                return pyglet.input.darwin_hid.Controller(
                    pyglet.input.darwin_hid.PygletDevice(
                        display, device, pyglet.input.darwin_hid._hid_manager
                    ),
                    mapping,
                )

        pyglet.input.darwin_hid.Device.get_guid = get_guid
        pyglet.input.darwin_hid._create_controller = _create_controller

        pyglet.input.controller.add_mappings_from_file("assets/gamecontrollerdb.txt")
