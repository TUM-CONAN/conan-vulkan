## This repository holds a conan recipe for the Vulkan LunarG SDK.

[Conan.io](https://conan.io) package for [Vulkan LunarG SDK](https://vulkan.lunarg.com) project

## For Users: Use this package

### Basic setup

    $ conan install vulkan/1.1.85.0@camposs/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    vulkan/1.1.85.0@camposs/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..
    
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they shoudl not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to ulricheck conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build  

This is a header only library, so nothing needs to be built.

## Package 

    $ conan create camposs/stable
    
## Add Remote

    $ conan remote add camposs "https://conan.campar.in.tum.de/api/conan/conan-camposs" True

## Upload

    $ conan upload -r camposs vulkan/1.1.85.0@camposs/stable

### License
[License](https://vulkan.lunarg.com/sdk/home#sdk-license)
