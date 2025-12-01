#include "EvaluationController.h"
#include <drogon/drogon.h>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/json.hpp>
#include <json/json.h>
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <chrono>
#include <mongocxx/client.hpp>

void EvaluationController::evaluate(const drogon::HttpRequestPtr &req,
                                    std::function<void(const drogon::HttpResponsePtr &)> &&callback)
{
    auto json = req->getJsonObject();
    if (!json || !json->isMember("title") || !json->isMember("code"))
    {
        Json::Value err;
        err["error"] = "Missing title or code";
        auto resp = HttpResponse::newHttpJsonResponse(err);
        resp->setStatusCode(k400BadRequest);
        callback(resp);
        return;
    }

    std::string title = (*json)["title"].asString();
    std::string code = (*json)["code"].asString();

    // --- Conexión a MongoDB ---
    mongocxx::client conn{mongocxx::uri{}};
    auto db = conn["CodeCoach"];
    auto collection = db["problems"];

    // --- Buscar el problema por título ---
    auto result = collection.find_one(
            bsoncxx::builder::stream::document{} << "title" << title
                                                 << bsoncxx::builder::stream::finalize);

    if (!result)
    {
        Json::Value err;
        err["error"] = "Problem not found";
        auto resp = HttpResponse::newHttpJsonResponse(err);
        resp->setStatusCode(k404NotFound);
        callback(resp);
        return;
    }

    // --- Obtener el expected output ---
    auto view = result->view();
    std::string expected;
    auto it = view.find("outputExample");
    if (it != view.end()) {
        try {
            expected = std::string(it->get_string().value);
        } catch (const std::exception &e) {
            expected = "";
            std::cerr << "Warning: outputExample no es tipo string (" << e.what() << ")\n";
        }
    } else {
        expected = "";
    }

    // --- Guardar el código temporalmente ---
    std::ofstream sourceFile("temp.cpp");
    sourceFile << code;
    sourceFile.close();

    auto start = std::chrono::high_resolution_clock::now();

    // --- Compilar ---
    int compileCode = std::system("g++ temp.cpp -o temp.out 2> compile_error.txt");
    if (compileCode != 0)
    {
        std::ifstream errFile("compile_error.txt");
        std::string errorMsg((std::istreambuf_iterator<char>(errFile)),
                             std::istreambuf_iterator<char>());

        Json::Value err;
        err["status"] = "error";
        err["message"] = errorMsg;
        auto resp = HttpResponse::newHttpJsonResponse(err);
        callback(resp);
        return;
    }

    // --- Ejecutar el programa ---
    std::system("chmod +x temp.out && ./temp.out > output.txt");

    std::ifstream output("output.txt");
    std::string got((std::istreambuf_iterator<char>(output)), std::istreambuf_iterator<char>());

    auto end = std::chrono::high_resolution_clock::now();
    double exec_time = std::chrono::duration<double, std::milli>(end - start).count();

    // --- Limpiar espacios y saltos de línea ---
    auto trim = [](std::string &s) {
        if (s.empty()) return;
        s.erase(s.find_last_not_of(" \n\r\t") + 1);
        s.erase(0, s.find_first_not_of(" \n\r\t"));
    };
    trim(got);
    trim(expected);

    // --- Crear respuesta JSON ---
    Json::Value response;
    response["expected"] = expected;
    response["got"] = got;
    response["execution_time_ms"] = exec_time;
    response["status"] = (got == expected) ? "success" : "failure";

    auto resp = HttpResponse::newHttpJsonResponse(response);
    callback(resp);
}
