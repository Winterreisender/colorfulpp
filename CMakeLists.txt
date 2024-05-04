# Project
cmake_minimum_required(VERSION 3.28)
project(coloro)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_SCAN_FOR_MODULES ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Packages
## GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://mirror.ghproxy.com/https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Core Lib
add_library(libcolorfulpp) 
target_sources(libcolorfulpp
  PUBLIC FILE_SET CXX_MODULES FILES src/colorfulpp.mpp
)

# CLI
add_executable(cli src/cli.cpp)
target_link_libraries(cli libcolorfulpp)

# Test
enable_testing()
add_executable(unittest
  tests/test_main.cpp
)
target_link_libraries(unittest
  libcolorfulpp
  GTest::gtest_main
)
include(GoogleTest)
gtest_discover_tests(unittest)