cmake_minimum_required(VERSION 3.10)
project(curl_example)

set(CMAKE_CXX_STANDARD 11)
find_package(CURL REQUIRED)

add_executable(curl_example main.cpp)
target_link_libraries(curl_example ${CURL_LIBRARIES})
include_directories(${CURL_INCLUDE_DIRS})
