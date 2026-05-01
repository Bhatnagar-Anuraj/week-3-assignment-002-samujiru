"""
DIGM 131 - Assignment 3: Function Library (main_scene.py)
==========================================================

OBJECTIVE:
    Use the functions you wrote in scene_functions.py to build a complete
    scene. This file demonstrates how importing and reusing functions makes
    scene creation clean and readable.

REQUIREMENTS:
    1. Import scene_functions (the module you completed).
    2. Call each of your 5+ functions at least once.
    3. Use place_in_circle with at least one of your create functions.
    4. The final scene should contain at least 15 objects total.
    5. Comment your code explaining what you are building.

GRADING CRITERIA:
    - [30%] All 5+ functions from scene_functions.py are called.
    - [25%] place_in_circle is used at least once.
    - [20%] Scene contains 15+ objects and looks intentional.
    - [15%] Code is well-commented.
    - [10%] Script runs without errors from top to bottom.
"""

import maya.cmds as cmds
import scene_functions as sf

# ---------------------------------------------------------------------------
# Scene Setup
# ---------------------------------------------------------------------------
cmds.file(new=True, force=True)

# Create a ground plane.
ground = cmds.polyPlane(name="ground", width=60, height=60,
                        subdivisionsX=1, subdivisionsY=1)[0]

#This line adds the main building that the city is built around.
sf.create_building(width=12, height=18, depth=12, position=(0, 0, 0))

#These lines add more buildings around.
sf.create_building(width=6, height=10, depth=6, position=(-20, 0, -15))
sf.create_building(width=6, height=10, depth=6, position=(20, 0, -15))

#This line adds a circle of trees, surrounding a little park in the city.
sf.place_in_circle(sf.create_tree, count=10, radius=35, center=(0, 0, 0))

#These lines add lamp posts around the city
sf.create_lamp_post(position=(15, 0, 15))
sf.create_lamp_post(position=(-15, 0, 15))
sf.create_lamp_post(position=(15, 0, -15))
sf.create_lamp_post(position=(-15, 0, -15))

#This line adds a fence in the scene. 
sf.create_fence(length=50, height=2, post_count=12, position=(-25, 0, -25))

#This line adds a tree, but it's not in a circle. 
sf.create_tree(trunk_height=5, canopy_radius=3, position=(0, 0, 25))

# ---------------------------------------------------------------------------
# Final viewport framing (do not remove).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.viewFit(allObjects=True)
    print("Main scene built successfully!")
