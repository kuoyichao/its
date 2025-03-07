project(gstreamer_plugins_worst)

add_library(${PROJECT_NAME} SHARED src/rtp_header_extension_timestamp_frame_stream.cpp src/timestamp_frame_meta.cpp src/timestamp_frame_meta.cpp src/rtp_header_extension_random_number_stream.cpp src/random_number_meta.cpp src/rtp_header_extension_random_number.cpp src/random_number_meta.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_23)
target_compile_definitions(${PROJECT_NAME} PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_executable(test_${PROJECT_NAME} test/test_${PROJECT_NAME}.cpp)
target_include_directories(test_${PROJECT_NAME} PUBLIC ${OpenCV_INCLUDE_DIRS})
target_link_libraries(test_${PROJECT_NAME} PUBLIC ${PROJECT_NAME})
target_link_libraries(test_${PROJECT_NAME} PUBLIC common)
target_link_libraries(test_${PROJECT_NAME} PUBLIC PkgConfig::gstreamer)
target_link_libraries(test_${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-sdp)
target_link_libraries(test_${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-app)
target_link_libraries(test_${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-video)
target_link_libraries(test_${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-rtsp-server)
target_link_libraries(test_${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-rtsp)
target_link_libraries(test_${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-rtp)
target_link_libraries(test_${PROJECT_NAME} PUBLIC ${OpenCV_LIBS})
target_compile_features(test_${PROJECT_NAME} PRIVATE cxx_std_23)
target_compile_definitions(test_${PROJECT_NAME} PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_executable(test_${PROJECT_NAME}_receive test/test_${PROJECT_NAME}_receive.cpp)
target_include_directories(test_${PROJECT_NAME}_receive PUBLIC ${OpenCV_INCLUDE_DIRS})
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC ${PROJECT_NAME})
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC common)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC PkgConfig::gstreamer)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC PkgConfig::gstreamer-sdp)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC PkgConfig::gstreamer-app)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC PkgConfig::gstreamer-video)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC PkgConfig::gstreamer-rtsp-server)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC PkgConfig::gstreamer-rtsp)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC PkgConfig::gstreamer-rtp)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC ${OpenCV_LIBS})
target_compile_features(test_${PROJECT_NAME}_receive PRIVATE cxx_std_23)
target_compile_definitions(test_${PROJECT_NAME}_receive PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

project(data_communication_nodes)

add_library(${PROJECT_NAME} SHARED src/StreamingDataNode.cpp src/ReceivingDataNode.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_include_directories(${PROJECT_NAME} PUBLIC ${OpenCV_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PUBLIC common)
target_link_libraries(${PROJECT_NAME} PUBLIC ${OpenCV_LIBS})
target_link_libraries(${PROJECT_NAME} PUBLIC msg)
target_link_libraries(${PROJECT_NAME} PUBLIC concurra)
target_link_libraries(${PROJECT_NAME} PUBLIC msg_yas)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::Mosquitto)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_23)
target_compile_definitions(${PROJECT_NAME} PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_executable(test_${PROJECT_NAME} test/test_${PROJECT_NAME}.cpp)
target_link_libraries(test_${PROJECT_NAME} PUBLIC ${PROJECT_NAME})
target_link_libraries(test_${PROJECT_NAME} PUBLIC common)
target_compile_features(test_${PROJECT_NAME} PRIVATE cxx_std_23)
target_compile_definitions(test_${PROJECT_NAME} PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_test(NAME ctest_${PROJECT_NAME} COMMAND test_${PROJECT_NAME} WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

project(image_communication_nodes)

add_library(${PROJECT_NAME} SHARED src/StreamingImageNode.cpp src/StreamingNodeBase.cpp src/ReceivingImageNode.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_include_directories(${PROJECT_NAME} PUBLIC ${OpenCV_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PUBLIC common)
target_link_libraries(${PROJECT_NAME} PUBLIC gstreamer_plugins_worst)
target_link_libraries(${PROJECT_NAME} PUBLIC ${OpenCV_LIBS})
target_link_libraries(${PROJECT_NAME} PUBLIC msg)
target_link_libraries(${PROJECT_NAME} PUBLIC concurra)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-sdp)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-app)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-video)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-rtsp-server)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-rtsp)
target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gstreamer-rtp)
target_link_libraries(${PROJECT_NAME} PUBLIC msg_yas)
target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_23)
target_compile_definitions(${PROJECT_NAME} PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_executable(test_${PROJECT_NAME} test/test_${PROJECT_NAME}.cpp)
target_link_libraries(test_${PROJECT_NAME} PUBLIC ${PROJECT_NAME})
target_link_libraries(test_${PROJECT_NAME} PUBLIC common)
target_link_libraries(test_${PROJECT_NAME} PUBLIC image_processing_nodes)
target_link_libraries(test_${PROJECT_NAME} PUBLIC cameras_simulator_nodes)
target_compile_features(test_${PROJECT_NAME} PRIVATE cxx_std_23)
target_compile_definitions(test_${PROJECT_NAME} PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_executable(test_${PROJECT_NAME}_receive test/test_${PROJECT_NAME}_receive.cpp)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC ${PROJECT_NAME})
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC common)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC image_processing_nodes)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC image_visualization_nodes)
target_link_libraries(test_${PROJECT_NAME}_receive PUBLIC cameras_simulator_nodes)
target_compile_features(test_${PROJECT_NAME}_receive PRIVATE cxx_std_23)
target_compile_definitions(test_${PROJECT_NAME}_receive PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_test(NAME ctest_${PROJECT_NAME}
        COMMAND bash -c "${CMAKE_CURRENT_BINARY_DIR}/test_${PROJECT_NAME} & ${CMAKE_CURRENT_BINARY_DIR}/test_${PROJECT_NAME}_receive & wait"
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

add_executable(test_custom_media_factory test/test_custom_media_factory.cpp)
target_link_libraries(test_custom_media_factory PUBLIC PkgConfig::gstreamer)
target_link_libraries(test_custom_media_factory PUBLIC PkgConfig::gstreamer-sdp)
target_link_libraries(test_custom_media_factory PUBLIC PkgConfig::gstreamer-app)
target_link_libraries(test_custom_media_factory PUBLIC PkgConfig::gstreamer-video)
target_link_libraries(test_custom_media_factory PUBLIC PkgConfig::gstreamer-rtsp-server)
target_link_libraries(test_custom_media_factory PUBLIC PkgConfig::gstreamer-rtsp)
target_link_libraries(test_custom_media_factory PUBLIC PkgConfig::gstreamer-rtp)
target_compile_features(test_custom_media_factory PRIVATE cxx_std_23)
target_compile_definitions(test_custom_media_factory PRIVATE CMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")
