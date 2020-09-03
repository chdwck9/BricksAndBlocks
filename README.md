# BricksAndBlocks
Is your work highly project based? Do you find yourself creating the same folder structure and copying templates every time?

Bricks and Blocks is a program/framework to automating this. Of course it's nothing new, but what's unique is its flexibility - it's a program that's easy enough for a manager to use, detailed enough for a developer to use and broad enough that a designer can use.

The core is the brick and the block. A brick is a subfolder structure and accompanying templates (for example, an app in a project folder). A block is a global template (think the project plan). Using these two effectively allows you to create and change project structures, adding bricks or blocks as you need.

# How to use
I built the program so that it would be easy use... once it's properly installed (if there's anyone keen on building a Windows and a Mac installer, branch this repo!).

To install, you must first install Python, pip install dependancies, and modify the config file (see below). The final step is to adapt the registry file or the Mac automator script in order to have access to BnB in context menus. Instructional guide will follow in due time.

The config file is the central controller for your bricks and blocks. I've provided a basic template as an example. Editing bricks will provide new sub-folders and copy files from a templates folder on your computer. Editing blocks will give you additional access to those templates and drop them into the root folder (or another if you need). 

When you run the program you will be asked to give the project folder a name. Then you'll be provided a menu to add the bricks you've setup to your project folder. Finally, you can choose which bricks you want to add to the project file.

The tool will setup your folder as directed.

# The future of Bricks and Blocks
Some things I'm working on, and would relish some collaboration on:
- Installer file for Windows
- Installer file for Mac/linux
- Adding shell execution (adapt the config slightly)
- Build a basic gui for non-developers
