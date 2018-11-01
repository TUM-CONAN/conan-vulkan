#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class VulkanConan(ConanFile):
    name = "vulkan"
    version = "1.1.85.0"
    description = "Vulkan is a new generation graphics and compute API that provides high-efficiency, cross-platform access to modern GPUs used in a wide variety of devices from PCs and consoles to mobile phones and embedded platforms."
    url = "https://github.com/ulricheck/conan-vulkan"
    homepage = "https://www.lunarg.com/vulkan-sdk/"

    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://vulkan.lunarg.com/sdk/download"
        if self.settings.os == 'Windows':
            tools.download("{0}/{1}/windows/VulkanSDK-{1}-Installer.exe".format(source_url, self.version), "VulkanSDK.exe")
            self.run("VulkanSDK.exe /S")
            os.rename("c:/VulkanSDK/{0}".format(self.version), self.source_subfolder)
        elif self.settings.os == "Macos":
            tools.download("{0}/{1}/mac/vulkansdk-macos-{1}.tar.gz".format(source_url, self.version), "vulkansdk-macos.tar.gz")
            tools.unzip("vulkansdk-macos.tar.gz")
            os.rename("vulkansdk-macos-{0}".format(self.version), self.source_subfolder)
        else:
            raise ValueError("Unsupported platform")

    def get_lib_folder(self):
        if self.settings.os == 'Windows':
            if self.settings.arch == 'x86':
                if self.settings.build_type == 'Release':
                    return os.path.join(self.source_subfolder, "Lib32")
                else:
                    return os.path.join(self.source_subfolder, "Source/lib32")
            else:
                if self.settings.build_type == 'Release':
                    return os.path.join(self.source_subfolder, "Lib")
                else:
                    return os.path.join(self.source_subfolder, "Source/lib")
        elif self.settings.os == "Macos":
            return os.path.join(self.source_subfolder, "macOS/lib")
        else:
            raise ValueError("unsupported platform")

    def get_bin_folder(self):
        if self.settings.os == 'Windows':
            if self.settings.arch == 'x86':
                return os.path.join(self.source_subfolder, "Bin32")
            else:
                return os.path.join(self.source_subfolder, "Bin")
        elif self.settings.os == "Macos":
            return os.path.join(self.source_subfolder, "macOS/bin")
        else:
            raise ValueError("unsupported platform")

    def get_frameworks_folder(self):
        if self.settings.os == "Macos":
            return os.path.join(self.source_subfolder, "macOS/Frameworks")
        else:
            raise ValueError("unsupported platform")

    def package(self):

        lib_folder = self.get_lib_folder()
        if self.settings.os == "Windows":
            self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)
            include_folder = os.path.join(self.source_subfolder, "Include")
            self.copy(pattern="*", dst="include", src=include_folder)

            if self.options.shared:
                bin_folder = self.get_bin_folder()
                if self.settings.build_type == 'Release':
                    self.copy(pattern="*.dll", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*.json", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*", dst="lib", src=lib_folder, keep_path=False)
                else:
                    self.copy(pattern="*.dll", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*.json", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*.lib", dst="lib", src=lib_folder, keep_path=False)
                    self.copy(pattern="*.pdb", dst="lib", src=lib_folder, keep_path=False)
                os.remove(os.path.join(self.package_folder, 'lib', 'VKstatic.1.lib'))
                os.remove(os.path.join(self.package_folder, 'lib', 'shaderc_combined.lib'))
            else:
                self.copy(pattern="VKstatic.1.lib", dst="lib", src=lib_folder, keep_path=False)


        elif self.settings.os == "Macos":
            include_folder = os.path.join(self.source_subfolder, "macos/include")
            self.copy(pattern="*", dst="include", src=include_folder)

            if self.options.shared:
                self.copy(pattern="*.dylib", dst="lib", src=lib_folder, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=lib_folder, keep_path=False)
                self.copy(pattern="libMoltenVK.dylib", dst="lib", src=lib_folder, keep_path=False)

            self.copy(pattern="*", dst="etc", src=os.path.join(self.source_subfolder, "macOS", "etc"), keep_path=True)
        else:
            raise ValueError("unsupported platform")

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["vulkan-1"]
        elif self.settings.os == "Macos":
            self.cpp_info.libs = ['vulkan']
            self.env_info.VK_ICD_FILENAMES = os.path.join(self.package_folder, "etc", "vulkan", "icd.d", "MoltenVK_icd.json")
