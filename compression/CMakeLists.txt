cmake_minimum_required(VERSION 3.14...3.21)

project(compressor LANGUAGES C CXX)

enable_testing()

add_executable(bwt_cxx burrows_wheeler.cxx)
target_compile_features(bwt_cxx PRIVATE cxx_std_11)

add_executable(rle_cxx rle.cxx)
target_compile_features(rle_cxx PRIVATE cxx_std_20)

add_executable(bwt_c burrows_wheeler.c)
add_executable(rle_c rle.c)
