cmake_minimum_required(VERSION 3.14...3.21)

project(compressor LANGUAGES C CXX)

enable_testing()

# C++ code
set(CMAKE_CXX_STANDARD 20)

add_library(bwt_cxx OBJECT burrows_wheeler.cxx)
target_include_directories(bwt_cxx PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(test_bwt_cxx test_bwt_text.cxx)
target_link_libraries(test_bwt_cxx PRIVATE bwt_cxx)

add_executable(rle_cxx rle.cxx)

# C code

add_library(bwt_c OBJECT burrows_wheeler.c)
target_include_directories(bwt_c PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(test_bwt_c test_bwt_text.c)
target_link_libraries(test_bwt_c PRIVATE bwt_c)

add_executable(rle_c rle.c)
