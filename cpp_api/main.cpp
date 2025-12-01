//
// Created by kevin on 27/10/25.
//

#include <drogon/drogon.h>
#include "controllers/ProblemController.h"


int main() {
    ProblemController::initMongo();

    drogon::app()
            .setLogLevel(trantor::Logger::kTrace)   // esto es para mostrar el registro para debuggear
            .addListener("0.0.0.0", 8080)
            .run();
}
