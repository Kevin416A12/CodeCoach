#pragma once
#include <drogon/HttpController.h>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>

using namespace drogon;

class ProblemController : public drogon::HttpController<ProblemController> {
public:
    static void initMongo();
    static inline mongocxx::client* client = nullptr;

    METHOD_LIST_BEGIN
        ADD_METHOD_TO(ProblemController::listProblems, "/problems", Get);
        ADD_METHOD_TO(ProblemController::createProblem, "/problems", Post);
        ADD_METHOD_TO(ProblemController::updateProblem, "/problems/{1}", Put);
        ADD_METHOD_TO(ProblemController::deleteProblem, "/problems/{1}", Delete);
    METHOD_LIST_END

    void listProblems(const HttpRequestPtr& req,
                      std::function<void(const HttpResponsePtr&)>&& callback);

    void createProblem(const HttpRequestPtr& req,
                       std::function<void(const HttpResponsePtr&)>&& callback);

    void updateProblem(const HttpRequestPtr& req,
                       std::function<void(const HttpResponsePtr&)>&& callback,
                       std::string title);

    void deleteProblem(const HttpRequestPtr& req,
                       std::function<void(const HttpResponsePtr&)>&& callback,
                       std::string title);
};
