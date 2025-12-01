//
// Created by kevin on 28/10/25.
//
#pragma once
#include <drogon/HttpController.h>
#include <json/json.h>
#include <fstream>
#include <sstream>
#include <cstdio>   // remove()
#include <cstdlib>  // system()
#include <iostream>

using namespace drogon;

class EvaluationController : public drogon::HttpController<EvaluationController>
{
public:
    METHOD_LIST_BEGIN
        ADD_METHOD_TO(EvaluationController::evaluate, "/evaluate", Post);
    METHOD_LIST_END

    void evaluate(const HttpRequestPtr &req, std::function<void(const HttpResponsePtr &)> &&callback);
};
