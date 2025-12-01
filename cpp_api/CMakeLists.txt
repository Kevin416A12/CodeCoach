cmake_minimum_required(VERSION 3.10)
project(CodeCoachAPI)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_TYPE Debug)

# Donde están las librerías Drogon y Mongo
set(CMAKE_PREFIX_PATH "/usr/local/lib/cmake")

# Buscar paquetes
find_package(Drogon CONFIG REQUIRED)
find_package(mongocxx CONFIG REQUIRED)
find_package(bsoncxx CONFIG REQUIRED)
find_package(jsoncpp REQUIRED)

# Incluir headers
include_directories(
        ${CMAKE_SOURCE_DIR}/controllers
        ${CMAKE_SOURCE_DIR}/models
        /usr/local/include
        /usr/include/jsoncpp
)

# Crear ejecutable (usa .cpp en lugar de .cc)
add_executable(CodeCoachAPI
        main.cpp
        controllers/ProblemController.cpp
        models/Problem.cpp
        controllers/EvaluationController.cpp

)

# Vincular librerías
target_link_libraries(CodeCoachAPI
        PRIVATE
        Drogon::Drogon
        /usr/local/lib/libmongocxx.so
        /usr/local/lib/libbsoncxx.so
        jsoncpp_lib
)

