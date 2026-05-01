"""
DIGM 131 - Assignment 3: Function Library (scene_functions.py)
===============================================================

OBJECTIVE:
    Create a library of reusable functions that each generate a specific
    type of scene element. This module will be imported by main_scene.py.

REQUIREMENTS:
    1. Implement at least 5 reusable functions.
    2. Every function must have a complete docstring with Args and Returns.
    3. Every function must accept parameters for position and/or size so
       they can be reused at different locations and scales.
    4. Every function must return the name(s) of the Maya object(s) it creates.
    5. Follow PEP 8 naming conventions (snake_case for functions/variables).

GRADING CRITERIA:
    - [30%] At least 5 functions, each creating a distinct scene element.
    - [25%] Functions accept parameters and use them (not hard-coded values).
    - [20%] Every function has a complete docstring (summary, Args, Returns).
    - [15%] Functions return the created object name(s).
    - [10%] Clean, readable code following PEP 8.
"""

import maya.cmds as cmds

#this line imports the math module
import math

def create_building(width=4, height=8, depth=4, position=(0, 0, 0)):
    """Create a simple building from a cube, placed on the ground plane.

    The building is a single scaled cube whose base sits at ground level
    (y = 0) at the given position.

    Args:
        width (float): Width of the building along the X axis.
        height (float): Height of the building along the Y axis.
        depth (float): Depth of the building along the Z axis.
        position (tuple): (x, y, z) ground-level position. The building
            base will rest at this point; y is typically 0.

    Returns:
        str: The name of the created building transform node.
    """
    #this line of code create building geometry
    building = cmds.polyCube(w=width, h=height, d=depth, name="building_01")[0]
    #this line moves the mesh so the base sit son the ground plane. 
    cmds.xform(building, translation=(position[0], position[1] + (height / 2.0), position[2]))
    #this line returns object name
    return building

def create_tree(trunk_radius=0.3, trunk_height=3, canopy_radius=2,
                position=(0, 0, 0)):
    """Create a simple tree using a cylinder trunk and a sphere canopy.

    Args:
        trunk_radius (float): Radius of the cylindrical trunk.
        trunk_height (float): Height of the trunk cylinder.
        canopy_radius (float): Radius of the sphere used for the canopy.
        position (tuple): (x, y, z) ground-level position for the tree base.

    Returns:
        str: The name of a group node containing the trunk and canopy.
    """
    #this line creates the trunk and moves it so it's at Y=0
    trunk = cmds.polyCylinder(r=trunk_radius, h=trunk_height, name="trunk")[0]
    cmds.xform(trunk, translation=(0, trunk_height / 2.0, 0))

    #this line creatse the canopy
    canopy = cmds.polySphere(r=canopy_radius, name="canopy")[0]
    cmds.xform(canopy, translation=(0, trunk_height + (canopy_radius * 0.75), 0))

    #this line groups the tree and canopy, and moves them to the targeted position
    tree_grp = cmds.group(trunk, canopy, name="tree_grp")
    cmds.xform(tree_grp, translation=position)
    #this line returns the group name
    return tree_grp

def create_fence(length=10, height=1.5, post_count=6, position=(0, 0, 0)):
    """Create a simple fence made of posts and rails.

    The fence runs along the X axis starting at the given position.

    Args:
        length (float): Total length of the fence along the X axis.
        height (float): Height of the fence posts.
        post_count (int): Number of vertical posts (must be >= 2).
        position (tuple): (x, y, z) starting position of the fence.

    Returns:
        str: The name of a group node containing all fence parts.
    """
    items_to_group = []
    spacing = length / (post_count - 1)

    #this line creates the vertical posts
    for i in range(post_count):
        post = cmds.polyCube(w=0.2, h=height, d=0.2, name=f"fence_post_{i}")[0]
        cmds.xform(post, translation=(i * spacing, height / 2.0, 0))
        items_to_group.append(post)

    #this line creates the horizontal rails
    rail = cmds.polyCube(w=length, h=0.2, d=0.1, name="fence_rail")[0]
    cmds.xform(rail, translation=(length / 2.0 - 0.1, height * 0.75, 0))
    items_to_group.append(rail)

    #this line groups the horizontal rails and the vertical posts, and moves them into position
    fence_grp = cmds.group(items_to_group, name="fence_grp")
    cmds.xform(fence_grp, translation=position)
    #this line returns the group name
    return fence_grp

def create_lamp_post(pole_height=5, light_radius=0.5, position=(0, 0, 0)):
    """Create a street lamp using a cylinder pole and a sphere light.

    Args:
        pole_height (float): Height of the lamp pole.
        light_radius (float): Radius of the sphere representing the light.
        position (tuple): (x, y, z) ground-level position.

    Returns:
        str: The name of a group node containing the pole and light.
    """
    #this line creates the pole using a cylinder
    pole = cmds.polyCylinder(r=0.15, h=pole_height, name="lamp_pole")[0]
    cmds.xform(pole, translation=(0, pole_height / 2.0, 0))

    #this line creates the bulb
    bulb = cmds.polySphere(r=light_radius, name="lamp_bulb")[0]
    cmds.xform(bulb, translation=(0, pole_height, 0))

    #this line groups and repositions the pole and bulb
    lamp_grp = cmds.group(pole, bulb, name="lamp_post_grp")
    cmds.xform(lamp_grp, translation=position)
    #this line returns the group name
    return lamp_grp

def place_in_circle(create_func, count=8, radius=10, center=(0, 0, 0),
                     **kwargs):
    """Place objects created by 'create_func' in a circular arrangement.

    This is a higher-order function: it takes another function as an
    argument and calls it repeatedly to place objects around a circle.

    Args:
        create_func (callable): A function from this module (e.g.,
            create_tree) that accepts a 'position' keyword argument
            and returns an object name.
        count (int): Number of objects to place around the circle.
        radius (float): Radius of the circle.
        center (tuple): (x, y, z) center of the circle.
        **kwargs: Additional keyword arguments passed to create_func
            (e.g., trunk_height=4).

    Returns:
        list: A list of object/group names created by create_func.
    """

    for i in range(count):
        #This line calculates the angle in radians 
        angle = 2 * math.pi * i / count

        #this line calculates the x and z coordinates based on the circle formula
        x = center[0] + radius * math.cos(angle)
        z = center[2] + radius * math.sin(angle)

        #this line calls the passed function with the calculated position and extra arguments
        new_obj = create_func(position=(x, center[1], z), **kwargs)
        results.append(new_obj)
    #this line returns results
    return results
