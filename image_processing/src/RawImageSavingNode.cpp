#include "RawImageSavingNode.h"

#include <fstream>

RawImageSavingNode::RawImageSavingNode(std::map<std::string, FolderConfig>&& config) : _camera_name_folder_map(std::forward<decltype(config)>(config)) {
	for (auto const& [camera_name, folder_config] : _camera_name_folder_map) {
		std::filesystem::create_directories(folder_config.folder);
	}
}

/**
 * @brief Saves the incoming raw image data to the previous defined folder.
 *
 * @param data The raw image data to be saved.
 */
void RawImageSavingNode::run(const ImageDataRaw& data) {
	std::ofstream raw_image(
	    _camera_name_folder_map.at(data.source).folder / (std::to_string(std::chrono::time_point_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now()).time_since_epoch().count()) + '_' + std::to_string(data.timestamp)));

	raw_image.write(reinterpret_cast<const char*>(data.image_raw.data()), data.image_raw.size());
}
