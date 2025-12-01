#include "ProblemController.h"
#include <drogon/drogon.h>
#include <json/json.h>

#include <bsoncxx/json.hpp>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/builder/stream/helpers.hpp>
#include <bsoncxx/builder/basic/document.hpp>
#include <bsoncxx/builder/basic/kvp.hpp>

void ProblemController::initMongo() {
    static mongocxx::instance inst{};
    client = new mongocxx::client(mongocxx::uri("mongodb://localhost:27017"));
}

//  GET /problems
void ProblemController::listProblems(const HttpRequestPtr&,
                                     std::function<void(const HttpResponsePtr&)>&& callback) {
    auto db = client->database("CodeCoach");
    auto cursor = db["problems"].find({});

    Json::Value problems(Json::arrayValue);
    for (auto&& doc : cursor) {
        Json::Value item;
        if (doc["title"]) item["title"] = std::string(doc["title"].get_string().value);
        if (doc["description"]) item["description"] = std::string(doc["description"].get_string().value);
        if (doc["inputExample"]) item["inputExample"] = std::string(doc["inputExample"].get_string().value);
        if (doc["outputExample"]) item["outputExample"] = std::string(doc["outputExample"].get_string().value);
        problems.append(item);
    }

    auto resp = HttpResponse::newHttpJsonResponse(problems);
    callback(resp);
}

//  POST /problems
void ProblemController::createProblem(const HttpRequestPtr& req,
                                      std::function<void(const HttpResponsePtr&)>&& callback) {
    auto json = req->getJsonObject();
    if (!json) {
        auto resp = HttpResponse::newHttpResponse();
        resp->setStatusCode(k400BadRequest);
        resp->setBody("Invalid JSON");
        callback(resp);
        return;
    }

    auto db = client->database("CodeCoach");
    auto coll = db["problems"];

    bsoncxx::builder::stream::document doc;
    doc << "title" << (*json)["title"].asString()
        << "description" << (*json)["description"].asString()
        << "inputExample" << (*json)["inputExample"].asString()
        << "outputExample" << (*json)["outputExample"].asString();

    coll.insert_one(doc.view());

    auto resp = HttpResponse::newHttpJsonResponse(*json);
    resp->setStatusCode(k201Created);
    callback(resp);
}

// PUT /problems/{title}
void ProblemController::updateProblem(const HttpRequestPtr& req,
                                      std::function<void(const HttpResponsePtr&)>&& callback,
                                      std::string title) {
    auto json = req->getJsonObject();
    if (!json) {
        auto resp = HttpResponse::newHttpResponse();
        resp->setStatusCode(k400BadRequest);
        resp->setBody("Invalid JSON");
        callback(resp);
        return;
    }

    auto db = client->database("CodeCoach");
    auto coll = db["problems"];

    bsoncxx::builder::stream::document filter_builder;
    filter_builder << "title" << title;

    bsoncxx::builder::stream::document update_builder;
    update_builder << "$set" << bsoncxx::builder::stream::open_document
                   << "description" << (*json)["description"].asString()
                   << "inputExample" << (*json)["inputExample"].asString()
                   << "outputExample" << (*json)["outputExample"].asString()
                   << bsoncxx::builder::stream::close_document;

    auto result = coll.update_one(filter_builder.view(), update_builder.view());

    Json::Value response;
    if (result && result->modified_count() > 0) {
        response["status"] = "updated";
    } else {
        response["status"] = "not found";
    }

    auto resp = HttpResponse::newHttpJsonResponse(response);
    callback(resp);
}

// DELETE /problems/{title}
void ProblemController::deleteProblem(const HttpRequestPtr&,
                                      std::function<void(const HttpResponsePtr&)>&& callback,
                                      std::string title) {
    auto db = client->database("CodeCoach");
    auto coll = db["problems"];

    bsoncxx::builder::stream::document filter_builder;
    filter_builder << "title" << title;

    auto result = coll.delete_one(filter_builder.view());

    Json::Value response;
    if (result && result->deleted_count() > 0) {
        response["status"] = "deleted";
    } else {
        response["status"] = "not found";
    }

    auto resp = HttpResponse::newHttpJsonResponse(response);
    callback(resp);
}
