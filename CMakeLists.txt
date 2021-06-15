
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(eic_beam_shape)

#shared library
set (LIB eic_beam_shape)

#sources and headers
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cxx)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.h)
include_directories(${PROJECT_SOURCE_DIR}/include)

#ROOT
find_package(ROOT REQUIRED COMPONENTS Core EG Hist Physics RIO Tree MathCore)
include(${ROOT_USE_FILE})

#build the library
add_library (${LIB} SHARED ${sources} ${headers})
target_link_libraries(${LIB} ${ROOT_LIBRARIES})

