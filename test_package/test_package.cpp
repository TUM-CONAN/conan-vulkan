#include "vulkan/vulkan.hpp"

#include <cstdlib>
#include <iostream>

int main()
{
    vk::ApplicationInfo appInfo;
	appInfo.pApplicationName = "TestApp";
	appInfo.pEngineName = "TestEngine";
    appInfo.apiVersion = VK_API_VERSION_1_0;

    vk::InstanceCreateInfo instanceCreateInfo;
    instanceCreateInfo.pApplicationInfo = &appInfo;

    vk::Instance instance = vk::createInstance(instanceCreateInfo);

	auto physicalDevices = instance.enumeratePhysicalDevices();
    auto physicalDevice = physicalDevices[0];
    auto deviceProperties = physicalDevice.getProperties();
    auto deviceMemoryProperties = physicalDevice.getMemoryProperties();

    std::cout << "Vulkan device created\n";
    std::cout << "API Version:    " << deviceProperties.apiVersion << "\n";
    std::cout << "Driver Version: " << deviceProperties.driverVersion << "\n";
    std::cout << "Device Name:    " << deviceProperties.deviceName << "\n";
    std::cout << "Device Type:    " << vk::to_string(deviceProperties.deviceType) << "\n";
    std::cout << "Memory Heaps:  " << deviceMemoryProperties.memoryHeapCount << "\n";
    
    return EXIT_SUCCESS;
}
